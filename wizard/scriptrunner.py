# -*- encoding: utf-8 -*-

from enum import Enum, auto
from pathlib import Path
from typing import Optional, TextIO, Tuple, Union

from antlr4 import InputStream

from .contexts import (
    WizardInterpreterContext,
    WizardInterpreterContextFactory,
    WizardSelectManyContext,
    WizardSelectOneContext,
    WizardTerminationContext,
    WizardTopLevelContext,
)
from .functions import make_basic_functions, make_manager_functions
from .interpreter import WizardInterpreter
from .manager import ManagerModInterface, ManagerUserInterface
from .runner import (
    WizardRunnerExpressionVisitor,
    WizardRunnerKeywordVisitor,
    WizardRunnerState,
)
from .severity import SeverityContext
from .value import SubPackages


class WizardScriptRunnerKeywordFactory(WizardRunnerKeywordVisitor):

    """
    Small extension of the runner keyword visitor to call requireVersions()
    on a manager.
    """

    _manager: ManagerUserInterface

    def __init__(
        self,
        manager: ManagerUserInterface,
        subpackages: SubPackages,
        severity: SeverityContext,
    ):
        super().__init__(subpackages, severity)
        self._manager = manager

    def visitRequireVersions(
        self,
        state: WizardRunnerState,
        game_version: str,
        script_extender_version: Optional[str],
        graphics_extender_version: Optional[str],
        wrye_bash_version: Optional[str],
    ):
        self._manager.requiresVersions(
            game_version,
            script_extender_version,
            graphics_extender_version,
            wrye_bash_version,
        )


class WizardScriptRunnerStatus(Enum):

    # A 'Cancel' instruction was encountered:
    CANCEL = auto()

    # A 'Return' instruction was encountered:
    RETURN = auto()

    # The script was completely executed:
    COMPLETE = auto()

    # An error was encountered:
    ERROR = auto()


class WizardScriptRunner(
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
            WizardScriptRunnerKeywordFactory(self, subpackages, self),
            self,
        )

        SeverityContext.__init__(self)
        WizardInterpreter.__init__(self, factory)

    def context(self) -> WizardInterpreterContext:
        return self._ctx

    def abort(self):
        raise WizardScriptRunner.CancelFlow()

    def rewind(self, context: WizardInterpreterContext):
        raise WizardScriptRunner.RewindFlow(context)

    def make_top_level_context(  # type: ignore
        self,
        script: Union[InputStream, Path, TextIO, str],
        state: Optional[WizardRunnerState] = None,
    ) -> WizardTopLevelContext[WizardRunnerState]:
        if state is None:
            state = WizardRunnerState()
        return super().make_top_level_context(script, state)

    def run(
        self, script: Union[InputStream, Path, TextIO, str]
    ) -> Tuple[WizardScriptRunnerStatus, WizardRunnerState]:
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

        # Run the interpret:
        ctx: WizardInterpreterContext = self.make_top_level_context(script)

        while True:

            self._ctx = ctx

            try:
                if isinstance(ctx, WizardSelectOneContext):
                    ctx = ctx.select(
                        self.selectOne(ctx.description, ctx.options, ctx.default)
                    )
                elif isinstance(ctx, WizardSelectManyContext):
                    ctx = ctx.select(
                        self.selectMany(ctx.description, ctx.options, ctx.defaults)
                    )
                elif isinstance(ctx, WizardTerminationContext):
                    if ctx.is_cancel():
                        if self.cancel():
                            return (WizardScriptRunnerStatus.CANCEL, ctx.state)
                    elif ctx.is_return():
                        if self.complete():
                            return (WizardScriptRunnerStatus.RETURN, ctx.state)
                    else:
                        if self.complete():
                            return (WizardScriptRunnerStatus.COMPLETE, ctx.state)

                ctx = ctx.exec()

            except WizardScriptRunner.RewindFlow as rfex:
                ctx = rfex.context

            except WizardScriptRunner.CancelFlow:
                if self.cancel():
                    return (WizardScriptRunnerStatus.CANCEL, ctx.state)

            except Exception as ex:
                self.error(ex)
                return (WizardScriptRunnerStatus.ERROR, ctx.state)

        return (WizardScriptRunnerStatus.COMPLETE, ctx.state)
