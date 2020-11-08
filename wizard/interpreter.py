# -*- encoding: utf-8 -*-

from pathlib import Path
from typing import Optional, Union, TextIO, overload

from antlr4 import InputStream

from .contexts import (
    WizardInterpreterContextFactory,
    WizardTopLevelContext,
)
from .state import ContextState, WizardInterpreterState
from .utils import make_top_level_context


class WizardInterpreter:

    """
    The WizardInterpreter is the main interpreter for Wizard scripts.
    """

    # The severity context:
    _factory: WizardInterpreterContextFactory

    def __init__(
        self,
        factory: WizardInterpreterContextFactory,
    ):
        """
        Args:
            factory: The context factory.
        """
        self._factory = factory

    @overload
    def make_top_level_context(
        self, script: Union[InputStream, Path, TextIO, str], state: ContextState
    ) -> WizardTopLevelContext[ContextState]:
        ...

    @overload
    def make_top_level_context(
        self, script: Union[InputStream, Path, TextIO, str]
    ) -> WizardTopLevelContext[WizardInterpreterState]:
        ...

    def make_top_level_context(
        self,
        script: Union[InputStream, Path, TextIO, str],
        state: Optional[ContextState] = None,
    ) -> Union[
        WizardTopLevelContext[ContextState],
        WizardTopLevelContext[WizardInterpreterState],
    ]:
        return make_top_level_context(script, self._factory, state)  # type: ignore
