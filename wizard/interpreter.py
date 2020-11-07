# -*- encoding: utf-8 -*-

from typing import Optional

from .antlr4.wizardParser import wizardParser

from .functions import make_basic_functions
from .contexts import (
    WizardInterpreterContextFactory,
    WizardTopLevelContext,
)
from .expr import (
    SubPackages,
    WizardExpressionVisitor,
)
from .keywords import WizardKeywordVisitor
from .severity import SeverityContext
from .state import ContextState, WizardInterpreterState


class WizardInterpreter:

    """
    The WizardInterpreter is the main interpreter for Wizard scripts.
    """

    # The severity context:
    _factory: WizardInterpreterContextFactory

    def __init__(
        self,
        subpackages: SubPackages,
        severity: SeverityContext,
        factory: Optional[WizardInterpreterContextFactory] = None,
    ):
        """
        Args:
            subpackages: The list of SubPackages in the archive.
            severity: The severity context to use for the expression visitor and the
                factory.
            factory: The context factory. If None, a default factory will be used.
        """

        if factory is None:
            evisitor = WizardExpressionVisitor(
                subpackages, make_basic_functions(), severity
            )
            kvisitor: WizardKeywordVisitor[
                WizardInterpreterState
            ] = WizardKeywordVisitor(severity)
            factory = WizardInterpreterContextFactory(evisitor, kvisitor, severity)
        self._factory = factory

    # Main entry:
    def make_context(
        self, ctx: wizardParser.ParseWizardContext, state: Optional[ContextState] = None
    ) -> WizardTopLevelContext[ContextState]:
        if state is None:
            state = WizardInterpreterState()  # type: ignore
        return WizardTopLevelContext(self._factory, ctx, state)  # type: ignore
