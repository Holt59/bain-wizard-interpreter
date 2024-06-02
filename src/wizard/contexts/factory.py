from __future__ import annotations

import copy
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from antlr4 import ParserRuleContext

from ..antlr4.wizardParser import wizardParser
from ..expr import WizardExpressionVisitor
from ..keywords import WizardKeywordVisitor
from ..manager import SelectOption
from ..severity import SeverityContext
from ..state import ContextState
from .contexts import (
    WizardAssignmentContext,
    WizardBodyContext,
    WizardBreakContext,
    WizardCancelContext,
    WizardCaseContext,
    WizardCompoundAssignmentContext,
    WizardContinueContext,
    WizardExecContext,
    WizardForLoopContext,
    WizardIfContext,
    WizardInterpreterContext,
    WizardReturnContext,
    WizardSelectCasesContext,
    WizardSelectManyContext,
    WizardSelectOneContext,
    WizardTerminationContext,
    WizardWhileLoopContext,
)

RuleContext = TypeVar("RuleContext", bound=ParserRuleContext)
WizardContext = TypeVar("WizardContext", bound=WizardInterpreterContext[Any, Any])

_SelectOneOrManyRuleContext = TypeVar(
    "_SelectOneOrManyRuleContext",
    wizardParser.SelectOneContext,
    wizardParser.SelectManyContext,
)


class WizardInterpreterContextFactory(Generic[ContextState]):
    # The visitors:
    _evisitor: WizardExpressionVisitor
    _kvisitor: WizardKeywordVisitor[ContextState]

    # The severity context:
    _severity: SeverityContext

    def __init__(
        self,
        evisitor: WizardExpressionVisitor,
        kvisitor: WizardKeywordVisitor[ContextState],
        severity: SeverityContext,
    ):
        self._evisitor = evisitor
        self._kvisitor = kvisitor
        self._severity = severity

    @property
    def evisitor(self) -> WizardExpressionVisitor:
        return self._evisitor

    @property
    def kvisitor(self) -> WizardKeywordVisitor[ContextState]:
        return self._kvisitor

    @property
    def severity(self) -> SeverityContext:
        return self._severity

    def copy_context(
        self,
        context: WizardContext,
        state: ContextState | None = None,
    ) -> WizardContext:
        """
        Copy the given context. By default, this method simply calls copy.copy() on
        the context and than state.copy(). This should be  sufficient in most
        cases.

        Args:
            context: The context to copy.
            state: The state to copy into the new context. If None, a copy of the
                context state will be made (see WizardInterpreterState.copy()).

        Returns:
            A copy of this context.
        """
        context = copy.copy(context)
        if state is None:
            context._state = context._state.copy()  # pyright: ignore[reportPrivateUsage]
        else:
            context._state = state.copy()  # pyright: ignore[reportPrivateUsage]
        return context

    def copy_parent(
        self,
        context: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ) -> WizardInterpreterContext[ContextState, Any]:
        """
        Copy the parent of the given context and update its state using either the
        given state or the state of the context.

        Args:
            context: The state to copy the parent from.
            state: The state to copy into the copy of the parent. If None, a copy of
                the context state will be made (see WizardInterpreterState.copy()).

        Returns:
            A copy of the parent of this context.
        """
        if state is None:
            state = context.state
        return self.copy_context(context.parent, state)

    def make_cancel_context(
        self,
        context: wizardParser.CancelStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardCancelContext[ContextState]:
        return WizardCancelContext(self, context, parent)

    def make_return_context(
        self,
        context: wizardParser.ReturnContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardReturnContext[ContextState]:
        return WizardReturnContext(self, context, parent)

    def make_exec_context(
        self,
        context: wizardParser.FunctionCallContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardExecContext[ContextState]:
        return WizardExecContext(self, context, parent)

    def make_body_context(
        self,
        context: wizardParser.BodyContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardBodyContext[ContextState]:
        return WizardBodyContext(self, context, parent)

    def make_assignment_context(
        self,
        context: wizardParser.AssignmentContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardAssignmentContext[ContextState]:
        return WizardAssignmentContext(self, context, parent)

    def make_compound_assignment_context(
        self,
        context: wizardParser.CompoundAssignmentContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardCompoundAssignmentContext[ContextState]:
        return WizardCompoundAssignmentContext(self, context, parent)

    def make_keyword_context(
        self,
        context: wizardParser.KeywordStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardInterpreterContext[ContextState, wizardParser.KeywordStmtContext]:
        from .keywords import make_keyword_context

        return make_keyword_context(self, context, parent)

    def make_break_context(
        self,
        context: wizardParser.BreakContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardBreakContext[ContextState]:
        return WizardBreakContext(self, context, parent)

    def make_continue_context(
        self,
        context: wizardParser.ContinueContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardContinueContext[ContextState]:
        return WizardContinueContext(self, context, parent)

    def make_termination_context(
        self, parent: WizardInterpreterContext[ContextState, Any]
    ) -> WizardTerminationContext[ContextState]:
        return WizardTerminationContext(self, parent.context, parent)

    def make_for_loop_context(
        self,
        context: wizardParser.ForStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardForLoopContext[ContextState]:
        return WizardForLoopContext(self, context, parent)

    def make_while_loop_context(
        self,
        context: wizardParser.WhileStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardWhileLoopContext[ContextState]:
        return WizardWhileLoopContext(self, context, parent)

    def make_if_context(
        self,
        context: wizardParser.IfStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardIfContext[ContextState]:
        return WizardIfContext(self, context, parent)

    def make_select_context(
        self,
        context: wizardParser.SelectStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardSelectOneContext[ContextState] | WizardSelectManyContext[ContextState]:
        if context.selectOne():
            return WizardSelectOneContext(self, context.selectOne(), parent)
        else:
            return WizardSelectManyContext(self, context.selectMany(), parent)

    def make_select_cases_context(
        self,
        options: Sequence[SelectOption],
        context: _SelectOneOrManyRuleContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardSelectCasesContext[ContextState, _SelectOneOrManyRuleContext]:
        return WizardSelectCasesContext(self, options, context, parent)

    def make_case_context(
        self,
        context: wizardParser.CaseStmtContext | wizardParser.DefaultStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ) -> WizardCaseContext[ContextState]:
        return WizardCaseContext(self, context, parent)
