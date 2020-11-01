# -*- encoding: utf-8 -*-

import copy

from enum import Enum, auto
from typing import (
    Callable,
    List,
    Mapping,
    MutableMapping,
    Optional,
)

from .antlr4.wizardParser import wizardParser

from .functions import make_basic_functions, make_manager_functions
from .contexts import (
    WizardBodyContext,
    WizardInterpreterContext,
    WizardCancelContext,
    WizardReturnContext,
)
from .expr import (
    AbstractWizardInterpreter,
    SubPackages,
    Value,
    WizardExpressionVisitor,
)
from .mmitf import ModManagerInterface, WizardRunner, WizardRunnerState
from .severity import SeverityContext


class WizardInterpreterResult(Enum):

    # TODO: More clean way to do this (with extra info?).

    # A 'Cancel' instruction was encountered:
    CANCEL = auto()

    # A 'Return' instruction was encountered:
    RETURN = auto()

    # The script was completely executed:
    COMPLETED = auto()


class WizardInterpreterState(WizardRunnerState):

    """
    Wrapper class that contains the context to rewind to (WizardInterpreterContext)
    and the variables.

    Note that the variables and the parent contexts are shared between all states
    unless a deepcopy is made.
    """

    # The interpreter context:
    _context: Optional[WizardInterpreterContext]

    # The list of variables:
    _variables: MutableMapping[str, Value]

    def __init__(
        self,
        context: Optional[WizardInterpreterContext],
        variables: MutableMapping[str, Value],
    ):
        self._context = context
        self._variables = variables

    @property
    def context(self) -> Optional[WizardInterpreterContext]:
        """
        Returns:
            Return the context associated with this state.
        """
        return self._context

    @property
    def variables(self) -> MutableMapping[str, Value]:
        """
        Returns:
            The variables for this state.
        """
        return self._variables

    def exec(self) -> "WizardInterpreterState":
        """
        Call exec() on the underlying context and return a wrapped version
        of the context.

        Returns:
            A new interpreter state after applying exec() on the underlying
            context.
        """
        assert self.context is not None
        return WizardInterpreterState(self.context.exec(), self.variables)

    def __bool__(self) -> bool:
        """
        Returns:
            True if this state contains a context, False otherwise.
        """
        return bool(self.context)


class WizardInterpreter(AbstractWizardInterpreter, SeverityContext, WizardRunner):

    """
    The WizardInterpreter is the main interpreter for Wizard scripts. It contains
    most control and flow operations (visitXXX function), and uses an expression
    visitor to parse expression.
    """

    # Internal exceptions used to rewind / cancel at any point:
    class RewindFlow(Exception):

        """
        Exception used to rewind a script execution when calling rewind().
        """

        _state: WizardRunnerState

        def __init__(self, state: WizardRunnerState):
            self._state = state

        @property
        def state(self) -> WizardRunnerState:
            """
            Returns:
                The state to rewind to.
            """
            return self._state

    class CancelFlow(Exception):

        """
        Exception used to cancel a script execution when calling abort().
        """

        ...

    # The Mod Manager interface contains function that are MM-specific, e.g.
    # check if a file exists, or install a subpackage, etc.
    _manager: ModManagerInterface

    # The list of subpackages in the archives:
    _subpackages: SubPackages

    # The list of functions:
    _functions: MutableMapping[str, Callable[[List[Value]], Value]]

    # The expression visitor:
    _evisitor: WizardExpressionVisitor

    # Under this are stuff that can be "rewound":

    _state: WizardInterpreterState

    def __init__(
        self,
        manager: ModManagerInterface,
        subpackages: SubPackages,
        extra_functions: Mapping[str, Callable[[List[Value]], Value]] = {},
    ):
        """
        Args:
            manager: The Mod Manager interface. See ModManagerInterface for
                more details on what needs to be implemented.
            subpackages: The list of SubPackages in the archive.
            functions: List of extra functions to made available to the script.
                Can override default functions.
        """
        SeverityContext.__init__(self)

        self._manager = manager

        self._subpackages = subpackages
        self._functions = {}

        self._evisitor = WizardExpressionVisitor(self)

        self._functions.update(make_manager_functions(manager, self))
        self._functions.update(make_basic_functions())
        self._functions.update(extra_functions)

        # Initial state, in case someone calls variables() or context():
        self._state = WizardInterpreterState(None, {})

    # AbstractWizardInterpreter interface:
    @property
    def subpackages(self) -> SubPackages:
        return self._subpackages

    @property
    def variables(self) -> MutableMapping[str, Value]:
        return self._state.variables

    @property
    def functions(self) -> Mapping[str, Callable[[List[Value]], Value]]:
        return self._functions

    @property
    def severity(self) -> SeverityContext:
        return self

    @property
    def manager(self) -> ModManagerInterface:
        return self._manager

    def warning(self, text: str):
        self._manager.warning(text)

    # WizardRunner interface:

    def abort(self):
        raise WizardInterpreter.CancelFlow()

    def rewind(self, context: WizardRunnerState):
        raise WizardInterpreter.RewindFlow(context)

    @property
    def context(self) -> WizardRunnerState:
        return copy.deepcopy(self._state)

    # Main entry:
    def visit(self, ctx: wizardParser.ParseWizardContext) -> WizardInterpreterResult:
        """
        Visit the main context.
        """

        self._state = WizardInterpreterState(
            WizardBodyContext(self, self._evisitor, ctx.body(), parent=None), {}
        )

        while self._state:
            try:
                self._state = self._state.exec()

                if isinstance(self._state.context, WizardCancelContext):
                    if self._manager.cancel():
                        return WizardInterpreterResult.CANCEL

                if isinstance(self._state.context, WizardReturnContext):
                    if self._manager.complete():
                        return WizardInterpreterResult.RETURN

            except WizardInterpreter.RewindFlow as rfex:
                self._state = rfex.state  # type: ignore

            except WizardInterpreter.CancelFlow:
                return WizardInterpreterResult.CANCEL

            except Exception as ex:
                self._manager.error(ex)

        return WizardInterpreterResult.COMPLETED
