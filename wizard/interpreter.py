# -*- encoding: utf-8 -*-

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
from .mmitf import ModManagerInterface
from .severity import SeverityContext


class WizardInterpreterResult(Enum):

    # TODO: More clean way to do this (with extra info?).

    # A 'Cancel' instruction was encountered:
    CANCEL = auto()

    # A 'Return' instruction was encountered:
    RETURN = auto()

    # The script was completely executed:
    COMPLETED = auto()


class WizardInterpreter(AbstractWizardInterpreter, SeverityContext):

    """
    The WizardInterpreter is the main interpreter for Wizard scripts. It contains
    most control and flow operations (visitXXX function), and uses an expression
    visitor to parse expression.
    """

    # The Mod Manager interface contains function that are MM-specific, e.g.
    # check if a file exists, or install a subpackage, etc.
    _manager: ModManagerInterface

    # The list of subpackages in the archives:
    _subpackages: SubPackages

    # The list of functions:
    _functions: MutableMapping[str, Callable[[List[Value]], Value]]

    # The expression visitor:
    _evisitor: WizardExpressionVisitor

    # Under this are stuff that can be "rewinded":

    # The list of variables:
    _variables: MutableMapping[str, Value]

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

        self._variables = {}
        self._subpackages = subpackages
        self._functions = {}

        self._evisitor = WizardExpressionVisitor(self)

        self._functions.update(make_manager_functions(manager, self))
        self._functions.update(make_basic_functions())
        self._functions.update(extra_functions)

    # AbstractWizardInterpreter interface:

    @property
    def subpackages(self) -> SubPackages:
        return self._subpackages

    @property
    def variables(self) -> MutableMapping[str, Value]:
        return self._variables

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

    # Main entry:
    def visit(self, ctx: wizardParser.ParseWizardContext) -> WizardInterpreterResult:
        """
        Visit the main context.
        """

        context: Optional[WizardInterpreterContext] = WizardBodyContext(
            self, self._evisitor, ctx.body(), parent=None
        )

        while context:
            context = context.exec()

            if isinstance(context, WizardCancelContext):
                return WizardInterpreterResult.CANCEL

            if isinstance(context, WizardReturnContext):
                return WizardInterpreterResult.RETURN

        return WizardInterpreterResult.COMPLETED
