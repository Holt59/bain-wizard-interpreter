# -*- encoding: utf-8 -*-

from pathlib import Path
from typing import Optional, Union, TextIO, overload

from antlr4 import InputStream, FileStream, CommonTokenStream, BailErrorStrategy

from .antlr4.wizardLexer import wizardLexer
from .antlr4.wizardParser import wizardParser

from .contexts import WizardTopLevelContext, WizardInterpreterContextFactory
from .expr import WizardExpressionVisitor
from .functions import make_basic_functions, make_manager_functions
from .keywords import WizardKeywordVisitor
from .manager import ManagerModInterface
from .runner import WizardRunnerExpressionVisitor, WizardRunnerKeywordVisitor
from .severity import SeverityContext
from .state import ContextState, WizardInterpreterState
from .value import SubPackages


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
    script: Union[InputStream, Path, TextIO, str]
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

    Returns:
        A ParseWizardContext extracted from the given script.
    """

    # Make a stream:
    stream: InputStream
    if isinstance(script, InputStream):
        stream = script
    elif isinstance(script, Path):
        stream = FileStream(script)
    elif isinstance(script, str):
        stream = InputStream(script)
    else:
        stream = InputStream(script.read())

    lexer = wizardLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = wizardParser(stream)
    parser._errHandler = BailErrorStrategy()

    # Run the interpret:
    return parser.parseWizard()  # type: ignore


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
    state: ContextState,
) -> WizardTopLevelContext[ContextState]:
    ...


@overload
def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
) -> WizardTopLevelContext[WizardInterpreterState]:
    ...


def make_top_level_context(
    script: Union[InputStream, Path, TextIO, str],
    factory: WizardInterpreterContextFactory,
    state: Optional[ContextState] = None,
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

    Returns:
        A ParseWizardContext extracted from the given script.
    """

    ctx = make_parse_wizard_context(script)

    if state is None:
        return WizardTopLevelContext(factory, ctx, WizardInterpreterState())
    else:
        return WizardTopLevelContext(factory, ctx, state)
