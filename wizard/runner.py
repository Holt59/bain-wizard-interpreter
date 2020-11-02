# -*- encoding: utf-8 -*-

import copy

from pathlib import Path
from typing import Dict, List, TextIO, Union

from antlr4 import FileStream, InputStream, CommonTokenStream, BailErrorStrategy
from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser

from .errors import WizardMissingPackageError, WizardMissingPluginError
from .interpreter import WizardInterpreter, WizardInterpreterResult
from .mmitf import ModManagerInterface, WizardRunnerState
from .value import SubPackages
from .severity import Issue


class WizardRunnerData:

    """
    Wrapper around multiple containers that are updated during the execution
    of a Wizard script and need to be rewound.
    """

    # The list of selected subpackages and plugins:
    _subpackages: List[str]
    _plugins: List[str]

    # Renaming of plugins (original name -> new name):
    _renames: Dict[str, str]

    # The list of notes:
    _notes: List[str]

    def __init__(self):
        self._subpackages = []
        self._plugins = []
        self._renames = {}
        self._notes = []

    @property
    def subpackages(self) -> List[str]:
        """
        Returns:
            The name of the selected sub-packages.
        """
        return self._subpackages

    @property
    def plugins(self) -> List[str]:
        """
        Returns:
            The name of the selected plugins.
        """
        return self._plugins

    @property
    def renames(self) -> Dict[str, str]:
        """
        Returns:
            The mapping for renamed plugins (original name -> new name).
        """
        return self._renames

    @property
    def notes(self) -> List[str]:
        """
        Returns:
            The list of notes.
        """
        return self._notes


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
        self._data = data

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
        return self._data.notes

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
        self._plugins = [
            Path(f).name for sp in subpackages for f in sp.files if self._isPlugin(f)
        ]

    # Main method:
    def run(self, script: Union[InputStream, Path, TextIO, str]):
        """
        Run the script from the given input stream.

        Args:
            script: The script to read the script from. Can be a antlr4 stream,
                a path to a script file, a string containing the script or a TextIO
                object.

        Returns:
            The result of running the script.
        """

        # Reset the data:
        self._data = WizardRunnerData()

        # Parse the stream:
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
            for sp in self._subpackages
            for f in sp.files
            if sp in self._data.subpackages and self._isPlugin(f)
        ]

    def selectPlugin(self, plugin_name: str):
        if plugin_name not in self._plugins:
            self.raise_or_warn(
                Issue.SELECT_MISSING_PLUGIN,
                WizardMissingPluginError(self._state.context, plugin_name),
                f"Trying to select plugin '{plugin_name}' that does not exist.",
            )
            return
        self._data.plugins.append(plugin_name)

    def selectSubPackage(self, name: str):

        # Find the package:
        try:
            isp = self._subpackages.index(name)  # type: ignore
        except ValueError:
            self.raise_or_warn(
                Issue.SELECT_MISSING_SUBPACKAGE,
                WizardMissingPackageError(self._state.context, name),
                f"Trying to select sub-package '{name}' that does not exist.",
            )
            return

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
