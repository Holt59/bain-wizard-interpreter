# -*- encoding: utf-8 -*-

import copy
from typing import List, Optional, TypeVar, Union

from ..antlr4.wizardParser import wizardParser
from ..expr import WizardExpressionVisitor
from ..keywords import WizardKeywordVisitor
from ..manager import SelectOption
from ..severity import SeverityContext
from ..state import WizardInterpreterState
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
    WizardSelectContext,
    WizardSelectManyContext,
    WizardSelectOneContext,
    WizardTerminationContext,
    WizardWhileLoopContext,
)
from .keywords import WizardKeywordContext, make_keyword_context

WizardContext = TypeVar("WizardContext", bound=WizardInterpreterContext)


class WizardInterpreterContextFactory:

    # The visitors:
    _evisitor: WizardExpressionVisitor
    _kvisitor: WizardKeywordVisitor

    # The severity context:
    _severity: SeverityContext

    def __init__(
        self,
        evisitor: WizardExpressionVisitor,
        kvisitor: WizardKeywordVisitor,
        severity: SeverityContext,
    ):
        self._evisitor = evisitor
        self._kvisitor = kvisitor
        self._severity = severity

    @property
    def evisitor(self) -> WizardExpressionVisitor:
        return self._evisitor

    @property
    def kvisitor(self) -> WizardKeywordVisitor:
        return self._kvisitor

    @property
    def severity(self) -> SeverityContext:
        return self._severity

    def _copy_context(
        self,
        context: WizardContext,
        state: Optional[WizardInterpreterState] = None,
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
            context._state = context._state.copy()
        else:
            context._state = state.copy()
        return context

    def _copy_parent(
        self,
        context: WizardInterpreterContext,
        state: Optional[WizardInterpreterState] = None,
    ) -> "WizardInterpreterContext":
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
        return self._copy_context(context.parent, state)

    def make_cancel_context(
        self, context: wizardParser.CancelContext, parent: WizardInterpreterContext
    ) -> WizardCancelContext:
        return WizardCancelContext(self, context, parent)

    def make_return_context(
        self, context: wizardParser.CancelContext, parent: WizardInterpreterContext
    ) -> WizardReturnContext:
        return WizardReturnContext(self, context, parent)

    def make_exec_context(
        self,
        context: wizardParser.FunctionCallContext,
        parent: WizardInterpreterContext,
    ) -> WizardExecContext:
        return WizardExecContext(self, context, parent)

    def make_body_context(
        self,
        context: wizardParser.BodyContext,
        parent: WizardInterpreterContext,
    ) -> WizardBodyContext:
        return WizardBodyContext(self, context, parent)

    def make_assignment_context(
        self,
        context: wizardParser.AssignmentContext,
        parent: WizardInterpreterContext,
    ) -> WizardAssignmentContext:
        return WizardAssignmentContext(self, context, parent)

    def make_compound_assignment_context(
        self,
        context: wizardParser.CompoundAssignmentContext,
        parent: WizardInterpreterContext,
    ) -> WizardCompoundAssignmentContext:
        return WizardCompoundAssignmentContext(self, context, parent)

    def make_keyword_context(
        self,
        context: wizardParser.KeywordStmtContext,
        parent: WizardInterpreterContext,
    ) -> WizardKeywordContext:
        return make_keyword_context(self, context, parent)

    def make_break_context(
        self, context: wizardParser.BreakContext, parent: WizardInterpreterContext
    ) -> WizardBreakContext:
        return WizardBreakContext(self, context, parent)

    def make_continue_context(
        self, context: wizardParser.BreakContext, parent: WizardInterpreterContext
    ) -> WizardContinueContext:
        return WizardContinueContext(self, context, parent)

    def make_termination_context(
        self, parent: WizardInterpreterContext
    ) -> WizardTerminationContext:
        return WizardTerminationContext(self, parent.context, parent)

    def make_for_loop_context(
        self, context: wizardParser.ForStmtContext, parent: WizardInterpreterContext
    ) -> WizardForLoopContext:
        return WizardForLoopContext(self, context, parent)

    def make_while_loop_context(
        self, context: wizardParser.WhileStmtContext, parent: WizardInterpreterContext
    ) -> WizardWhileLoopContext:
        return WizardWhileLoopContext(self, context, parent)

    def make_if_context(
        self, context: wizardParser.IfStmtContext, parent: WizardInterpreterContext
    ) -> WizardIfContext:
        return WizardIfContext(self, context, parent)

    def make_select_context(
        self,
        context: wizardParser.SelectStmtContext,
        parent: WizardInterpreterContext,
    ) -> WizardSelectContext:
        if context.selectOne():
            return WizardSelectOneContext(self, context.selectOne(), parent)
        else:
            return WizardSelectManyContext(self, context.selectMany(), parent)

    def make_select_cases_context(
        self,
        options: List[SelectOption],
        context: wizardParser.SelectStmtContext,
        parent: WizardInterpreterContext,
    ) -> WizardSelectCasesContext:
        return WizardSelectCasesContext(self, options, context, parent)

    def make_case_context(
        self,
        context: Union[wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext],
        parent: WizardInterpreterContext,
    ) -> WizardCaseContext:
        return WizardCaseContext(self, context, parent)
