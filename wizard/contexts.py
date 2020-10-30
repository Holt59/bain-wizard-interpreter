# -*- encoding: utf-8 -*-

"""
This file contains "context" which are used to rewind the
interpreter.
"""

from abc import abstractmethod
from typing import (
    Callable,
    Generic,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from antlr4 import ParserRuleContext
from .antlr4.wizardParser import wizardParser

from .errors import WizardNameError, WizardParseError, WizardTypeError
from .expr import AbstractWizardInterpreter, WizardExpressionVisitor
from .mmitf import SelectOption
from .severity import Issue
from .value import Value, SubPackage, SubPackages


RuleContext = TypeVar("RuleContext", bound=ParserRuleContext)


class WizardInterpreterContext(Generic[RuleContext]):

    """
    The base context class. The context are represented by a tree, where each
    child has access to his parent. Unlike ANTLR4 context, not all rules or
    elements in the grammer creates a context.
    """

    # The interpreter:
    _interpreter: AbstractWizardInterpreter

    # The visitor:
    _evisitor: WizardExpressionVisitor

    # The ANTLR4 context:
    _context: RuleContext

    # The parent context:
    _parent: Optional["WizardInterpreterContext"]

    def __init__(
        self,
        interpreter: AbstractWizardInterpreter,
        evisitor: WizardExpressionVisitor,
        context: RuleContext,
        parent: Optional["WizardInterpreterContext"] = None,
    ):
        """
        Args:
            interpreter: The interpreter.
            evisitor: The visitor.
            context: The ANTLR4 context.
            parent: The parent context.
        """
        self._interpreter = interpreter
        self._evisitor = evisitor
        self._context = context
        self._parent = parent

    @property
    def parent(self) -> Optional["WizardInterpreterContext"]:
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

    @abstractmethod
    def exec(self) -> Optional["WizardInterpreterContext"]:
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
    def break_(self) -> Optional[WizardInterpreterContext]:
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


class WizardCancelContext(WizardInterpreterContext[wizardParser.CancelContext]):

    """
    Special context that is returned when a 'Cancel' instruction is encountered.
    """

    def exec(self) -> Optional["WizardInterpreterContext"]:
        return None


class WizardReturnContext(WizardInterpreterContext[wizardParser.ReturnContext]):

    """
    Special context that is returned when a 'Return' instruction is encountered.
    """

    def exec(self) -> Optional["WizardInterpreterContext"]:
        return None


class WizardBodyContext(WizardInterpreterContext[wizardParser.BodyContext]):

    """
    Body context.
    """

    # Index of the next child to process.
    _ichild: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ichild = 0

    def exec(self) -> Optional["WizardInterpreterContext"]:

        # Empty block or no more children:
        if not self._context.children or self._ichild == len(self._context.children):
            return self.parent

        child = self._context.children[self._ichild]
        self._ichild += 1

        # Expression - Standard context:
        if isinstance(child, wizardParser.ExprContext):
            self._evisitor.visitExpr(child)
            return self

        if isinstance(child, wizardParser.StmtContext):
            if child.assignment():
                return WizardAssignmentContext(
                    self._interpreter, self._evisitor, child.assignment(), self
                )
            elif child.compoundAssignment():
                return WizardAssignmentContext(
                    self._interpreter, self._evisitor, child.compoundAssignment(), self
                )
            elif child.controlFlowStmt():
                return self._visitControlFlowStmt(child.controlFlowStmt())
            elif child.keywordStmt():
                return WizardKeywordContext(
                    self._interpreter, self._evisitor, child.keywordStmt(), self
                )

        raise WizardParseError(f"Unknow context in body: {child}.")

    def _visitControlFlowStmt(
        self, ctx: wizardParser.ControlFlowStmtContext
    ) -> WizardInterpreterContext:

        # Small utility to avoid boiler-plate code:
        def make(typ: Type[WizardInterpreterContext], ctx) -> WizardInterpreterContext:
            return typ(self._interpreter, self._evisitor, ctx, self)

        if isinstance(ctx, wizardParser.ForContext):
            return make(WizardForLoopContext, ctx.forStmt())
        elif isinstance(ctx, wizardParser.WhileContext):
            return make(WizardWhileLoopContext, ctx.whileStmt())
        elif isinstance(ctx, wizardParser.IfContext):
            return make(WizardIfContext, ctx.ifStmt())
        elif isinstance(ctx, wizardParser.SelectContext):
            return make(WizardSelectContext, ctx.selectStmt())
        elif isinstance(ctx, wizardParser.BreakContext):
            return make(WizardBreakContext, ctx)
        elif isinstance(ctx, wizardParser.ContinueContext):
            return make(WizardContinueContext, ctx)
        elif isinstance(ctx, wizardParser.CancelContext):
            return make(WizardCancelContext, ctx)
        elif isinstance(ctx, wizardParser.ReturnContext):
            return make(WizardReturnContext, ctx)

        raise WizardParseError(f"Unknown control flow statement: {ctx}.")


class WizardBreakContext(WizardInterpreterContext[wizardParser.BreakContext]):
    def exec(self) -> Optional["WizardInterpreterContext"]:

        # Find the first loop or case:
        loop_or_case: Optional[WizardInterpreterContext] = self

        while loop_or_case is not None and not isinstance(
            loop_or_case, WizardBreakableContext
        ):
            loop_or_case = loop_or_case.parent

        if loop_or_case is None:
            raise WizardParseError("Invalid 'Break' statement encountered.")

        return loop_or_case.break_()


class WizardContinueContext(WizardInterpreterContext[wizardParser.ContinueContext]):
    def exec(self) -> Optional["WizardInterpreterContext"]:

        # Find the first parent loop:
        loop: Optional[WizardInterpreterContext] = self

        while loop is not None and not isinstance(loop, WizardContinuableContext):
            loop = loop.parent

        if loop is None:
            raise WizardParseError("Invalid 'Continue' statement encountered.")

        return loop.continue_()


class WizardIfContext(WizardInterpreterContext[wizardParser.IfStmtContext]):
    def exec(self) -> Optional["WizardInterpreterContext"]:

        if self._evisitor.visitExpr(self.context.expr()):
            return WizardBodyContext(
                self._interpreter, self._evisitor, self.context.body(), self.parent
            )
        else:
            for eifc in self.context.elifStmt():
                if self._evisitor.visitExpr(eifc.expr()):
                    return WizardBodyContext(
                        self._interpreter, self._evisitor, eifc.body(), self.parent
                    )

            if self.context.elseStmt():
                return WizardBodyContext(
                    self._interpreter,
                    self._evisitor,
                    self.context.elseStmt().body(),
                    self.parent,
                )

        return self.parent


class WizardForLoopContext(
    WizardInterpreterContext[wizardParser.ForStmtContext],
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
            self._values = self._visitForInHeader(self.context.forInHeader())
        else:
            self._values = self._visitForRangeHeader(self.context.forRangeHeader())

        self._name = self.context.Identifier().getText()
        self._index = 0

    def break_(self) -> Optional[WizardInterpreterContext]:
        return self.parent

    def continue_(self) -> WizardInterpreterContext:
        return self

    def _visitForRangeHeader(
        self, ctx: wizardParser.ForRangeHeaderContext
    ) -> Sequence[Value]:
        start = self._evisitor.visitExpr(ctx.expr(0))
        end = self._evisitor.visitExpr(ctx.expr(1))

        if ctx.expr(2):
            by = self._evisitor.visitExpr(ctx.expr(2))
        else:
            by = Value(1)

        if (
            isinstance(start.value, int)
            and isinstance(end.value, int)
            and isinstance(by.value, int)
        ):
            return [Value(i) for i in range(start.value, end.value + 1, by.value)]

        raise WizardTypeError("Cannot create range from non-integer values.")

    def _visitForInHeader(
        self, ctx: wizardParser.ForInHeaderContext
    ) -> Sequence[Value]:
        value = self._evisitor.visitExpr(ctx.expr())

        if isinstance(value.value, SubPackage):
            return [Value(f) for f in value.value.files]
        elif isinstance(value.value, SubPackages):
            return [Value(sp) for sp in value.value]
        elif isinstance(value.value, str):
            # TODO: Allow?
            return [Value(s) for s in value.value]
        else:
            raise WizardTypeError(f"Cannot iterable over value of type {value.type}.")

    def exec(self) -> Optional["WizardInterpreterContext"]:

        # End of the loop:
        if self._index == len(self._values):
            # Remove the variable:
            if self._name in self._interpreter.variables:
                del self._interpreter.variables[self._name]

            return self.parent

        # Retrieve the next value and set it:
        value = self._values[self._index]
        self._index += 1

        self._interpreter.variables[self._name] = value

        # Return a body context:
        return WizardBodyContext(
            self._interpreter, self._evisitor, self.context.body(), self
        )


class WizardWhileLoopContext(
    WizardInterpreterContext[wizardParser.WhileStmtContext],
    WizardBreakableContext,
    WizardContinuableContext,
):
    def break_(self) -> Optional[WizardInterpreterContext]:
        return self.parent

    def continue_(self) -> WizardInterpreterContext:
        return self

    def exec(self) -> Optional["WizardInterpreterContext"]:

        # If the expression evaluates to True, we return a body context:
        if self._evisitor.visitExpr(self.context.expr()):
            return WizardBodyContext(
                self._interpreter, self._evisitor, self.context.body(), self
            )

        # Otherwise we return the parent:
        return self.parent


class WizardKeywordContext(WizardInterpreterContext[wizardParser.KeywordStmtContext]):
    def exec(self) -> Optional["WizardInterpreterContext"]:
        # We consider keyword as function - Is there a real difference?

        name: str = self.context.Keyword().getText()
        if name not in self._interpreter.functions:
            raise WizardNameError(name)

        self._interpreter.functions[name](
            [self._evisitor.visitExpr(ex) for ex in self.context.argList().expr()]
        )

        return self.parent


class WizardAssignmentContext(
    WizardInterpreterContext[
        Union[wizardParser.AssignmentContext, wizardParser.CompoundAssignmentContext]
    ]
):
    def exec(self) -> Optional["WizardInterpreterContext"]:

        # Retrieve the name:
        name: str = self.context.Identifier().getText()

        # Evalue the expression:
        value: Value = self._evisitor.visitExpr(self.context.expr())

        if isinstance(self.context, wizardParser.CompoundAssignmentContext):
            if name not in self._interpreter.variables:
                raise WizardNameError(name)

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
                raise WizardParseError(f"Unknown compouned operation: {self.context}.")

            value = op(self._interpreter.variables[name], value)

        self._interpreter.variables[name] = value

        return self.parent


class WizardSelectContext(WizardInterpreterContext[wizardParser.SelectStmtContext]):

    """
    The select context is split in multiple contexts:
      - The WizardSelectContext queries the user and returns a WizardSelectCasesContext,
      - The WizardSelectCasesContext loop through the cases returning WizardCaseContext
        or WizardDefaultContext,
      - The WizardCaseContext and WizardDefaultContext simply evaluate their bodies.
    """

    def exec(self) -> "WizardSelectCasesContext":

        one = False
        ctxx: Union[wizardParser.SelectOneContext, wizardParser.SelectManyContext]
        if self.context.selectOne():
            one = True
            ctxx = self.context.selectOne()
        else:
            one = False
            ctxx = self.context.selectMany()

        # Parse the description and option:
        desc = self._evisitor.visitExpr(ctxx.expr())
        if not isinstance(desc.value, str):
            raise WizardTypeError("Description should be a string.")

        opts: List[SelectOption] = []
        defs: List[SelectOption] = []
        for opt in ctxx.optionTuple():
            a, b, c = (
                self._evisitor.visitExpr(opt.expr(0)),
                self._evisitor.visitExpr(opt.expr(1)),
                self._evisitor.visitExpr(opt.expr(2)),
            )

            if (
                not isinstance(a.value, str)
                or not isinstance(b.value, str)
                or not isinstance(c.value, str)
            ):
                raise WizardTypeError("Invalid option for select statement.")

            name = a.value
            isdef = False
            if name.startswith("|"):
                name = name[1:]
                isdef = True

            opts.append(
                SelectOption(name, b.value, c.value if c.value.strip() else None)
            )

            # Add to defaults:
            if isdef:
                defs.append(opts[-1])

        # Actually do the selection?
        sopts: List[SelectOption] = []
        if one:
            if len(defs) > 1:
                self._interpreter.severity.raise_or_warn(
                    Issue.MULTIPLE_DEFAULTS_IN_SELECT_ON,
                    WizardTypeError(
                        "Cannot have multiple default values with SelectOne."
                    ),
                    "SelectOne statement should have a single default, using the"
                    " first one.",
                )
            sopts = [
                self._interpreter.manager.selectOne(
                    desc.value, opts, defs[0] if defs else opts[0]
                )
            ]
        else:
            sopts = self._interpreter.manager.selectMany(desc.value, opts, defs)

        # This completely delegates to the other context:
        return WizardSelectCasesContext(
            sopts, self._interpreter, self._evisitor, self.context, self.parent
        )


class WizardSelectCasesContext(
    WizardInterpreterContext[wizardParser.SelectStmtContext], WizardBreakableContext
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

    def __init__(self, options: List[SelectOption], *args, **kwargs):
        """
        Args:
            options: List of selected options.
            *args, **kwargs: See WizardInterpreterContext.
        """
        super().__init__(*args, **kwargs)

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

    def break_(self) -> Optional[WizardInterpreterContext]:
        # Disable fallthrough:
        self._fallthrough = False

        # We return the context itself to keep evaluating cases:
        return self

    def exec(self) -> Optional[WizardInterpreterContext]:

        # Element found in a selectOne, returns to the parent:
        if self._found and not self._ismany and not self._fallthrough:
            return self.parent

        # Cases remaining:
        if self._index < len(self._cases):

            # Find the next case:
            case = self._cases[self._index]
            self._index += 1

            target = self._evisitor.visitExpr(case.expr())
            if not isinstance(target.value, str):
                raise WizardTypeError(
                    f"Case label should be string, not {target.type}."
                )

            # Check if the case match or if we have a fallthrough:
            if self._fallthrough or any(
                sopt.name == target.value for sopt in self._options
            ):

                # We found the value, remember it:
                self._found = True

                # Assume fallthrough, the break_() will set this off if a 'Break'
                # statement is found:
                self._fallthrough = True

                return WizardCaseContext(self._interpreter, self._evisitor, case, self)

            # Return the context itself:
            return self

        # No cases remaining, default, and not found:
        elif self._default and (self._fallthrough or not self._found):
            self._found = True
            return WizardCaseContext(
                self._interpreter, self._evisitor, self._default, self
            )

        return self.parent


class WizardCaseContext(
    WizardInterpreterContext[
        Union[wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext]
    ]
):
    def __init__(
        self,
        interpreter: AbstractWizardInterpreter,
        evisitor: WizardExpressionVisitor,
        context: Union[wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext],
        parent: WizardSelectCasesContext,
    ):
        super().__init__(interpreter, evisitor, context, parent)

    def exec(self) -> Optional[WizardInterpreterContext]:
        # It's the select context job to check if this should be executed:
        return WizardBodyContext(
            self._interpreter, self._evisitor, self.context.body(), self.parent
        )
