# -*- encoding: utf-8 -*-

import copy

from typing import Dict, List, NamedTuple

from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser

from .interpreter import WizardInterpreter, WizardInterpreterResult
from .mmitf import ModManagerInterface, WizardRunnerState
from .value import SubPackages


class WizardRunnerData(NamedTuple):

    # The list of selected subpackages and plugins:
    subpackages: List[str] = []
    plugins: List[str] = []

    # Renaming of plugins (original name -> new name):
    renames: Dict[str, str] = {}

    # The list of notes:
    notes: List[str] = []


class WizardBundleState(WizardRunnerState):

    # The interpreter state:
    istate: WizardRunnerState

    # The runner date:
    data: WizardRunnerData

    def __init__(self, istate: WizardRunnerState, data: WizardRunnerData):
        self.istate = istate
        self.data = data


class WizardRunnerResult:

    # Status from the interpreter:
    _status: WizardInterpreterResult

    # The data from the runner:
    _data: WizardRunnerData

    def __init__(self, status: WizardInterpreterResult, data: WizardRunnerData):
        self._status = status
        self._data

    @property
    def status(self) -> WizardInterpreterResult:
        """
        Returns:
            The return status of ths interpreter.
        """
        return self._status

    @property
    def notes(self):
        """
        Returns:
            The notes set during script execution, in the order they were
            added..
        """
        return self._notes

    @property
    def subpackages(self) -> List[str]:
        """
        Returns:
            The list of selected subpackages, in alphabetical order.
        """
        return sorted(list(set(self._data.subpackages)))

    @property
    def plugins(self) -> List[str]:
        """
        Returns:
            The list of selected plugins, in alphabetical order.
        """
        return sorted(list(set(self._data.plugins)))


class WizardRunner(ModManagerInterface, WizardInterpreter):

    """
    A WizardRunner is an intermediate class that is both a Wizard interpreter
    and a partial ModManagerInterface.

    It implements sub-packages and plugins related stuff, so that only dialog
    and mod-manager specific stuffs need to be handled.
    """

    # The list of all plugins:
    _plugins: List[str]
    _data: WizardRunnerData

    def __init__(self, subpackages: SubPackages):
        ModManagerInterface.__init__(self)
        WizardInterpreter.__init__(self, self, subpackages)

        # "Setup" the mod-manager:
        self.setup(self)

        self._data = WizardRunnerData()
        self._plugins = [f for sp in subpackages for f in sp.files if self._isPlugin(f)]

    # Main method:
    def run(self, stream: InputStream):

        # Reset the data:
        self._data = WizardRunnerData()

        # Parse the stream:
        lexer = wizardLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        parser._errHandler = BailErrorStrategy()

        # Run the interpret:
        result = WizardInterpreter.visit(self, parser.parseWizard())

        # Wrap everything and return:
        return WizardRunnerResult(result, self._data)

    # Interpreter methods:
    def state(self) -> WizardRunnerState:
        # We wrap the parent state with the data. There should be no way for the
        # interpreter to change self._data in-between state(), so that should be ok.
        return WizardBundleState(
            WizardInterpreter.state(self), copy.deepcopy(self._data)
        )

    def rewind(self, state: WizardRunnerState):
        # Extract the parent state and the data and rewind them:
        assert isinstance(state, WizardBundleState)
        self._data = copy.deepcopy(state.data)
        WizardInterpreter.rewind(self, state.istate)

    # Methods that can be overridden:
    def _isPlugin(self, name: str) -> bool:
        """
        Check if the given name corresponds to a plugin.

        Args:
            name: The name of the file.

        Returns:
            True if the name corresponds to a plugin, False otherwise.
        """
        return name.endswith(".esp") or name.endswith(".esm") or name.endswith(".esl")

    # ModManagerInterface functions:
    def deselectAll(self):
        self._data.subpackages.clear()
        self._data.plugins.clear()

    def deselectAllPlugins(self):
        self._data.plugins.clear()

    def deselectPlugin(self, plugin_name: str):
        if plugin_name in self._data.plugins:
            self._data.plugins.remove(plugin_name)

    def deselectSubPackage(self, name: str):
        if name in self._data.subpackages:
            self._data.subpackages.remove(name)

    def note(self, text: str):
        self._data.notes.append(text)

    def selectAll(self):
        self._data.plugins = list(self._plugins)
        self._data.subpackages = [str(sp) for sp in self._subpackages]

    def selectAllPlugins(self):
        # Guess we only select plugins from selected subpackages?
        self._data.plugins = [
            f
            for sp in self._all_subpackages
            for f in sp.files
            if sp in self._subpackages and (f.endswith(".esp") or f.endswith(".esm"))
        ]

    def selectPlugin(self, plugin_name: str):
        self._plugins.append(plugin_name)

    def selectSubPackage(self, name: str):

        # Find the package:
        isp = self._subpackages.index(name)  # type: ignore
        subpackage = self._subpackages[isp]

        self._data.subpackages.append(name)

        # Auto-select plugins?
        for f in subpackage.files:
            if self._isPlugin(f):
                self.selectPlugin(f.split("\\")[-1])

    def renamePlugin(self, original_name: str, new_name: str):
        self._data.renames[original_name] = new_name

    def resetPluginName(self, original_name: str):
        if original_name in self._data.renames:
            del self._data.renames[original_name]

    def resetAllPluginNames(self):
        self._data.renames.clear()
