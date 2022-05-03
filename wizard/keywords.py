# -*- encoding: utf-8 -*-

from enum import Enum
from typing import Generic, Optional

from .contexts.keywords import WizardKeywordContext
from .severity import SeverityContext
from .state import ContextState


class WizardKeyword(Enum):

    """
    Enumeration representing possible keywords in a Wizard scripts.
    """

    DESELECT_ALL = "DeSelectAll"
    DESELECT_ALL_PLUGINS = "DeSelectAllPlugins"
    DESELECT_PLUGIN = "DeSelectPlugin"
    DESELECT_SUBPACKAGE = "DeSelectSubPackage"
    NOTE = "Note"
    RENAME_PLUGIN = "RenamePlugin"
    REQUIRE_VERSIONS = "RequireVersions"
    RESET_ALL_PLUGIN_NAMES = "ResetAllPluginNames"
    RESET_PLUGIN_NAME = "ResetPluginName"
    SELECT_ALL = "SelectAll"
    SELECT_ALL_PLUGINS = "SelectAllPlugins"
    SELECT_PLUGIN = "SelectPlugin"
    SELECT_SUBPACKAGE = "SelectSubPackage"


class WizardKeywordVisitor(Generic[ContextState]):

    """
    Keyword visitor that can be extended to perform specific actions for
    each keywords. By default, none of the methods do anything.
    """

    _severity: SeverityContext

    def __init__(self, severity: SeverityContext):
        self._severity = severity

    def visitDeSelectAll(self, context: WizardKeywordContext, state: ContextState):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
        """
        ...

    def visitDeSelectAllPlugins(
        self, context: WizardKeywordContext, state: ContextState
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
        """
        ...

    def visitDeSelectPlugin(
        self, context: WizardKeywordContext, state: ContextState, name: str
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            name: The name of the plugin to de-select.
        """
        ...

    def visitDeSelectSubPackage(
        self, context: WizardKeywordContext, state: ContextState, name: str
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            name: The name of the subpackage to de-select.
        """
        ...

    def visitNote(self, context: WizardKeywordContext, state: ContextState, text: str):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            text: The text for the note.
        """
        ...

    def visitRenamePlugin(
        self,
        context: WizardKeywordContext,
        state: ContextState,
        original_name: str,
        new_name: str,
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            original_name: The original name of the plugin.
            new_name: The new name of the plugin.
        """
        ...

    def visitRequireVersions(
        self,
        state: ContextState,
        game_version: str,
        script_extender_version: Optional[str],
        graphics_extender_version: Optional[str],
        wrye_bash_version: Optional[str],
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            game_version: The required game version.
            script_extender_version: The required script extender version.
            graphics_extender_version: The required graphics extender version.
            wrye_bash_version: The required wrye bash version.
        """
        ...

    def visitResetAllPluginNames(
        self, context: WizardKeywordContext, state: ContextState
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
        """
        ...

    def visitResetPluginName(
        self, context: WizardKeywordContext, state: ContextState, name: str
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            name: The original name of the plugin.
        """
        ...

    def visitSelectAll(self, context: WizardKeywordContext, state: ContextState):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
        """
        ...

    def visitSelectAllPlugins(self, context: WizardKeywordContext, state: ContextState):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
        """
        ...

    def visitSelectPlugin(
        self, context: WizardKeywordContext, state: ContextState, name: str
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            name: The name of the plugin to select.
        """
        ...

    def visitSelectSubPackage(
        self, context: WizardKeywordContext, state: ContextState, name: str
    ):
        """
        Args:
            context: The context corresponding to the keyword.
            state: The interpreter state to update.
            name: The name of the subpackage to select.
        """
        ...
