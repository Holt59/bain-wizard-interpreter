# -*- encoding: utf-8 -*-

import codecs
import re
from typing import Callable, List, Mapping, Optional, Type, overload

from .antlr4.wizardParser import wizardParser
from .errors import WizardIndexError, WizardNameError, WizardParseError, WizardTypeError
from .severity import Issue, SeverityContext
from .state import WizardInterpreterState
from .value import (  # noqa: F401
    SubPackage,
    SubPackages,
    Value,
    ValueType,
    VariableType,
    Void,
)


class WizardExpressionVisitor:

    """
    Visitor for Wizard expression. This visitor can be used to interpret Wizard
    expression and return `Value` object. The main entry point is `visitExpr()`
    which takes an expression context and returns a `Value`.
    """

    BAD_ESCAPE_SEQUENCE = re.compile(r"(^|(?<=[^\\]))\\(?=[^abfnrtuUx0-7\\])")

    _subpackages: SubPackages
    _functions: Mapping[str, Callable[[WizardInterpreterState, List[Value]], Value]]
    _severity: SeverityContext

    def __init__(
        self,
        subpackages: SubPackages,
        functions: Mapping[str, Callable[[WizardInterpreterState, List[Value]], Value]],
        severity: SeverityContext,
    ):
        """
        Args:
            subpackages: The subpackages for the visitor.
            functions: The list of usable functions.
            severity: The severity context.
        """
        self._subpackages = subpackages
        self._functions = functions
        self._severity = severity

    def visitTimesDivideModulo(
        self,
        ctx: wizardParser.TimesDivideModuloContext,
        state: WizardInterpreterState,
    ) -> Value:
        op: Callable[[Value, Value], Value] = Value.__mul__
        if ctx.Divide():
            op = Value.__div__
        elif ctx.Modulo():
            op = Value.__mod__
        return op(
            self.visitExpr(ctx.expr(0), state),
            self.visitExpr(ctx.expr(1), state),
        )

    def visitPlusMinus(
        self, ctx: wizardParser.PlusMinusContext, state: WizardInterpreterState
    ) -> Value:
        op: Callable[[Value, Value], Value] = Value.__add__
        if ctx.Minus():
            op = Value.__sub__
        return op(
            self.visitExpr(ctx.expr(0), state),
            self.visitExpr(ctx.expr(1), state),
        )

    def visitOr(
        self, ctx: wizardParser.OrContext, state: WizardInterpreterState
    ) -> Value:
        return self.visitExpr(ctx.expr(0), state) | self.visitExpr(ctx.expr(1), state)

    def visitFunctionCall(
        self,
        ctx: wizardParser.FunctionCallContext,
        state: WizardInterpreterState,
    ) -> Value:

        name = ctx.Identifier().getText()

        # Specific handle for Exec:
        if name == "Exec":
            raise WizardNameError(ctx, "Exec() cannot be used in a complex expression.")
        if name == "EndExec":
            raise WizardNameError(ctx, "EndExec() should not be used explicitly.")

        function: Callable[[WizardInterpreterState, List[Value]], Value]
        if name in self._functions:
            function = self._functions[name]
            is_visit = False
        elif hasattr(self, "visit" + name):
            function = getattr(self, "visit" + name)
            is_visit = True
        else:
            raise WizardNameError(ctx, name)

        values: List[Value] = []
        if ctx.argList():
            for ex in ctx.argList().expr():
                values.append(self.visitExpr(ex, state))

        if is_visit:
            return Value(function(state, *(value.value for value in values)))
        return function(state, values)

    def visitDotFunctionCall(
        self,
        ctx: wizardParser.DotFunctionCallContext,
        state: WizardInterpreterState,
    ) -> Value:
        values: List[Value] = [self.visitExpr(ctx.expr(), state)]

        mname = "{}.{}".format(values[0].type, ctx.Identifier().getText())
        if mname not in self._functions:
            raise WizardNameError(ctx, mname)

        if ctx.argList():
            for ex in ctx.argList().expr():
                values.append(self.visitExpr(ex, state))

        return self._functions[mname](state, values)

    def visitIn(
        self, ctx: wizardParser.InContext, state: WizardInterpreterState
    ) -> Value:
        return self.visitExpr(ctx.expr(1), state).contains(
            self.visitExpr(ctx.expr(0), state), bool(ctx.Colon())
        )

    def doCmp(
        self,
        op: Callable[[Value, Value], Value],
        lhs: Value,
        rhs: Value,
        case_insensitive: bool = True,
    ) -> Value:
        if case_insensitive:
            if not isinstance(lhs.value, str) or not isinstance(rhs.value, str):
                raise WizardTypeError(
                    "Cannot use case-insensitive comparison with values of type"
                    f" {lhs.type}, {rhs.type}."
                )
            lhs = Value(lhs.value.lower())
            rhs = Value(rhs.value.lower())
        return op(lhs, rhs)

    def visitEqual(
        self, ctx: wizardParser.EqualContext, state: WizardInterpreterState
    ) -> Value:
        op = Value.equals
        if ctx.NotEqual():
            op = Value.not_equals
        return self.doCmp(
            op,
            self.visitExpr(ctx.expr(0), state),
            self.visitExpr(ctx.expr(1), state),
            bool(ctx.Colon()),
        )

    def visitLesser(
        self, ctx: wizardParser.LesserContext, state: WizardInterpreterState
    ) -> Value:
        op = Value.__le__
        if ctx.Lesser():
            op = Value.__lt__
        return self.doCmp(
            op,
            self.visitExpr(ctx.expr(0), state),
            self.visitExpr(ctx.expr(1), state),
            bool(ctx.Colon()),
        )

    def visitGreater(
        self, ctx: wizardParser.GreaterContext, state: WizardInterpreterState
    ) -> Value:
        op = Value.__ge__
        if ctx.Greater():
            op = Value.__gt__
        return self.doCmp(
            op,
            self.visitExpr(ctx.expr(0), state),
            self.visitExpr(ctx.expr(1), state),
            bool(ctx.Colon()),
        )

    def visitExponentiation(
        self,
        ctx: wizardParser.ExponentiationContext,
        state: WizardInterpreterState,
    ) -> Value:
        return self.visitExpr(ctx.expr(0), state) ** self.visitExpr(ctx.expr(1), state)

    def visitIndex(
        self, ctx: wizardParser.IndexContext, state: WizardInterpreterState
    ) -> Value:
        return self.visitExpr(ctx.expr(0), state)[self.visitExpr(ctx.expr(1), state)]

    def visitPreDecrement(
        self,
        ctx: wizardParser.PreDecrementContext,
        state: WizardInterpreterState,
    ) -> Value:
        name = ctx.Identifier().getText()
        if name not in state._variables:
            raise WizardNameError(ctx, name)
        state._variables[ctx.Identifier().getText()] -= Value(1)
        return state._variables[ctx.Identifier().getText()]

    def visitPreIncrement(
        self,
        ctx: wizardParser.PreIncrementContext,
        state: WizardInterpreterState,
    ) -> Value:
        name = ctx.Identifier().getText()
        if name not in state._variables:
            raise WizardNameError(ctx, name)
        state._variables[ctx.Identifier().getText()] += Value(1)
        return state._variables[ctx.Identifier().getText()]

    def visitPostIncrement(
        self,
        ctx: wizardParser.PostIncrementContext,
        state: WizardInterpreterState,
    ) -> Value:
        name = ctx.Identifier().getText()
        if name not in state._variables:
            raise WizardNameError(ctx, name)
        state._variables[ctx.Identifier().getText()] += Value(1)
        return state._variables[ctx.Identifier().getText()]

    def visitPostDecrement(
        self,
        ctx: wizardParser.PostDecrementContext,
        state: WizardInterpreterState,
    ) -> Value:
        name = ctx.Identifier().getText()
        if name not in state._variables:
            raise WizardNameError(ctx, name)
        state._variables[ctx.Identifier().getText()] -= Value(1)
        return state._variables[ctx.Identifier().getText()]

    def visitNegative(
        self, ctx: wizardParser.NegativeContext, state: WizardInterpreterState
    ) -> Value:
        return -self.visitExpr(ctx.expr(), state)

    def visitNot(
        self, ctx: wizardParser.NotContext, state: WizardInterpreterState
    ) -> Value:
        return self.visitExpr(ctx.expr(), state).logical_not()

    def visitParenExpr(
        self, ctx: wizardParser.ParenExprContext, state: WizardInterpreterState
    ) -> Value:
        return self.visitExpr(ctx.expr(), state)

    def visitSlice(
        self, ctx: wizardParser.SliceContext, state: WizardInterpreterState
    ) -> Value:
        # expr LeftBracket expr? Colon expr? (Colon expr?)? RightBracket
        lhs = self.visitExpr(ctx.expr(0), state)

        start: Optional[Value] = None
        end: Optional[Value] = None
        step: Optional[Value] = None

        # Index of end expression in ctx.children (without start by
        # default):
        cidx: int = 3

        # Is there a start?
        if isinstance(ctx.children[2], wizardParser.ExprContext):
            start = self.visitExpr(ctx.expr(1), state)
            cidx = 4

        # Is there and end?
        if isinstance(ctx.children[cidx], wizardParser.ExprContext):
            end = self.visitExpr(ctx.children[cidx], state)

        # Is there a step?
        if ctx.Colon(1) and isinstance(ctx.children[-2], wizardParser.ExprContext):
            step = self.visitExpr(ctx.children[-2], state)

        # We keep None and let python built-in slice() do the job for us.
        return lhs.slice(start, end, step)

    def visitAnd(
        self, ctx: wizardParser.AndContext, state: WizardInterpreterState
    ) -> Value:
        lhs, rhs = self.visitExpr(ctx.expr(0), state), self.visitExpr(
            ctx.expr(1), state
        )
        return lhs & rhs

    def visitValue(
        self, ctx: wizardParser.ValueContext, state: WizardInterpreterState
    ) -> Value:
        if ctx.constant():
            return self.visitConstant(ctx.constant())
        if ctx.integer():
            return self.visitInteger(ctx.integer())
        if ctx.decimal():
            return self.visitDecimal(ctx.decimal())
        if ctx.string():
            return self.visitString(ctx.string())
        if ctx.Identifier():
            name = ctx.Identifier().getText()
            if name not in state._variables:
                # Severity check:
                self._severity.raise_or_warn(
                    Issue.USAGE_OF_NOTSET_VARIABLES,
                    WizardNameError(ctx, name),
                    f"Variable {name} used before being set, default to 0.",
                )
                return Value(0)
            else:
                return state._variables[ctx.Identifier().getText()]

        raise WizardNameError(ctx, ctx.getText())

    def visitConstant(self, ctx: wizardParser.ConstantContext) -> Value:
        if ctx.getText() == "False":
            return Value(False)
        elif ctx.getText() == "True":
            return Value(True)
        else:
            return Value(self._subpackages)

    def visitInteger(self, ctx: wizardParser.IntegerContext) -> Value:
        return Value(int(ctx.getText()))

    def visitDecimal(self, ctx: wizardParser.DecimalContext) -> Value:
        return Value(float(ctx.getText()))

    def visitString(self, ctx: wizardParser.StringContext) -> Value:
        # Remove the quotation marks:
        txt = ctx.getText()[1:-1]

        # Remove bad escape sequences:
        txt = self.BAD_ESCAPE_SEQUENCE.sub("", txt)

        # Replace escape sequences by Python escape sequences:
        txt = codecs.decode(txt, "unicode_escape")

        return Value(txt)

    @overload
    def visitExpr(
        self, ctx: wizardParser.ExprContext, state: WizardInterpreterState
    ) -> Value:
        ...

    @overload
    def visitExpr(
        self,
        ctx: wizardParser.ExprContext,
        state: WizardInterpreterState,
        typ: Type[ValueType],
    ) -> Value[ValueType]:
        ...

    def visitExpr(
        self,
        ctx: wizardParser.ExprContext,
        state: WizardInterpreterState,
        typ: Optional[Type[ValueType]] = None,
    ):
        """
        Evaluate the given expression.

        IMPORTANT: This method can modify the state.

        Args:
            ctx: The expression context to evaluate.
            state: The list of state (can be modified).
            typ: The type of the value to return.

        Returns:
            The result of the given expression.
        """

        if ctx.exception:
            raise WizardParseError(ctx, ctx.exception)

        try:
            value = getattr(self, "visit" + type(ctx).__name__[:-7])(ctx, state)
        except TypeError as te:
            raise WizardTypeError(ctx, *te.args)
        except IndexError as ie:
            raise WizardIndexError(ctx, *ie.args)

        if typ is not None and not isinstance(value.value, typ):
            raise WizardTypeError(
                ctx,
                f"Expected value of type {VariableType.from_pytype(typ)} but got value"
                f" of type {value.type}.",
            )

        return value  # type: ignore
