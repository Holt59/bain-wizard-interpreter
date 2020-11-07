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
    TextIO,
    Tuple,
    Union,
)

from antlr4 import InputStream, FileStream, CommonTokenStream, BailErrorStrategy

from .antlr4.wizardLexer import wizardLexer
from .antlr4.wizardParser import wizardParser

from .contexts import (
    WizardKeywordContext,
    WizardInterpreterContext,
    WizardInterpreterContextFactory,
    WizardSelectContext,
    WizardTerminationContext,
)
from .errors import WizardMissingPackageError, WizardMissingPluginError
from .expr import WizardExpressionVisitor
from .functions import make_basic_functions, make_manager_functions
from .interpreter import WizardInterpreter
from .inisettings import WizardINISetting, WizardINISettingEdit, WizardINITweaks
from .keywords import WizardKeywordVisitor
from .manager import ManagerModInterface, ManagerUserInterface
from .severity import Issue, SeverityContext
from .state import WizardInterpreterState
from .value import SubPackages


class WizardRunnerResult(Enum):

    # A 'Cancel' instruction was encountered:
    CANCEL = auto()

    # A 'Return' instruction was encountered:
    RETURN = auto()

    # The script was completely executed:
    COMPLETE = auto()

    # An error was encountered:
    ERROR = auto()


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


class WizardRunner(
    WizardInterpreter, ManagerModInterface, ManagerUserInterface, SeverityContext
):

    """
    The WizardRunner is a high-level interface for the interpreter that
    uses callbacks to interact with the user.

    Implementations should inherit the WizardRunner class and implements
    missing methods from the manager interfaces.
    """

    # Internal exceptions used to rewind / cancel at any point:
    class RewindFlow(Exception):

        """
        Exception used to rewind a script execution when calling rewind().
        """

        context: WizardInterpreterContext

        def __init__(self, context: WizardInterpreterContext):
            self.context = context

    class CancelFlow(Exception):

        """
        Exception used to cancel a script execution when calling abort().
        """

        ...

    # The current context:
    _ctx: WizardInterpreterContext

    def __init__(self, subpackages: SubPackages = SubPackages()):
        functions = make_basic_functions()
        functions.update(make_manager_functions(self, self))

        factory = WizardInterpreterContextFactory(
            WizardRunnerExpressionVisitor(subpackages, functions, self),
            WizardRunnerKeywordVisitor(subpackages, self),
            self,
        )

        SeverityContext.__init__(self)
        WizardInterpreter.__init__(self, subpackages, self, factory)

    def context(self) -> WizardInterpreterContext:
        return self._ctx

    def abort(self):
        raise WizardRunner.CancelFlow()

    def rewind(self, context: WizardInterpreterContext):
        raise WizardRunner.RewindFlow(context)

    def run(
        self, script: Union[InputStream, Path, TextIO, str]
    ) -> Tuple[WizardRunnerResult, WizardRunnerState]:
        """
        Run the script from the given input stream.

        Args:
            script: The script to read the script from. Can be a antlr4 stream,
                a path to a script file, a string containing the script or a TextIO
                object.

        Returns:
            A tuple (result, state) from running the script where state is the last
            state of the interpreter and result the result.
        """

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
        ctx: WizardInterpreterContext = self.make_context(
            parser.parseWizard(), WizardRunnerState()
        )

        while True:

            self._ctx = ctx

            try:
                if isinstance(ctx, WizardSelectContext):

                    if ctx.is_many():
                        ctx = ctx.select(
                            self.selectMany(ctx.description, ctx.options, ctx.defaults)
                        )
                    else:
                        ctx = ctx.select(
                            [
                                self.selectOne(
                                    ctx.description, ctx.options, ctx.defaults[0]
                                )
                            ]
                        )
                elif isinstance(ctx, WizardTerminationContext):
                    if ctx.is_cancel():
                        if self.cancel():
                            return (WizardRunnerResult.CANCEL, ctx.state)
                    elif ctx.is_return():
                        if self.complete():
                            return (WizardRunnerResult.RETURN, ctx.state)
                    else:
                        if self.complete():
                            return (WizardRunnerResult.COMPLETE, ctx.state)

                ctx = ctx.exec()

            except WizardRunner.RewindFlow as rfex:
                ctx = rfex.context

            except WizardRunner.CancelFlow:
                if self.cancel():
                    return (WizardRunnerResult.CANCEL, ctx.state)

            except Exception as ex:
                self.error(ex)
                return (WizardRunnerResult.ERROR, ctx.state)

        return (WizardRunnerResult.COMPLETE, ctx.state)
