from pathlib import Path
from typing import Any, BinaryIO, TextIO, Union, overload

import chardet
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ConsoleErrorListener

from ..antlr4.wizardLexer import wizardLexer
from ..antlr4.wizardParser import wizardParser
from ..contexts import WizardInterpreterContextFactory, WizardTopLevelContext
from ..contexts.utils import wrap_exceptions
from ..expr import WizardExpressionVisitor
from ..functions import make_basic_functions, make_manager_functions
from ..keywords import WizardKeywordVisitor
from ..manager import ManagerModInterface
from ..runner import WizardRunnerExpressionVisitor, WizardRunnerKeywordVisitor
from ..severity import SeverityContext
from ..state import ContextState, WizardInterpreterState
from ..value import SubPackages


def make_basic_context_factory(
    subpackages: SubPackages, severity: SeverityContext
) -> WizardInterpreterContextFactory[Any]:
    """
    Make a basic context factory from the given subpackages and severity context.
    The expression visitor includes the basic functions (see `make_basic_functions`).

    Args:
        subpackages: The subpackages used for the expression visitor.
        severity: The severity context to use.

    Returns:
        A basic context factory, built using default expression and keyword visitors.
    """
    return WizardInterpreterContextFactory(
        WizardExpressionVisitor(subpackages, make_basic_functions(), severity),
        WizardKeywordVisitor(severity),
        severity,
    )


def make_runner_context_factory(
    subpackages: SubPackages, manager: ManagerModInterface, severity: SeverityContext
) -> WizardInterpreterContextFactory[Any]:
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
    from .error_strategy import WizardErrorStrategy

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

    token_stream = CommonTokenStream(lexer)

    # Create the parser with a custom error strategy:
    parser = wizardParser(token_stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
    parser._errHandler = WizardErrorStrategy()

    # Run the interpret:
    if wrap_excs:
        return wrap_exceptions(parser.parseWizard)
    return parser.parseWizard()


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory[ContextState],
    state: ContextState,
    *,
    wrap_excs: bool = True,
) -> WizardTopLevelContext[ContextState]: ...


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory[WizardInterpreterState],
    *,
    wrap_excs: bool = True,
) -> WizardTopLevelContext[WizardInterpreterState]: ...


def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory[ContextState],
    state: ContextState | None = None,
    *,
    wrap_excs: bool = True,
) -> WizardTopLevelContext[ContextState]:
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

    ctx = make_parse_wizard_context(script, wrap_excs=wrap_excs)

    if state is None:
        # if state is None, the second overload matches so we are using the basic
        # interpreter state
        state = WizardInterpreterState()  # type: ignore

    return WizardTopLevelContext(factory, ctx, None, state)
