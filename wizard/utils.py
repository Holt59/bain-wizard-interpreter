# -*- encoding: utf-8 -*-

from pathlib import Path
from typing import BinaryIO, Iterable, Optional, TextIO, Union, overload

import chardet
from antlr4 import CommonTokenStream, InputStream, Parser, Token
from antlr4.error.ErrorListener import ConsoleErrorListener, ErrorListener
from antlr4.error.Errors import RecognitionException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.IntervalSet import IntervalSet

from .antlr4.wizardLexer import wizardLexer
from .antlr4.wizardParser import wizardParser
from .contexts import WizardInterpreterContextFactory, WizardTopLevelContext
from .contexts.utils import wrap_exceptions
from .expr import WizardExpressionVisitor
from .functions import make_basic_functions, make_manager_functions
from .keywords import WizardKeywordVisitor
from .manager import ManagerModInterface
from .runner import WizardRunnerExpressionVisitor, WizardRunnerKeywordVisitor
from .severity import SeverityContext
from .state import ContextState, WizardInterpreterState
from .value import SubPackages


class WizardErrorStrategy(DefaultErrorStrategy):

    """
    Custom error strategy that tries to recover for broken Wizard scripts.

    This class is inspired by DefaultErrorStrategy but is really experimental.
    Basically, it should recover by broken scripts by closing enclosing control
    block, e.g. if the body of a If is broken, we try to look for a Elif, Else
    or EndIf and skip everything in-between.
    """

    # "Block" contexts are context for which we need to consume the last token when
    # recovering to move to the next rule. This is basically the contexts for all the
    # rules that contains a EndXXX token at the end.
    BlockContexts = {
        wizardParser.IfStmtContext: wizardLexer.EndIf,
        wizardParser.ForStmtContext: wizardLexer.EndFor,
        wizardParser.SelectStmtContext: wizardLexer.EndSelect,
        wizardParser.WhileStmtContext: wizardLexer.EndWhile,
    }

    def recover(self, recognizer: Parser, e: RecognitionException):

        # Mark the context (and "some" parent contexts):
        recognizer._ctx.exception = e

        # Try to do custom recovery using control-flow:
        controlRecoverSet = self.getControlRecoverySet(recognizer)
        index = recognizer._input.index
        state = recognizer.state

        if controlRecoverSet.intervals:
            self.consumeUntil(recognizer, controlRecoverSet)

        # Same state, nothing was done, fallback to parent:
        if recognizer.state == state and recognizer._input.index == index:
            super().recover(recognizer, e)
        else:

            # Something was consumed, but do we have to consume the next token
            # to close the statement? Yes if the current context if a "block"
            # context and the next context its close token:
            for tctx, tok in self.BlockContexts.items():
                if (
                    isinstance(recognizer._ctx, tctx)
                    and recognizer.getTokenStream().LA(1) == tok
                ):
                    recognizer.consume()
                    break

        return recognizer.getTokenStream().LT(1)

    def getControlRecoverySet(self, recognizer: Parser):
        ctx = recognizer._ctx
        recoverSet = IntervalSet()

        while ctx is not None and ctx.invokingState >= 0:

            # If statement (for Else we only want EndIf):
            if isinstance(
                ctx, (wizardParser.IfStmtContext, wizardParser.ElifStmtContext)
            ):
                recoverSet.addOne(wizardLexer.Elif)
                recoverSet.addOne(wizardLexer.Else)
                recoverSet.addOne(wizardLexer.EndIf)
            elif isinstance(ctx, wizardParser.ElseStmtContext):
                recoverSet.addOne(wizardLexer.EndIf)

            # For/While statement:
            elif isinstance(ctx, wizardParser.ForStmtContext):
                recoverSet.addOne(wizardLexer.EndFor)
            elif isinstance(ctx, wizardParser.WhileStmtContext):
                recoverSet.addOne(wizardLexer.EndWhile)

            # Case/Default context:
            elif isinstance(
                ctx,
                (wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext),
            ):
                recoverSet.addOne(wizardLexer.Break)

            # Select context:
            elif isinstance(ctx, wizardParser.SelectStmtContext):
                recoverSet.addOne(wizardLexer.EndSelect)

            ctx = ctx.parentCtx
        recoverSet.removeOne(Token.EPSILON)

        return recoverSet


def make_basic_context_factory(
    subpackages: SubPackages, severity: SeverityContext
) -> WizardInterpreterContextFactory:
    """
    Make a basic context factory from the given subpackages and severity context.
    The expression visitor includes the basic functions (see `make_basic_functions`).

    Args:
        subpackages: The subpackages used for the expression visitor.
        severity: The severity context to use.

    Returns:
        A basic context factory, built using default expression and keyword visitors.
    """
    evisitor = WizardExpressionVisitor(subpackages, make_basic_functions(), severity)
    kvisitor: WizardKeywordVisitor[WizardInterpreterState] = WizardKeywordVisitor(
        severity
    )
    return WizardInterpreterContextFactory(evisitor, kvisitor, severity)


def make_runner_context_factory(
    subpackages: SubPackages, manager: ManagerModInterface, severity: SeverityContext
) -> WizardInterpreterContextFactory:
    """
    Make a runner context factory from the given subpackages, severity context and
    manager.

    This method constructs a context factory using a `WizardRunnerExpressionVisitor`
    and a `WizardRunnerKeywordVisitor` constructed from the given parameters. The
    expression visitor also includes the basic functions (see `make_basic_functions`).

    Args:
        subpackages: The subpackages used for the expression visitor and keyword
            visitors.
        manager: The manager to use for the expression visitor (functions).
        severity: The severity context to use.

    Returns:
        A context factory, built using runner expression and keyword visitors.
    """
    functions = make_basic_functions()
    functions.update(make_manager_functions(manager, severity))
    evisitor = WizardRunnerExpressionVisitor(subpackages, functions, severity)
    kvisitor = WizardRunnerKeywordVisitor(subpackages, severity)
    return WizardInterpreterContextFactory(evisitor, kvisitor, severity)


def make_parse_wizard_context(
    script: Union[InputStream, Path, BinaryIO, TextIO, str],
    wrap_excs: bool = True,
    error_listeners: Iterable[ErrorListener] = [],
) -> wizardParser.ParseWizardContext:
    """
    Create a ParseWizardContext from the given script. Depending on the type of
    the script, the following procedure is used to parse the script:
    - If `script` is an `InputStream`, it is used as-is.
    - If `script` is a `Path`, it should point to a file containing a Wizard script.
    - If `script` is a `TextIO`, it is equivalent to the `str` version after reading
        the whole file.
    - If `script` is a `str`, an `InputStream` is constructed from it.

    Args:
        script: The script to create a context for.
        wrap_excs: If True, exceptions will be converted to Wizard exceptions (when
            possible).

    Returns:
        A ParseWizardContext extracted from the given script.
    """

    # Make a stream:
    stream: InputStream
    if isinstance(script, InputStream):
        stream = script
    elif isinstance(script, str):
        stream = InputStream(script)
    else:
        if isinstance(script, Path):
            with open(script, "rb") as fp:
                data = fp.read()
        else:
            data = script.read()  # type: ignore
        if isinstance(data, bytes):
            encoding = chardet.detect(data)["encoding"]
            text = data.decode(encoding)
        else:
            text = data
        stream = InputStream(text)

    # Create the lexer and disable console logs:
    lexer = wizardLexer(stream)
    lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)

    stream = CommonTokenStream(lexer)

    # Create the parser with a custom error strategy:
    parser = wizardParser(stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
    parser._errHandler = WizardErrorStrategy()

    # Run the interpret:
    if wrap_excs:
        return wrap_exceptions(parser.parseWizard)  # type: ignore
    return parser.parseWizard()  # type: ignore


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
    state: ContextState,
    **kwargs,
) -> WizardTopLevelContext[ContextState]:
    ...


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
    **kwargs,
) -> WizardTopLevelContext[WizardInterpreterState]:
    ...


def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
    state: Optional[ContextState] = None,
    **kwargs,
) -> Union[
    WizardTopLevelContext[ContextState], WizardTopLevelContext[WizardInterpreterState]
]:
    """
    Create a WizardTopLevelContext from the given script.

    Args:
        script: The script to create a context for. See make_parse_wizard_context for
            details on the possible types.
        factory: The factory for the top-level context.
        state: The state for the top-level context. If None, a WizardInterpreterState()
            will be used.
        **kwargs: Extra named parameters that are passed to `make_parse_wizard_context`.

    Returns:
        A ParseWizardContext extracted from the given script.
    """

    ctx = make_parse_wizard_context(script, **kwargs)

    if state is None:
        return WizardTopLevelContext(factory, ctx, WizardInterpreterState())
    else:
        return WizardTopLevelContext(factory, ctx, state)
