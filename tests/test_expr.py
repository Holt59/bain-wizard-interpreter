# -*- encoding: utf-8 -*-

import pytest

from antlr4 import InputStream, CommonTokenStream
from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser


from wizard.expr import WizardExpressionVisitor, SubPackages, Value, VariableType
from wizard.errors import WizardNameError, WizardTypeError


class ExpressionChecker(WizardExpressionVisitor):
    def parse(self, expr: str) -> Value:
        input_stream = InputStream(expr)
        lexer = wizardLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        return self.visitExpr(parser.parseWizard().body().expr(0))


def test_constant():

    c = ExpressionChecker({}, SubPackages([]), {})

    # Bool values:
    assert c.parse("False") == Value(False)
    assert c.parse("True") == Value(True)

    # SubPackages:
    assert c.parse("SubPackages") == Value(c._subpackages)

    # Int values:
    assert c.parse("0") == Value(0)
    assert c.parse("1") == Value(1)
    assert c.parse("-3") == Value(-3)

    # Float values:
    v1 = c.parse("1.5")
    assert v1.type == VariableType.FLOAT
    assert v1.value == pytest.approx(1.5)

    v2 = c.parse("-1.3")
    assert v2.type == VariableType.FLOAT
    assert v2.value == pytest.approx(-1.3)

    # String values:
    assert c.parse('""') == Value("")
    assert c.parse("''") == Value("")
    assert c.parse('"hello world"') == Value("hello world")


def test_add_minus():

    c = ExpressionChecker(
        {"x": Value(4), "y": Value(-3), "s": Value("hello"), "b": Value(False)},
        SubPackages([]),
        {},
    )

    # Constant / Ints.
    assert c.parse("-3") == Value(-3)
    assert c.parse("3 + 4") == Value(7)
    assert c.parse("2 - 7") == Value(-5)
    assert c.parse("-7") == Value(-7)
    assert c.parse("2 - 7 + 4 - 3 + 2") == Value(-2)

    # Constants / Strings.
    assert c.parse("'hello' + ' world'") == Value("hello world")
    assert c.parse("'a' + 'b' + 'c'") == Value("abc")

    # Variables / Ints.
    assert c.parse("-x") == Value(-4)
    assert c.parse("-y") == Value(3)
    assert c.parse("x + 2") == Value(6)
    assert c.parse("x + y - 3") == Value(-2)

    # Variables / Strings.
    assert c.parse("s + ' ' + 'world'") == Value("hello world")

    # Errors:
    with pytest.raises(WizardTypeError):
        c.parse("s + 3")
    with pytest.raises(WizardTypeError):
        c.parse("x + 'a'")


def test_increment_decrement():

    c = ExpressionChecker({"x": Value(0), "y": Value(0)}, SubPackages([]), {})

    assert c.parse("x++") == Value(1)
    assert c._variables["x"] == Value(1)

    assert c.parse("x++") == Value(2)
    assert c._variables["x"] == Value(2)

    assert c.parse("--x") == Value(1)
    assert c._variables["x"] == Value(1)

    assert c.parse("y--") == Value(-1)
    assert c._variables["y"] == Value(-1)


def test_functions():

    c = ExpressionChecker(
        {},
        SubPackages([]),
        {
            "nargs": lambda vs: len(vs),
            "add": lambda vs: sum(vs, Value(type(vs[0].value)())),
            "string.trim": lambda vs: Value(vs[0]._value.strip()),
        },
    )

    assert c.parse("nargs()") == Value(0)
    assert c.parse("nargs(3)") == Value(1)
    assert c.parse("nargs(1, 3)") == Value(2)
    assert c.parse("nargs(False, SubPackages, 3)") == Value(3)

    assert c.parse("add(1, 2)") == Value(3)
    assert c.parse("add('hello', ' ', 'world')") == Value("hello world")

    with pytest.raises(WizardTypeError):
        c.parse("add('hello', 3)")

    assert c.parse("'  hello  '.trim()") == Value("hello")

    with pytest.raises(WizardNameError) as ex:
        c.parse("fn()")
    assert ex.value.name == "fn"
