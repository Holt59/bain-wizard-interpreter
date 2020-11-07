# -*- encoding: utf-8 -*-

from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Mapping,
    MutableMapping,
    List,
    Optional,
    Sequence,
)

from .contexts import WizardKeywordContext
from .errors import WizardMissingPackageError, WizardMissingPluginError
from .expr import WizardExpressionVisitor
from .inisettings import WizardINISetting, WizardINISettingEdit, WizardINITweaks
from .keywords import WizardKeywordVisitor
from .severity import Issue, SeverityContext
from .state import WizardInterpreterState
from .value import SubPackages


class WizardRunnerState(WizardInterpreterState):

    """
    Wrapper around multiple containers that are updated during the execution
    of a Wizard script and need to be rewound.
    """

    # The list of selected subpackages and plugins:
    _subpackages: List[str]
    _plugins: List[str]

    # Renaming of plugins (original name -> new name):
    _renames: MutableMapping[str, str]

    # The INI tweaks (disabled and modified settings):
    _tweaks: WizardINITweaks

    # The list of notes:
    _notes: List[str]

    def __init__(self):
        super().__init__()
        self._subpackages = []
        self._plugins = []
        self._renames = {}
        self._tweaks = WizardINITweaks()
        self._notes = []

    def copy(self) -> "WizardRunnerState":
        state: WizardRunnerState = super().copy()  # type: ignore
        state._subpackages.extend(self._subpackages)
        state._plugins.extend(self._plugins)
        state._renames.update(self._renames)
        state._notes.extend(self._notes)
        state._tweaks._disabled.extend(self.tweaks.disabled)
        state._tweaks._modified.extend(self.tweaks.modified)
        return state

    @property
    def subpackages(self) -> Sequence[str]:
        """
        Returns:
            The name of the selected sub-packages (sorted).
        """
        return sorted(self._subpackages)

    @property
    def plugins(self) -> Sequence[str]:
        """
        Returns:
            The name of the selected plugins (sorted).
        """
        return sorted(self._plugins)

    @property
    def renames(self) -> Mapping[str, str]:
        """
        Returns:
            The mapping for renamed plugins (original name -> new name).
        """
        return self._renames

    @property
    def tweaks(self) -> WizardINITweaks:
        """
        Returns:
            The INI tweaks created by the script (disabled, new or
            modified settings).
        """
        return self._tweaks

    @property
    def notes(self) -> Sequence[str]:
        """
        Returns:
            The list of notes.
        """
        return self._notes


class WizardRunnerExpressionVisitor(WizardExpressionVisitor):

    """
    Simple extension of the expression visitor to update INI tweaks.
    """

    def visitDisableINILine(
        self, state: WizardInterpreterState, filename: str, section: str, setting: str
    ):
        """
        Create an INI tweak file that disables the specified setting by commenting it
        out. Otherwise, behaves identically to editINI.

        Args:
            filename: The name of the INI file to edit, relative to the Data directory.
            section: The section in the INI where setting resides.
            setting: The setting to disable.
        """
        assert isinstance(state, WizardRunnerState)
        state.tweaks._disabled.append(WizardINISetting(filename, section, setting))

    def visitEditINI(
        self,
        state: WizardInterpreterState,
        filename: str,
        section: str,
        setting: str,
        value: Any,
        comment: Optional[str] = "",
    ):
        """
        Create an INI tweak file with some tweaks in it. If file that to apply the
        tweak to is from the current installer or is the game's ini file, then the
        tweaks are also applied, otherwise, it will just be generated for the user
        to apply manually.

        Args:
            filename: The name of the INI file to edit, relative to the Data directory.
            section: The section in the INI where setting resides.
            setting: The setting to set.
            value: The value to set the setting to.
            comment: An optional comment to add.
        """
        assert isinstance(state, WizardRunnerState)
        state.tweaks._modified.append(
            WizardINISettingEdit(filename, section, setting, value, comment)
        )


class WizardRunnerKeywordVisitor(WizardKeywordVisitor):

    _subpackages: SubPackages
    _plugins: List[str]

    def __init__(self, subpackages: SubPackages, severity: SeverityContext):
        super().__init__(severity)
        self._subpackages = subpackages
        self._plugins = [
            Path(f).name
            for sp in self._subpackages
            for f in sp.files
            if self._isPlugin(f)
        ]

    def _isPlugin(self, name: str) -> bool:
        """
        Check if the given name corresponds to a plugin.

        Args:
            name: The name of the file.

        Returns:
            True if the name corresponds to a plugin, False otherwise.
        """
        return name.endswith(".esp") or name.endswith(".esm") or name.endswith(".esl")

    def visitDeSelectAll(self, context: WizardKeywordContext, state: WizardRunnerState):
        state._subpackages.clear()
        state._plugins.clear()

    def visitDeSelectAllPlugins(
        self, context: WizardKeywordContext, state: WizardRunnerState
    ):
        """
        Args:
            state: The interpreter state to update.
        """
        state._plugins.clear()

    def visitDeSelectPlugin(
        self, context: WizardKeywordContext, state: WizardRunnerState, name: str
    ):
        """
        Args:
            state: The interpreter state to update.
            name: The name of the plugin to de-select.
        """
        if name in state._plugins:
            state._plugins.remove(name)

    def visitDeSelectSubPackage(
        self, context: WizardKeywordContext, state: WizardRunnerState, name: str
    ):
        """
        Args:
            state: The interpreter state to update.
            name: The name of the subpackage to de-select.
        """
        if name in state._subpackages:
            state._subpackages.remove(name)

    def visitNote(
        self, context: WizardKeywordContext, state: WizardRunnerState, text: str
    ):
        """
        Args:
            state: The interpreter state to update.
            text: The text for the note.
        """
        state._notes.append(text)

    def visitRenamePlugin(
        self,
        context: WizardKeywordContext,
        state: WizardRunnerState,
        original_name: str,
        new_name: str,
    ):
        """
        Args:
            state: The interpreter state to update.
            original_name: The original name of the plugin.
            new_name: The new name of the plugin.
        """
        state._renames[original_name] = new_name

    def visitRequireVersions(
        self,
        state: WizardRunnerState,
        game_version: str,
        script_extender_version: Optional[str],
        graphics_extender_version: Optional[str],
        wrye_bash_version: Optional[str],
    ):
        """
        Args:
            state: The interpreter state to update.
            game_version: The required game version.
            script_extender_version: The required script extender version.
            graphics_extender_version: The required graphics extender version.
            wrye_bash_version: The required wrye bash version.
        """
        ...

    def visitResetAllPluginNames(
        self, context: WizardKeywordContext, state: WizardRunnerState
    ):
        """
        Args:
            state: The interpreter state to update.
        """
        state._renames.clear()

    def visitResetPluginName(
        self, context: WizardKeywordContext, state: WizardRunnerState, name: str
    ):
        """
        Args:
            state: The interpreter state to update.
            name: The original name of the plugin.
        """
        if name in state._renames:
            del state._renames[name]

    def visitSelectAll(self, context: WizardKeywordContext, state: WizardRunnerState):
        """
        Args:
            state: The interpreter state to update.
        """
        state._subpackages = [str(sp) for sp in self._subpackages]
        self.visitSelectAllPlugins(context, state)

    def visitSelectAllPlugins(
        self, context: WizardKeywordContext, state: WizardRunnerState
    ):
        """
        Args:
            state: The interpreter state to update.
        """
        # Guess we only select plugins from selected subpackages?
        state._plugins = [
            Path(f).name
            for sp in self._subpackages
            for f in sp.files
            if sp in state._subpackages and self._isPlugin(f)
        ]

    def visitSelectPlugin(
        self, context: WizardKeywordContext, state: WizardRunnerState, name: str
    ):
        """
        Args:
            state: The interpreter state to update.
            name: The name of the plugin to select.
        """
        if name not in self._plugins:
            self._severity.raise_or_warn(
                Issue.SELECT_MISSING_PLUGIN,
                WizardMissingPluginError(context.context, name),
                f"Trying to select plugin '{name}' that does not exist.",
            )
            return
        state._plugins.append(name)

    def visitSelectSubPackage(
        self, context: WizardKeywordContext, state: WizardRunnerState, name: str
    ):
        """
        Args:
            state: The interpreter state to update.
            name: The name of the subpackage to select.
        """

        # Find the package:
        try:
            isp = self._subpackages.index(name)  # type: ignore
        except ValueError:
            self._severity.raise_or_warn(
                Issue.SELECT_MISSING_SUBPACKAGE,
                WizardMissingPackageError(context.context, name),
                f"Trying to select sub-package '{name}' that does not exist.",
            )
            return

        subpackage = self._subpackages[isp]

        state._subpackages.append(name)

        # Auto-select plugins?
        for f in subpackage.files:
            if self._isPlugin(f):
                self.visitSelectPlugin(context, state, Path(f).name)
