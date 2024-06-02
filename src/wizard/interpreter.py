from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Generic, TextIO, overload

from antlr4 import InputStream

from .contexts import (
    WizardInterpreterContext,
    WizardInterpreterContextFactory,
    WizardTerminationContext,
    WizardTopLevelContext,
)
from .state import ContextState, WizardInterpreterState
from .utils import make_top_level_context


class WizardInterpreter(Generic[ContextState]):
    """
    The WizardInterpreter is the main interpreter for Wizard scripts.
    """

    # The severity context:
    _factory: WizardInterpreterContextFactory[ContextState]

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
    ):
        """
        Args:
            factory: The context factory.
        """
        self._factory = factory

    def exec_until(
        self,
        context: WizardInterpreterContext[ContextState, Any],
        targets: Sequence[type[WizardInterpreterContext[ContextState, Any]]],
    ) -> WizardInterpreterContext[ContextState, Any]:
        """
        Execute the contexts until a context of the given type is found, or
        a termination context is found. If context is one of the given targets,
        the function returns immediately.

        Args:
            context: The start context.
            targets: Target context types. If one of those context is found,
                the process stops.

        Returns:
            The next context (one of the targets or a termination contexts).
        """
        stargets = tuple(targets)

        while not isinstance(context, stargets + (WizardTerminationContext,)):
            context = context.exec()

        return context

    @overload
    def make_top_level_context(
        self, script: InputStream | Path | TextIO | str, state: ContextState
    ) -> WizardTopLevelContext[ContextState]: ...

    @overload
    def make_top_level_context(
        self, script: InputStream | Path | TextIO | str
    ) -> WizardTopLevelContext[WizardInterpreterState]: ...

    def make_top_level_context(
        self,
        script: InputStream | Path | TextIO | str,
        state: ContextState | None = None,
    ) -> (
        WizardTopLevelContext[ContextState]
        | WizardTopLevelContext[WizardInterpreterState]
    ):
        return make_top_level_context(script, self._factory, state)  # type: ignore
