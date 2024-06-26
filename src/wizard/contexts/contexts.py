"""
This file contains "context" which are used to rewind the
interpreter.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Callable, Generic, Self, TypeVar

from antlr4 import ParserRuleContext

from ..antlr4.wizardParser import wizardParser
from ..errors import WizardError, WizardNameError, WizardParseError, WizardTypeError
from ..manager import SelectOption
from ..severity import Issue
from ..state import ContextState
from ..value import SubPackage, SubPackages, Value
from .utils import wrap_exceptions

if TYPE_CHECKING:
    from .factory import WizardInterpreterContextFactory


RuleContext = TypeVar("RuleContext", bound=ParserRuleContext)


class WizardInterpreterContext(Generic[ContextState, RuleContext]):
    """
    The base context class. The context are represented by a tree, where each
    child has access to his parent. Unlike ANTLR4 context, not all rules or
    elements in the grammer creates a context.
    """

    # The interpreter:
    _factory: WizardInterpreterContextFactory[ContextState]

    # The ANTLR4 context:
    _context: RuleContext

    # The parent context:
    _parent: WizardInterpreterContext[ContextState, Any]

    # The state of this context:
    _state: ContextState

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: RuleContext,
        parent: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ):
        """
        Args:
            factory: The context factory.
            context: The ANTLR4 context.
            parent: The parent context.
            state: The state for this context. If None, a copy of the
                parent state will be made.
        """
        self._factory = factory
        self._context = context
        self._parent = parent

        if state is None:
            self._state = parent.state.copy()  # type: ignore
        else:
            self._state = state

    def is_top_level(self) -> bool:
        """
        Returns:
            True if this context is top-level (no parent), False otherwise.
        """
        return self is self.parent

    @property
    def factory(self) -> WizardInterpreterContextFactory[ContextState]:
        """
        Returns:
            The factory associated with this context.
        """
        return self._factory

    @property
    def parent(self) -> WizardInterpreterContext[ContextState, Any]:
        """
        Returns:
            The parent context.
        """
        return self._parent

    @property
    def context(self) -> RuleContext:
        """
        Returns:
            The ANTLR4 context associated with this interpreter context.
        """
        return self._context

    @property
    def state(self) -> ContextState:
        """
        Returns:
            The state before the execution of this context.
        """
        return self._state

    @abstractmethod
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        """
        Execute the next 'step' of this context and returns the next context
        to execute. When done, should return the parent context.

        This method should be implement by all sub-classes representing specific
        contexts.
        """
        pass

    def exec(self) -> WizardInterpreterContext[ContextState, Any]:
        """
        Execute the next 'step' of this context and returns the next context
        to execute. When done, should return the parent context.
        """
        if self.context.exception:
            raise WizardParseError(self.context, self.context.exception)
        return wrap_exceptions(self.exec_, self.context)


class WizardBreakableContext(Generic[ContextState]):
    """
    Context that can be broken by a 'Break' expression.
    """

    @abstractmethod
    def break_(self) -> WizardInterpreterContext[ContextState, Any]:
        """
        Called when a 'Break' instruction is encountered, should usually return
        the parent.

        Returns:
            The next context to use after this break.
        """
        pass


class WizardContinuableContext(Generic[ContextState]):
    """
    Context that can be broken by a 'Continue' expression.
    """

    @abstractmethod
    def continue_(self) -> WizardInterpreterContext[ContextState, Any]:
        """
        Called when a 'Continue' instruction is encountered, should usually return
        the context itself.

        Returns:
            The next context to use after this continue.
        """
        pass


class WizardTerminationContext(
    WizardInterpreterContext[ContextState, wizardParser.ParseWizardContext]
):
    """
    Special context returned at the end of the execution. You can check what caused
    the termination using the `is_cancel`, `is_return` and `is_complete` method. If you
    want to check for "normal" completion, you can check for `not is_return()`.
    """

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        raise NotImplementedError("exec() should not be called on termination context.")

    def is_cancel(self) -> bool:
        """
        Returns:
            True if this termination was caused by a 'Cancel' keyword.
        """
        return isinstance(self.parent, WizardCancelContext)

    def message(self) -> str | None:
        """
        Returns:
            The cancel message, if any. If `is_cancel()` is False, this returns None.
        """
        if not isinstance(self.parent, WizardCancelContext):
            return None
        return self.parent.message()

    def is_return(self) -> bool:
        """
        Returns:
            True if this termination was caused by a 'Return' keyword.
        """
        return isinstance(self.parent, WizardReturnContext)

    def is_complete(self) -> bool:
        """
        Returns:
            True if this termination was caused by the end of the script.
        """
        return not isinstance(self.parent, (WizardCancelContext, WizardReturnContext))


class WizardTopLevelContext(
    WizardInterpreterContext[ContextState, wizardParser.ParseWizardContext]
):
    """
    Special context to be the entry context point.
    """

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.ParseWizardContext,
        parent: WizardInterpreterContext[ContextState, Any] | None,
        state: ContextState | None = None,
    ):
        """
        Args:
            factory: The factory used to create this context and future contexts.
            context: The ANTLR4 context.
            state: The starting state for this context.
            parent: If not None, it means that this context was created from an Exec()
                expression and the parent should be the enclosing body.
        """
        super().__init__(factory, context, self if parent is None else parent, state)

    def exec_(self) -> WizardBodyContext[ContextState]:
        # We forward the parent, which is either self (no parent) or the parent body
        # for Exec().
        return self._factory.make_body_context(self.context.body(), self.parent)


class WizardCancelContext(
    WizardInterpreterContext[ContextState, wizardParser.CancelStmtContext]
):
    """
    Special context that is returned when a 'Cancel' instruction is encountered.
    """

    # The cancel message:
    _message: str | None

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.CancelStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ):
        super().__init__(factory, context, parent, state)

        self._message = None
        if self.context.expr():
            self._message = self._factory.evisitor.visitExpr(
                self.context.expr(), self.state, str
            ).value

    def message(self) -> str | None:
        """
        Returns:
            The cancel message, if any.
        """
        return self._message

    def exec_(self) -> WizardTerminationContext[ContextState]:
        return self._factory.make_termination_context(self)


class WizardReturnContext(
    WizardInterpreterContext[ContextState, wizardParser.ReturnContext]
):
    """
    Special context that is returned when a 'Return' instruction is encountered.
    """

    def exec_(self) -> WizardTerminationContext[ContextState]:
        return self._factory.make_termination_context(self)


class WizardBodyContext(
    WizardInterpreterContext[ContextState, wizardParser.BodyContext]
):
    """
    Body context.
    """

    # Index of the next child to process.
    _ichild: int

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.BodyContext,
        parent: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ):
        super().__init__(factory, context, parent, state)

        self._ichild = 0

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # Empty block or no more children:
        if not self._context.children or self._ichild == len(self._context.children):
            if isinstance(self._parent, WizardTopLevelContext):
                return self._factory.make_termination_context(self)
            return self._factory.copy_parent(self)

        child = self._context.children[self._ichild]

        # Copy the body and increment the child counter:
        body = self._factory.copy_context(self)
        body._ichild += 1

        # Expression - Standard context:
        if isinstance(child, wizardParser.ExprContext):
            # Specific handling of exec()
            if (
                isinstance(child, wizardParser.FunctionCallContext)
                and child.Identifier().getText() == "Exec"
            ):
                return self._factory.make_exec_context(child, body)

            self._factory.evisitor.visitExpr(child, body.state)
            return body

        if isinstance(child, wizardParser.StmtContext):
            if child.assignment():
                return self._factory.make_assignment_context(child.assignment(), body)
            elif child.compoundAssignment():
                return self._factory.make_compound_assignment_context(
                    child.compoundAssignment(), body
                )
            elif child.controlFlowStmt():
                return self._make_control_flow_context(child.controlFlowStmt(), body)
            elif child.keywordStmt():
                return self._factory.make_keyword_context(child.keywordStmt(), body)

        raise WizardParseError(child, f"Unknown context in body: {child}.")

    def _make_control_flow_context(
        self,
        ctx: wizardParser.ControlFlowStmtContext,
        parent: WizardBodyContext[ContextState],
    ) -> WizardInterpreterContext[ContextState, Any]:
        if isinstance(ctx, wizardParser.ForContext):
            return self._factory.make_for_loop_context(ctx.forStmt(), parent)
        elif isinstance(ctx, wizardParser.WhileContext):
            return self._factory.make_while_loop_context(ctx.whileStmt(), parent)
        elif isinstance(ctx, wizardParser.IfContext):
            return self._factory.make_if_context(ctx.ifStmt(), parent)
        elif isinstance(ctx, wizardParser.SelectContext):
            return self._factory.make_select_context(ctx.selectStmt(), parent)
        elif isinstance(ctx, wizardParser.BreakContext):
            return self._factory.make_break_context(ctx, parent)
        elif isinstance(ctx, wizardParser.ContinueContext):
            return self._factory.make_continue_context(ctx, parent)
        elif isinstance(ctx, wizardParser.CancelContext):
            return self._factory.make_cancel_context(ctx.cancelStmt(), parent)
        elif isinstance(ctx, wizardParser.ReturnContext):
            return self._factory.make_return_context(ctx, parent)

        raise WizardParseError(ctx, f"Unknown control flow statement: {ctx}.")


class WizardBreakContext(
    WizardInterpreterContext[ContextState, wizardParser.BreakContext]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # Find the first loop or case:
        loop_or_case: WizardInterpreterContext[ContextState, Any] = self

        while not loop_or_case.is_top_level() and not isinstance(
            loop_or_case, WizardBreakableContext
        ):
            loop_or_case = loop_or_case.parent

        if not isinstance(loop_or_case, WizardBreakableContext):
            raise WizardParseError(
                self.context, "Invalid 'Break' statement encountered."
            )

        context: WizardInterpreterContext[ContextState, Any] = loop_or_case.break_()
        return self._factory.copy_context(context, self.state)


class WizardContinueContext(
    WizardInterpreterContext[ContextState, wizardParser.ContinueContext]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # Find the first parent loop:
        loop: WizardInterpreterContext[ContextState, Any] = self

        while loop.is_top_level() and not isinstance(loop, WizardContinuableContext):
            loop = loop.parent

        if not isinstance(loop, WizardContinuableContext):
            raise WizardParseError(
                self.context, "Invalid 'Continue' statement encountered."
            )

        context: WizardInterpreterContext[ContextState, Any] = loop.continue_()
        return self._factory.copy_context(context, self.state)


class WizardExecContext(
    WizardInterpreterContext[ContextState, wizardParser.FunctionCallContext]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # import here otherwise we have circular imports
        from ..utils import make_parse_wizard_context

        state = self.state.copy()

        # Parse the expression:
        args = list(self.context.argList().expr())
        if len(args) != 1:
            raise WizardTypeError(
                self.context, f"Exec() expect exactly one argument, found {len(args)}."
            )
        script = self._factory.evisitor.visitExpr(args[0], state, str).value

        try:
            context = make_parse_wizard_context(script)
        except WizardError as we:
            # If an error occurs, the WizardError does not have a context, set it:
            we._ctx = self.context  # type: ignore
            raise we

        return WizardTopLevelContext(self._factory, context, self.parent, state)


class WizardIfContext(
    WizardInterpreterContext[ContextState, wizardParser.IfStmtContext]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        parent = self._factory.copy_parent(self)

        if self._factory.evisitor.visitExpr(self.context.expr(), parent.state):
            return self._factory.make_body_context(self.context.body(), parent)
        else:
            for eifc in self.context.elifStmt():
                if self._factory.evisitor.visitExpr(eifc.expr(), parent.state):
                    return self._factory.make_body_context(eifc.body(), parent)

            if self.context.elseStmt():
                return self._factory.make_body_context(
                    self.context.elseStmt().body(),
                    parent,
                )

        return parent


class WizardForLoopContext(
    WizardInterpreterContext[ContextState, wizardParser.ForStmtContext],
    WizardBreakableContext[ContextState],
    WizardContinuableContext[ContextState],
):
    """
    For-loop context.
    """

    # Name of the loop variable, sequence of values and current index:
    _name: str
    _values: Sequence[Value[Any]]
    _index: int

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.ForStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ):
        super().__init__(factory, context, parent, state)

        if self.context.forInHeader():
            self._values = self._for_in_header(self.context.forInHeader())
        else:
            self._values = self._for_range_header(self.context.forRangeHeader())

        self._name = self.context.Identifier().getText()
        self._index = 0

    def break_(self) -> WizardInterpreterContext[ContextState, Any]:
        return self._factory.copy_parent(self)

    def continue_(self) -> WizardInterpreterContext[ContextState, Any]:
        return self

    def _for_range_header(
        self, ctx: wizardParser.ForRangeHeaderContext
    ) -> Sequence[Value[Any]]:
        sta: Value[int] = self._factory.evisitor.visitExpr(ctx.expr(0), self.state, int)
        end: Value[int] = self._factory.evisitor.visitExpr(ctx.expr(1), self.state, int)

        if e2 := ctx.expr(2):
            by = self._factory.evisitor.visitExpr(e2, self.state, int)
        else:
            by = Value(1)

        return [Value(i) for i in range(sta.value, end.value + 1, by.value)]

    def _for_in_header(
        self, ctx: wizardParser.ForInHeaderContext
    ) -> Sequence[Value[Any]]:
        value = self._factory.evisitor.visitExpr(ctx.expr(), self.state)

        if isinstance(value.value, SubPackage):
            return [Value(f) for f in value.value.files]
        elif isinstance(value.value, SubPackages):
            return [Value(sp) for sp in value.value]
        elif isinstance(value.value, str):
            # TODO: Allow?
            return [Value(s) for s in value.value]
        else:
            raise WizardTypeError(
                ctx, f"Cannot iterable over value of type {value.type}."
            )

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # End of the loop:
        if self._index == len(self._values):
            return self._factory.copy_parent(self)

        # Retrieve the next value and set it:
        value = self._values[self._index]

        # Copy the context:
        loop = self._factory.copy_context(self)
        loop._index += 1

        loop.state.set(self._name, value)

        # Return a body context:
        return self._factory.make_body_context(self.context.body(), loop)


class WizardWhileLoopContext(
    WizardInterpreterContext[ContextState, wizardParser.WhileStmtContext],
    WizardBreakableContext[ContextState],
    WizardContinuableContext[ContextState],
):
    def break_(self) -> WizardInterpreterContext[ContextState, Any]:
        return self._factory.copy_parent(self)

    def continue_(self) -> WizardInterpreterContext[ContextState, Any]:
        return self

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        loop = self._factory.copy_context(self)

        # If the expression evaluates to True, we return a body context:
        if self._factory.evisitor.visitExpr(self.context.expr(), loop.state):
            return self._factory.make_body_context(self.context.body(), loop)

        # Otherwise we return the parent (after updating the variables):
        return self._factory.copy_parent(loop)


class WizardAssignmentContext(
    WizardInterpreterContext[
        ContextState,
        wizardParser.AssignmentContext,
    ]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        parent = self._factory.copy_parent(self)

        # Retrieve the name:
        name: str = self.context.Identifier().getText()

        # Evaluate the expression:
        value: Value[Any] = self._factory.evisitor.visitExpr(
            self.context.expr(), parent.state
        )

        parent.state.set(name, value)

        return parent


class WizardCompoundAssignmentContext(
    WizardInterpreterContext[
        ContextState,
        wizardParser.CompoundAssignmentContext,
    ]
):
    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        parent = self._factory.copy_parent(self)

        # Retrieve the name:
        name: str = self.context.Identifier().getText()

        # Evaluate the expression:
        value: Value[Any] = self._factory.evisitor.visitExpr(
            self.context.expr(), parent.state
        )

        if name not in parent.state.variables:
            raise WizardNameError(self.context, name)

        op: Callable[[Value[Any], Value[Any]], Value[Any]]
        if self.context.CompoundExp():
            op = Value.__pow__
        elif self.context.CompoundMul():
            op = Value.__mul__
        elif self.context.CompoundDiv():
            op = Value.__div__
        elif self.context.CompoundMod():
            op = Value.__mod__
        elif self.context.CompoundAdd():
            op = Value.__add__
        elif self.context.CompoundSub():
            op = Value.__sub__
        else:
            raise WizardParseError(
                self.context, f"Unknown compound operation: {self.context}."
            )

        try:
            value = op(parent.state.variables[name], value)
        except TypeError as te:
            raise WizardTypeError(self.context, str(te)) from te

        parent.state.set(name, value)

        return parent


def parse_select_options(
    factory: WizardInterpreterContextFactory[ContextState],
    context: wizardParser.SelectOneContext | wizardParser.SelectManyContext,
    state: ContextState,
) -> tuple[str, list[SelectOption], list[SelectOption]]:
    # Parse the description and option:
    description = factory.evisitor.visitExpr(context.expr(), state, str).value

    options: list[SelectOption] = []
    defaults: list[SelectOption] = []
    for opt in context.optionTuple():
        a, b, c = (
            factory.evisitor.visitExpr(opt.expr(0), state, str),
            factory.evisitor.visitExpr(opt.expr(1), state, str),
            factory.evisitor.visitExpr(opt.expr(2), state, str),
        )

        name = a.value
        isdef = False
        if name.startswith("|"):
            name = name[1:]
            isdef = True

        options.append(
            SelectOption(name, b.value, c.value if c.value.strip() else None)
        )

        # Add to defaults:
        if isdef:
            defaults.append(options[-1])

    # Not default in SelectOne -> Select first one.
    if not isinstance(context, wizardParser.SelectManyContext) and not defaults:
        defaults.append(options[0])

    return description, options, defaults


_SelectOneOrManyRuleContext = TypeVar(
    "_SelectOneOrManyRuleContext",
    wizardParser.SelectOneContext,
    wizardParser.SelectManyContext,
)


class WizardSelectContext(
    WizardInterpreterContext[ContextState, _SelectOneOrManyRuleContext]
):
    # The description:
    _description: str

    # The list of options:
    _options: list[SelectOption]

    # The default option(s):
    _default: list[SelectOption]

    # The selected option(s):
    _selected: list[SelectOption]

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: _SelectOneOrManyRuleContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ):
        super().__init__(factory, context, parent)

        self._description, self._options, self._defaults = parse_select_options(
            factory, context, self.state
        )

        # Note: It's the job of the child class to choose the default selected.

    @property
    def description(self) -> str:
        """
        Returns:
            The description for this select context.
        """
        return self._description

    @property
    def options(self) -> Sequence[SelectOption]:
        """
        Returns:
            The available options for this select context.
        """
        return self._options

    def _select(self, options: Sequence[SelectOption]) -> Self:
        """
        Select the given options and return the object.

        Args:
            options: The options to select.

        Returns:
            A copy of the current object with the given options selected.
        """
        copy = self._factory.copy_context(self)
        copy._selected = list(options)
        return copy

    def exec_(
        self,
    ) -> WizardSelectCasesContext[ContextState, _SelectOneOrManyRuleContext]:
        # This completely delegates to the other context:
        return self._factory.make_select_cases_context(
            self._selected, self.context, self.parent
        )


class WizardSelectOneContext(
    WizardSelectContext[ContextState, wizardParser.SelectOneContext]
):
    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.SelectOneContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ):
        super().__init__(factory, context, parent)

        # More than one default in SelectOne:
        if len(self._defaults) != 1:
            self._factory.severity.raise_or_warn(
                Issue.MULTIPLE_DEFAULTS_IN_SELECT_ON,
                WizardTypeError(
                    context,
                    "SelectOne statement should have a single default value.",
                ),
                "SelectOne statement should have a single default, using the"
                " first one.",
            )
            self._defaults = [self._defaults[0]]

        # We select the defaults:
        self._selected = self._defaults

    @property
    def default(self) -> SelectOption:
        """
        Returns:
            The default option for this select context.
        """
        return self._defaults[0]

    def select(self, option: SelectOption) -> WizardSelectOneContext[ContextState]:
        """
        Select the given option and return the object.

        Args:
            option: The option to select.

        Returns:
            A copy of the current object with the given option selected.
        """
        return self._select([option])


class WizardSelectManyContext(
    WizardSelectContext[ContextState, wizardParser.SelectManyContext]
):
    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.SelectManyContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ):
        super().__init__(factory, context, parent)

        # We select the defaults:
        self._selected = self._defaults

    @property
    def defaults(self) -> Sequence[SelectOption]:
        """
        Returns:
            The default options for this select context.
        """
        return self._defaults

    def select(
        self, options: Sequence[SelectOption]
    ) -> WizardSelectManyContext[ContextState]:
        """
        Select the given list of options and return the object.

        Args:
            options: The options to select.

        Returns:
            A copy of the current object with the given options selected.
        """
        return self._select(options)


class WizardSelectCasesContext(
    WizardInterpreterContext[ContextState, _SelectOneOrManyRuleContext],
    WizardBreakableContext[ContextState],
):
    # The list of selected options:
    _options: list[SelectOption]

    # The list of cases, the current index, a boolean indicating if
    # the value has been found, and a boolean for fallthrough:
    _ismany: bool
    _cases: list[wizardParser.CaseStmtContext]
    _default: wizardParser.DefaultStmtContext | None
    _index: int
    _found: bool
    _fallthrough: bool

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        options: Sequence[SelectOption],
        context: _SelectOneOrManyRuleContext,
        parent: WizardInterpreterContext[ContextState, Any],
    ):
        """
        Args:
            factory: The context factory.
            options: List of selected options.
            context: The select context.
            parent: The parent context.
        """
        super().__init__(factory, context, parent)

        self._options = list(options)

        if isinstance(self.context, wizardParser.SelectOneContext):
            self._ismany = False
        else:
            self._ismany = True

        self._cases = list(context.selectCaseList().caseStmt())
        self._default = context.selectCaseList().defaultStmt()

        self._index = 0
        self._found = False
        self._fallthrough = False

    def break_(self) -> WizardInterpreterContext[ContextState, Any]:
        # Disable fallthrough:
        copy = self._factory.copy_context(self)
        copy._fallthrough = False

        # We return the context itself to keep evaluating cases:
        return copy

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        # Element found in a selectOne, returns to the parent:
        if self._found and not self._ismany and not self._fallthrough:
            return self._factory.copy_parent(self)

        # Copy the current context:
        snext = self._factory.copy_context(self)

        # Cases remaining:
        if self._index < len(self._cases):
            # Find the next case:
            case = self._cases[self._index]
            snext._index += 1

            target: Value[str] = self._factory.evisitor.visitExpr(
                case.expr(), snext.state, str
            )

            # Check if the case match or if we have a fallthrough:
            if self._fallthrough or any(
                sopt.name == target.value for sopt in self._options
            ):
                # We found the value, remember it:
                snext._found = True

                # Assume fallthrough, the break_() will set this off if a 'Break'
                # statement is found:
                snext._fallthrough = True

                return self._factory.make_case_context(case, snext)

            # Return the context itself:
            return snext

        # No cases remaining, default, and not found:
        elif self._default and (self._fallthrough or not self._found):
            snext._found = True
            return self._factory.make_case_context(self._default, snext)

        # No need to copy from snext since if we reach this return statement, nothing
        # has been updated in snext.
        return self._factory.copy_parent(self)


class WizardCaseContext(
    WizardInterpreterContext[
        ContextState, wizardParser.CaseStmtContext | wizardParser.DefaultStmtContext
    ]
):
    def exec_(self) -> WizardBodyContext[ContextState]:
        # It's the select context job to check if this should be executed:
        return self._factory.make_body_context(self.context.body(), self.parent)
