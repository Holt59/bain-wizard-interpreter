# -*- encoding: utf-8 -*-

from typing import Callable, Iterable, List, Mapping, MutableMapping, Tuple, Union

from .antlr4.wizardParser import wizardParser
from .antlr4.wizardVisitor import wizardVisitor

from .errors import WizardNameError, WizardParseError, WizardTypeError
from .expr import SubPackage, SubPackages, Value, WizardExpressionVisitor
from .mmitf import SelectOption, ModManagerInterface


class LoopContext:

    """
    Small structure used to track Break and Continue statement.
    """

    _continue: bool
    _break: bool

    def __init__(self):
        self.reset()

    def do_break(self):
        """
        Set the Break flag.
        """
        self._break = True

    def do_continue(self):
        """
        Set the Continue flag.
        """
        self._continue = True

    def is_continue(self) -> bool:
        """
        Returns:
            True if the Continue flag is set.
        """
        return self._continue

    def is_break(self) -> bool:
        """
        Returns:
            True if the Break flag is set.
        """
        return self._break

    def is_break_or_continue(self) -> bool:
        """
        Returns:
            True if either the Break or Continue flag is set.
        """
        return self._break or self._continue

    def reset(self):
        """
        Reset the Continue and Break flag for this context.
        """
        self._continue = False
        self._break = False


class CancelFlow(Exception):

    """
    This is a "safe" exception that should be caught by the program using
    the WizardInterpreter and that indicates that a 'Cancel' keyword was
    encountered.
    """

    pass


class ReturnFlow(Exception):

    """
    This is a "safe" exception that should be caught by the program using
    the WizardInterpreter and that indicates that a 'Return' keyword was
    encountered.
    """

    pass


class WizardInterpreter(wizardVisitor):
    def __getattribute__(self, name):
        # For debug purpose:
        if name.startswith("visit"):
            if name not in WizardInterpreter.__dict__:
                raise ValueError(f"Method {name} not implemented in WizardInterpreter.")
        return object.__getattribute__(self, name)

    _manager: ModManagerInterface

    _subpackages: SubPackages
    _variables: MutableMapping[str, Value]
    _functions: Mapping[str, Callable[[List[Value]], Value]]

    _evisitor: WizardExpressionVisitor

    _loops: List[LoopContext]

    def __init__(
        self,
        manager: ModManagerInterface,
        subpackages: SubPackages,
        functions: Mapping[str, Callable[[List[Value]], Value]],
    ):
        self._manager = manager

        self._variables = {}
        self._subpackages = subpackages
        self._functions = functions

        self._evisitor = WizardExpressionVisitor(
            self._variables, self._subpackages, self._functions
        )

        self._loops = []

    def visit(self, ctx: wizardParser.ParseWizardContext):
        self.visitBody(ctx.body())

    def visitBody(self, ctx: wizardParser.BodyContext):

        # Happens with empty block:
        if not ctx.children:
            return

        for c in ctx.children:

            if self._loops and self._loops[-1].is_break_or_continue():
                break

            if isinstance(c, wizardParser.ExprContext):
                self._evisitor.visitExpr(c)
            elif isinstance(c, wizardParser.StmtContext):
                self.visitStmt(c)
            else:
                raise WizardParseError(f"Unknow context in body: {c}.")

    def visitStmt(self, ctx: wizardParser.StmtContext):
        if ctx.assignment():
            self.visitAssignment(ctx.assignment())
        elif ctx.compoundAssignment():
            self.visitCompoundAssignment(ctx.compoundAssignment())
        elif ctx.controlFlowStmt():
            self.visitControlFlowStmt(ctx.controlFlowStmt())
        elif ctx.keywordStmt():
            self.visitKeywordStmt(ctx.keywordStmt())
        else:
            raise WizardParseError(f"Unknow context statement: {ctx}.")

    def visitKeywordStmt(self, ctx: wizardParser.KeywordStmtContext):
        # We consider keyword as function - Is there a real difference?

        name = ctx.Keyword().getText()
        if name not in self._functions:
            raise WizardNameError(name)

        values: List[Value] = []
        for ex in ctx.argList().expr():
            values.append(self.visitExpr(ex))
        return self._functions[name](values)

    def visitAssignment(self, ctx: wizardParser.AssignmentContext):
        self._variables[ctx.Identifier().getText()] = self._evisitor.visitExpr(
            ctx.expr()
        )

    # Visit a parse tree produced by wizardParser#compoundAssignment.
    def visitCompoundAssignment(self, ctx: wizardParser.CompoundAssignmentContext):
        name: str = ctx.Identifier().getText()
        if name not in self._variables:
            raise WizardNameError(name)

        op: Callable[[Value, Value], Value]
        if ctx.CompoundExp():
            op = Value.__pow__
        elif ctx.CompoundMul():
            op = Value.__mul__
        elif ctx.CompoundDiv():
            op = Value.__div__
        elif ctx.CompoundMod():
            op = Value.__mod__
        elif ctx.CompoundAdd():
            op = Value.__add__
        elif ctx.CompoundSub():
            op = Value.__sub__
        else:
            raise WizardParseError(f"Unknown compouned operation: {ctx}.")

        self._variables[name] = op(
            self._variables[name], self._evisitor.visitExpr(ctx.expr())
        )

    # Visit a parse tree produced by wizardParser#controlFlowStmt.
    def visitControlFlowStmt(self, ctx: wizardParser.ControlFlowStmtContext):
        if isinstance(ctx, wizardParser.ForContext):
            self.visitForStmt(ctx.forStmt())
        elif isinstance(ctx, wizardParser.WhileContext):
            self.visitWhileStmt(ctx.whileStmt())
        elif isinstance(ctx, wizardParser.IfContext):
            self.visitIfStmt(ctx.ifStmt())
        elif isinstance(ctx, wizardParser.SelectContext):
            self.visitSelectStmt(ctx.selectStmt())
        elif isinstance(ctx, wizardParser.BreakContext):
            self._loops[-1].do_break()
        elif isinstance(ctx, wizardParser.ContinueContext):
            self._loops[-1].do_continue()
        elif isinstance(ctx, wizardParser.CancelContext):
            raise CancelFlow()
        elif isinstance(ctx, wizardParser.ReturnContext):
            raise ReturnFlow()
        else:
            raise WizardParseError(f"Unknown control flow statement: {ctx}.")

    def visitWhileStmt(self, ctx: wizardParser.WhileStmtContext):

        # Create a loop context:
        loop = LoopContext()
        self._loops.append(loop)

        while True:

            # Reset the "loop" context:
            loop.reset()

            # If the expression evaluates to False:
            if not ctx.expr():
                break

            # Visit the body (this will not visit in case of break / continue):
            self.visitBody(ctx.body())

            # If break:
            if loop.is_break():
                break

        self._loops.pop()

    def visitForStmt(self, ctx: wizardParser.ForStmtContext):

        # Create a loop context:
        loop = LoopContext()
        self._loops.append(loop)

        rng: Iterable[Value]
        if ctx.forInHeader():
            rng = self.visitForInHeader(ctx.forInHeader())
        else:
            rng = self.visitForRangeHeader(ctx.forRangeHeader())

        name: str = ctx.Identifier().getText()

        for value in rng:

            # Reset the "loop" context:
            loop.reset()

            # Update variable:
            self._variables[name] = value

            # Visit the body (this will not visit in case of break / continue):
            self.visitBody(ctx.body())

            # If break:
            if loop.is_break():
                break

        # Delete the variable?
        del self._variables[name]

        self._loops.pop()

    def visitForRangeHeader(
        self, ctx: wizardParser.ForRangeHeaderContext
    ) -> Iterable[Value]:
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
            return (Value(i) for i in range(start.value, end.value + 1, by.value))

        raise WizardTypeError("Cannot create range from non-integer values.")

    def visitForInHeader(self, ctx: wizardParser.ForInHeaderContext) -> Iterable[Value]:
        value = self._evisitor.visitExpr(ctx.expr())

        if isinstance(value.value, SubPackage):
            return (Value(f) for f in value.value.files)
        elif isinstance(value.value, SubPackages):
            return (Value(sp) for sp in value.value)
        elif isinstance(value.value, str):
            # TODO: Allow?
            return (Value(s) for s in value.value)
        else:
            raise WizardTypeError(f"Cannot iterable over value of type {value.type}.")

    def visitIfStmt(self, ctx: wizardParser.IfStmtContext):
        if self._evisitor.visitExpr(ctx.expr()):
            self.visitBody(ctx.body())
        else:
            for eifc in ctx.elifStmt():
                if self._evisitor.visitExpr(eifc.expr()):
                    self.visitBody(eifc.body())
                    return

            if ctx.elseStmt():
                self.visitBody(ctx.elseStmt().body())

    def visitSelectStmt(self, ctx: wizardParser.SelectStmtContext):
        one = False
        ctxx: Union[wizardParser.SelectOneContext, wizardParser.SelectManyContext]
        if ctx.selectOne():
            one = True
            ctxx = ctx.selectOne()
        else:
            one = False
            ctxx = ctx.selectMany()

        # Parse the description and option:
        desc = self._evisitor.visitExpr(ctxx.expr())
        vopts: List[Tuple[Value, Value, Value]] = []
        for opt in ctxx.optionTuple():
            vopts.append(
                (
                    self._evisitor.visitExpr(opt.expr(0)),
                    self._evisitor.visitExpr(opt.expr(1)),
                    self._evisitor.visitExpr(opt.expr(2)),
                )
            )

        # Check the types:
        if not isinstance(desc.value, str):
            raise WizardTypeError("Description should be a string.")

        opts: List[SelectOption] = []
        defs: List[SelectOption] = []
        for a, b, c in vopts:
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
                raise WizardTypeError(
                    "Cannot have multiple default values with SelectOne."
                )
            sopts = [
                self._manager.selectOne(desc.value, opts, defs[0] if defs else opts[0])
            ]
        else:
            sopts = self._manager.selectMany(desc.value, opts, defs)

        found: bool = False

        for case in ctxx.selectCaseList().caseStmt():
            target = self._evisitor.visitExpr(case.expr())
            if not isinstance(target.value, str):
                raise WizardTypeError(
                    f"Case label should be string, not {target.type}."
                )

            if any(sopt.name == target.value for sopt in sopts):
                found = True
                self.visitBody(case.body())

        if not found and ctxx.selectCaseList().defaultStmt():
            self.visitBody(ctxx.selectCaseList().defaultStmt().body())
