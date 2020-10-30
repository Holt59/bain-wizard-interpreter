# -*- encoding: utf-8 -*-

import inspect

from enum import Enum, auto
from typing import (
    Any,
    Callable,
    List,
    Mapping,
    MutableMapping,
    Optional,
)

from .antlr4.wizardParser import wizardParser

from .basic_functions import WizardFunctions
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
    VariableType,
    WizardExpressionVisitor,
)
from .mmitf import ModManagerInterface
from .severity import Issue, SeverityContext
from .utils import wrap_function, optional


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

    # Wizard functions utils:
    _wizard_fns: WizardFunctions

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
        self._wizard_fns = WizardFunctions()

        self._variables = {}
        self._subpackages = subpackages
        self._functions = {}

        self._evisitor = WizardExpressionVisitor(self)

        self._functions.update(self.manager_functions(manager))
        self._functions.update(self.basic_functions(self._wizard_fns))
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

    # Functions:

    def basic_functions(
        self, wf: WizardFunctions
    ) -> Mapping[str, Callable[[List[Value]], Value]]:
        """
        Create a list of basic functions.

        Args:
            wf: The WizardFunctions object to use for the basic functions.

        Returns:
            A mapping from function name to basic functions, including methods.
        """

        fns: MutableMapping[str, Callable[[List[Value]], Value]] = {}

        # Add all the free functions:
        for fname in dir(wf):
            if fname.startswith("__"):
                continue
            sig = inspect.signature(getattr(wf, fname))
            varargs = "args" in sig.parameters
            fns[fname] = wrap_function(
                fname,
                getattr(wf, fname),
                *(object for _ in range(len(sig.parameters) - varargs)),
                varargs=varargs,
                rawargs=True,
            )

        # Add methods:
        for fname in dir(wf):
            if fname.startswith("__"):
                continue
            fns["string." + fname] = fns[fname]

        for t in ("integer", "float", "bool"):
            fns[t + ".str"] = fns["str"]

        return fns

    def manager_functions(
        self, manager: ModManagerInterface
    ) -> Mapping[str, Callable[[List[Value]], Value]]:
        """
        Add manager functions to the _functions member variables. These functions
        calls method of the manager passed in.

        Args:
            manager: The manager to delete the call to.
        """

        fns: MutableMapping[str, Callable[[List[Value]], Value]] = {}

        for t in [
            # Functions:
            ("CompareGameVersion", manager.compareGameVersion, str),
            ("CompareSEVersion", manager.compareSEVersion, str),
            ("CompareGEVersion", manager.compareGEVersion, str),
            ("CompareWBVersion", manager.compareWBVersion, str),
            ("GetPluginLoadOrder", manager.getPluginLoadOrder, str, optional(int)),
            ("GetPluginStatus", manager.getPluginStatus, str),
            ("GetEspmStatus", manager.getPluginStatus, str),
            ("DisableINILine", manager.disableINILine, str, str, str),
            ("EditINI", manager.editINI, str, str, str, Any, optional(str)),
            ("GetFilename", manager.getFilename, str),
            ("GetFolder", manager.getFolder, str),
            # Keywords:
            ("DeSelectAll", manager.deselectAll),
            ("DeSelectAllPlugins", manager.deselectAllPlugins),
            ("DeSelectAllEspms", manager.deselectAllPlugins),
            ("DeSelectPlugin", manager.deselectPlugin, str),
            ("DeSelectEspm", manager.deselectPlugin, str),
            ("DeSelectSubPackage", manager.deselectSubPackage, str),
            ("RenamePlugin", manager.renamePlugin, str, str),
            ("RenameEspm", manager.renamePlugin, str, str),
            (
                "RequireVersions",
                manager.requiresVersions,
                str,
                optional(str),
                optional(str),
                optional(str),
            ),
            ("ResetPluginName", manager.resetPluginName, str),
            ("ResetEspmName", manager.resetPluginName, str),
            ("ResetAllPluginNames", manager.resetAllPluginNames),
            ("ResetAllEspmNames", manager.resetAllPluginNames),
            ("SelectAll", manager.selectAll),
            ("SelectAllPlugins", manager.selectAllPlugins),
            ("SelectAllEspms", manager.selectAllPlugins),
            ("SelectPlugin", manager.selectPlugin, str),
            ("SelectEspm", manager.selectPlugin, str),
            ("SelectSubPackage", manager.selectSubPackage, str),
        ]:
            fns[t[0]] = wrap_function(*t)  # type: ignore

        # Varargs:
        fns["DataFileExists"] = wrap_function(
            "DataFileExists", manager.dataFileExists, str, varargs=True
        )

        # Any type?
        def note(x: object):
            self.raise_or_warn(
                Issue.USAGE_OF_ANYTHING_IN_NOTE,
                TypeError(
                    "'Note' keyword expected string, found"
                    f" {VariableType.from_pytype(type(x))}."
                ),
                "'Note' keyword expected string, found"
                f" {VariableType.from_pytype(type(x))}.",
            )
            return manager.note(str(x))

        fns["Note"] = wrap_function("Note", note, object)

        return fns

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
