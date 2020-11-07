# -*- encoding: utf-8 -*-

"""
This file contains "context" which are used to rewind the
interpreter.
"""

from abc import abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
    TYPE_CHECKING,
)

from antlr4 import ParserRuleContext
from ..antlr4.wizardParser import wizardParser

from ..errors import WizardNameError, WizardParseError, WizardTypeError
from ..manager import SelectOption
from ..severity import Issue
from ..state import ContextState
from ..value import Value, SubPackage, SubPackages

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
    _factory: "WizardInterpreterContextFactory"

    # The ANTLR4 context:
    _context: RuleContext

    # The parent context:
    _parent: "WizardInterpreterContext"

    # The state of this context:
    _state: ContextState

    def __init__(
        self,
        factory: "WizardInterpreterContextFactory",
        context: RuleContext,
        parent: "WizardInterpreterContext[ContextState, Any]",
        state: Optional[ContextState] = None,
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

    @property
    def parent(self) -> "WizardInterpreterContext":
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
    def exec(self) -> "WizardInterpreterContext":
        """
        Execute the next 'step' of this context and returns the next context
        to execute. When done, should return the parent context.
        """
        pass


class WizardBreakableContext:

    """
    Context that can be broken by a 'Break' expression.
    """

    @abstractmethod
    def break_(self) -> WizardInterpreterContext:
        """
        Called when a 'Break' instruction is encountered, should usually return
        the parent.

        Returns:
            The next context to use after this break.
        """
        pass


class WizardContinuableContext:

    """
    Context that can be broken by a 'Continue' expression.
    """

    @abstractmethod
    def continue_(self) -> WizardInterpreterContext:
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

    def exec(self) -> WizardInterpreterContext:
        raise NotImplementedError("exec() should not be called on termination context.")

    def is_cancel(self) -> bool:
        """
        Returns:
            True if this termination was caused by a 'Cancel' keyword.
        """
        return isinstance(self.parent, WizardCancelContext)

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
    Special context to be the entry context point. This avoid having Optional[] only for
    the body context.
    """

    def __init__(
        self,
        factory: "WizardInterpreterContextFactory",
        context: wizardParser.ParseWizardContext,
        state: ContextState,
    ):
        super().__init__(factory, context, self, state)

    def exec(self) -> WizardInterpreterContext:
        return self._factory.make_body_context(self.context.body(), self)


class WizardCancelContext(
    WizardInterpreterContext[ContextState, wizardParser.CancelContext]
):

    """
    Special context that is returned when a 'Cancel' instruction is encountered.
    """

    def exec(self) -> WizardInterpreterContext:
        return self._factory.make_termination_context(self)


class WizardReturnContext(
    WizardInterpreterContext[ContextState, wizardParser.ReturnContext]
):

    """
    Special context that is returned when a 'Return' instruction is encountered.
    """

    def exec(self) -> WizardInterpreterContext:
        return self._factory.make_termination_context(self)


class WizardBodyContext(
    WizardInterpreterContext[ContextState, wizardParser.BodyContext]
):

    """
    Body context.
    """

    # Index of the next child to process.
    _ichild: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ichild = 0

    def exec(self) -> WizardInterpreterContext:

        # Empty block or no more children:
        if not self._context.children or self._ichild == len(self._context.children):
            if isinstance(self._parent, WizardTopLevelContext):
                return self._factory.make_termination_context(self)
            return self._factory._copy_parent(self)

        child = self._context.children[self._ichild]

        # Copy the body and increment the child counter:
        body = self._factory._copy_context(self)
        body._ichild += 1

        # Expression - Standard context:
        if isinstance(child, wizardParser.ExprContext):
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
        self, ctx: wizardParser.ControlFlowStmtContext, parent: "WizardBodyContext"
    ) -> WizardInterpreterContext:

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
            return self._factory.make_cancel_context(ctx, parent)
        elif isinstance(ctx, wizardParser.ReturnContext):
            return self._factory.make_return_context(ctx, parent)

        raise WizardParseError(ctx, f"Unknown control flow statement: {ctx}.")


class WizardBreakContext(
    WizardInterpreterContext[ContextState, wizardParser.BreakContext]
):
    def exec(self) -> WizardInterpreterContext:

        # Find the first loop or case:
        loop_or_case: Optional[WizardInterpreterContext] = self

        while loop_or_case is not None and not isinstance(
            loop_or_case, WizardBreakableContext
        ):
            loop_or_case = loop_or_case.parent

        if loop_or_case is None:
            raise WizardParseError(
                self.context, "Invalid 'Break' statement encountered."
            )

        return self._factory._copy_context(loop_or_case.break_(), self.state)


class WizardContinueContext(
    WizardInterpreterContext[ContextState, wizardParser.ContinueContext]
):
    def exec(self) -> WizardInterpreterContext:

        # Find the first parent loop:
        loop: Optional[WizardInterpreterContext] = self

        while loop is not None and not isinstance(loop, WizardContinuableContext):
            loop = loop.parent

        if loop is None:
            raise WizardParseError(
                self.context, "Invalid 'Continue' statement encountered."
            )

        return self._factory._copy_context(loop.continue_(), self.state)


class WizardIfContext(
    WizardInterpreterContext[ContextState, wizardParser.IfStmtContext]
):
    def exec(self) -> WizardInterpreterContext:

        parent = self._factory._copy_parent(self)

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
    WizardBreakableContext,
    WizardContinuableContext,
):

    """
    For-loop context.
    """

    # Name of the loop variable, sequence of values and current index:
    _name: str
    _values: Sequence[Value]
    _index: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.forInHeader():
            self._values = self._for_in_header(self.context.forInHeader())
        else:
            self._values = self._for_range_header(self.context.forRangeHeader())

        self._name = self.context.Identifier().getText()
        self._index = 0

    def break_(self) -> WizardInterpreterContext:
        return self._factory._copy_parent(self)

    def continue_(self) -> WizardInterpreterContext:
        return self

    def _for_range_header(
        self, ctx: wizardParser.ForRangeHeaderContext
    ) -> Sequence[Value]:

        sta: Value[int] = self._factory.evisitor.visitExpr(ctx.expr(0), self.state, int)
        end: Value[int] = self._factory.evisitor.visitExpr(ctx.expr(1), self.state, int)

        if ctx.expr(2):
            by = self._factory.evisitor.visitExpr(ctx.expr(2), self.state, int)
        else:
            by = Value(1)

        return [Value(i) for i in range(sta.value, end.value + 1, by.value)]

    def _for_in_header(self, ctx: wizardParser.ForInHeaderContext) -> Sequence[Value]:

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

    def exec(self) -> WizardInterpreterContext:

        # End of the loop:
        if self._index == len(self._values):
            return self._factory._copy_parent(self)

        # Retrieve the next value and set it:
        value = self._values[self._index]

        # Copy the context:
        loop = self._factory._copy_context(self)
        loop._index += 1

        loop.state._variables[self._name] = value

        # Return a body context:
        return self._factory.make_body_context(self.context.body(), loop)


class WizardWhileLoopContext(
    WizardInterpreterContext[ContextState, wizardParser.WhileStmtContext],
    WizardBreakableContext,
    WizardContinuableContext,
):
    def break_(self) -> WizardInterpreterContext:
        return self._factory._copy_parent(self)

    def continue_(self) -> WizardInterpreterContext:
        return self

    def exec(self) -> WizardInterpreterContext:

        loop = self._factory._copy_context(self)

        # If the expression evaluates to True, we return a body context:
        if self._factory.evisitor.visitExpr(self.context.expr(), loop.state):
            return self._factory.make_body_context(self.context.body(), loop)

        # Otherwise we return the parent (after updating the variables):
        return self._factory._copy_parent(loop)


class WizardAssignmentContext(
    WizardInterpreterContext[
        ContextState,
        wizardParser.AssignmentContext,
    ]
):
    def exec(self) -> WizardInterpreterContext:

        parent = self._factory._copy_parent(self)

        # Retrieve the name:
        name: str = self.context.Identifier().getText()

        # Evaluate the expression:
        value: Value = self._factory.evisitor.visitExpr(
            self.context.expr(), parent.state
        )

        parent.state._variables[name] = value

        return parent


class WizardCompoundAssignmentContext(
    WizardInterpreterContext[
        ContextState,
        wizardParser.CompoundAssignmentContext,
    ]
):
    def exec(self) -> WizardInterpreterContext:

        parent = self._factory._copy_parent(self)

        # Retrieve the name:
        name: str = self.context.Identifier().getText()

        # Evaluate the expression:
        value: Value = self._factory.evisitor.visitExpr(
            self.context.expr(), parent.state
        )

        if name not in parent.state._variables:
            raise WizardNameError(self.context.Identifier(), name)

        op: Callable[[Value, Value], Value]
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
            value = op(parent.state._variables[name], value)
        except TypeError as te:
            raise WizardTypeError(self.context, str(te))

        parent.state._variables[name] = value

        return parent


class WizardSelectContext(
    WizardInterpreterContext[ContextState, wizardParser.SelectStmtContext]
):

    """
    The select context is split in multiple contexts:
      - The WizardSelectContext queries the user and returns a WizardSelectCasesContext,
      - The WizardSelectCasesContext loop through the cases returning WizardCaseContext
        or WizardDefaultContext,
      - The WizardCaseContext and WizardDefaultContext simply evaluate their bodies.
    """

    # SelectMany or SelectOne:
    _many: bool

    # The description:
    _description: str

    # The list of options:
    _options: List[SelectOption]

    # The default option(s):
    _defaults: List[SelectOption]

    # The selected option(s):
    _selected: List[SelectOption]

    def __init__(
        self,
        factory: "WizardInterpreterContextFactory",
        context: wizardParser.SelectStmtContext,
        parent: WizardInterpreterContext,
    ):
        super().__init__(factory, context, parent)

        ctxx: Union[wizardParser.SelectOneContext, wizardParser.SelectManyContext]
        if self.context.selectOne():
            self._many = False
            ctxx = self.context.selectOne()
        else:
            self._many = True
            ctxx = self.context.selectMany()

        # Parse the description and option:
        self._description = self._factory.evisitor.visitExpr(
            ctxx.expr(), self.state, str
        ).value

        self._options = []
        self._defaults = []
        for opt in ctxx.optionTuple():
            a, b, c = (
                self._factory.evisitor.visitExpr(opt.expr(0), self.state, str),
                self._factory.evisitor.visitExpr(opt.expr(1), self.state, str),
                self._factory.evisitor.visitExpr(opt.expr(2), self.state, str),
            )

            name = a.value
            isdef = False
            if name.startswith("|"):
                name = name[1:]
                isdef = True

            self._options.append(
                SelectOption(name, b.value, c.value if c.value.strip() else None)
            )

            # Add to defaults:
            if isdef:
                self._options.append(self._options[-1])

        # Not default in SelectOne -> Select first one.
        if not self._many and not self._defaults:
            self._defaults.append(self._options[0])

        # More than one default in SelectOne:
        if not self._many and len(self._defaults) != 1:
            self._factory.severity.raise_or_warn(
                Issue.MULTIPLE_DEFAULTS_IN_SELECT_ON,
                WizardTypeError(
                    ctxx.optionTuple(),
                    "SelectOne statement should have a single default value.",
                ),
                "SelectOne statement should have a single default, using the"
                " first one.",
            )
            self._defaults = [self._defaults[0]]

        # We select the defaults:
        self._selected = self._defaults

    def is_many(self) -> bool:
        """
        Returns:
            True if this context corresponds to a SelectMany, False if it corresponds
            to a SelectOne.
        """
        return self._many

    @property
    def description(self) -> str:
        """
        Returns:
            The description for this select context.
        """
        return self._description

    @property
    def options(self) -> List[SelectOption]:
        """
        Returns:
            The available options for this select context.
        """
        return self._options

    @property
    def defaults(self) -> List[SelectOption]:
        """
        Returns:
            The default options for this select context. This is always a list, but
            for SelectOne, the list will contain a single element.
        """
        return self._defaults

    def select(self, options: List[SelectOption]) -> "WizardSelectContext":
        """
        Select the given list of options and return the object.

        Args:
            options: The option to select.

        Returns:
            A copy of the current object with the given options selected.
        """
        copy = self._factory._copy_context(self)
        copy._selected = options
        return copy

    def exec(self) -> "WizardSelectCasesContext":
        # This completely delegates to the other context:
        return self._factory.make_select_cases_context(
            self._selected, self.context, self.parent
        )


class WizardSelectCasesContext(
    WizardInterpreterContext[ContextState, wizardParser.SelectStmtContext],
    WizardBreakableContext,
):

    # The list of selected options:
    _options: List[SelectOption]

    # The list of cases, the current index, a boolean indicating if
    # the value has been found, and a boolean for fallthrough:
    _ismany: bool
    _cases: List[wizardParser.CaseStmtContext]
    _default: Optional[wizardParser.DefaultStmtContext]
    _index: int
    _found: bool
    _fallthrough: bool

    def __init__(
        self,
        factory: "WizardInterpreterContextFactory",
        options: List[SelectOption],
        context: wizardParser.IfStmtContext,
        parent: WizardInterpreterContext,
    ):
        """
        Args:
            factory: The context factory.
            options: List of selected options.
            context: The select context.
            parent: The parent context.
        """
        super().__init__(factory, context, parent)

        self._options = options

        if self.context.selectOne():
            self._ismany = False
            ctxx = self.context.selectOne()
        else:
            self._ismany = True
            ctxx = self.context.selectMany()
        self._cases = list(ctxx.selectCaseList().caseStmt())
        self._default = ctxx.selectCaseList().defaultStmt()

        self._index = 0
        self._found = False
        self._fallthrough = False

    def break_(self) -> WizardInterpreterContext:
        # Disable fallthrough:
        copy = self._factory._copy_context(self)
        copy._fallthrough = False

        # We return the context itself to keep evaluating cases:
        return copy

    def exec(self) -> WizardInterpreterContext:

        # Element found in a selectOne, returns to the parent:
        if self._found and not self._ismany and not self._fallthrough:
            return self._factory._copy_parent(self)

        # Copy the current context:
        snext = self._factory._copy_context(self)

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
        return self._factory._copy_parent(self)


class WizardCaseContext(
    WizardInterpreterContext[
        ContextState,
        Union[wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext],
    ]
):
    def exec(self) -> WizardInterpreterContext:
        # It's the select context job to check if this should be executed:
        return self._factory.make_body_context(self.context.body(), self.parent)
