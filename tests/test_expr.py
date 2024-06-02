from typing import cast

import pytest

from wizard.errors import WizardIndexError, WizardNameError, WizardTypeError
from wizard.expr import SubPackages, Value, VariableType

from .test_utils import ExpressionChecker, MockSubPackage


def test_constant():
    c = ExpressionChecker()

    # Bool values:
    assert c.parse("False") == Value(False)
    assert c.parse("True") == Value(True)

    # SubPackages:
    assert c.parse("SubPackages") == Value(c._subpackages)  # pyright: ignore[reportPrivateUsage]

    # Int values:
    assert c.parse("0") == Value(0)
    assert c.parse("1") == Value(1)
    assert c.parse("-3") == Value(-3)

    # Float values:
    v1 = c.parse("1.5")
    assert v1.type == VariableType.FLOAT
    assert v1.value == pytest.approx(1.5)  # pyright: ignore[reportUnknownMemberType]

    v2 = c.parse("-1.3")
    assert v2.type == VariableType.FLOAT
    assert v2.value == pytest.approx(-1.3)  # pyright: ignore[reportUnknownMemberType]

    # String values:
    assert c.parse('""') == Value("")
    assert c.parse("''") == Value("")
    assert c.parse('"hello world"') == Value("hello world")
    assert c.parse('"hello\\nworld"') == Value("hello\nworld")
    assert c.parse('"hello\\"world"') == Value('hello"world')
    assert c.parse('"hello\\\'world"') == Value("hello'world")
    assert c.parse('"hello\\\\,world"') == Value("hello\\,world")
    assert c.parse('"\\\\world"') == Value("\\world")
    assert c.parse('"\\"world"') == Value('"world')

    # Bad strings:
    assert c.parse('"hello\\,world"') == Value("hello,world")
    assert c.parse('"\\,world"') == Value(",world")


def test_add_sub():
    c = ExpressionChecker(
        variables={"x": Value(4), "y": Value(-3), "s": Value("hello")}
    )

    # Constant / Integers.
    assert c.parse("-3") == Value(-3)
    assert c.parse("3 + 4") == Value(7)
    assert c.parse("2 - 7") == Value(-5)
    assert c.parse("-7") == Value(-7)
    assert c.parse("2 - 7 + 4 - 3 + 2") == Value(-2)

    # Constants / Strings.
    assert c.parse("'hello' + ' world'") == Value("hello world")
    assert c.parse("'a' + 'b' + 'c'") == Value("abc")

    # Variables / Integers.
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


def test_mul_div_mod_pow():
    c = ExpressionChecker(variables={"x": Value(4), "y": Value(1.3)})

    # Constant:
    assert c.parse("3 * 4") == Value(12)
    assert c.parse("3 * 1.5") == Value(4.5)
    assert c.parse("3 / 2") == Value(1.5)
    assert c.parse("3 % 4") == Value(3)
    assert c.parse("4 % 3") == Value(1)
    assert c.parse("2 ^ 4") == Value(16)

    # Variables:
    assert c.parse("x / 8") == Value(0.5)


def test_increment_decrement():
    c = ExpressionChecker(variables={"x": Value(0), "y": Value(0)})

    assert c.parse("x++") == Value(1)
    assert c.state.variables["x"] == Value(1)

    assert c.parse("x++") == Value(2)
    assert c.state.variables["x"] == Value(2)

    assert c.parse("--x") == Value(1)
    assert c.state.variables["x"] == Value(1)

    assert c.parse("y--") == Value(-1)
    assert c.state.variables["y"] == Value(-1)


def test_containers():
    subpackages = SubPackages(
        [
            MockSubPackage("foo", ["a", "x/y", "b"]),
            MockSubPackage("bar", ["b", "u", "c/d"]),
        ]
    )
    c = ExpressionChecker(subpackages=subpackages)

    assert c.parse("SubPackages") == Value(subpackages)
    assert c.parse("SubPackages[0]") == Value(subpackages[0])
    assert c.parse("SubPackages[1]") == Value(subpackages[1])

    with pytest.raises(WizardIndexError):
        c.parse("SubPackages[10]")

    assert c.parse("SubPackages[0] == 'foo'") == Value(True)
    assert c.parse("SubPackages[0] == 'fo'") == Value(False)

    assert c.parse("'foo' in SubPackages") == Value(True)
    assert c.parse("'bar' in SubPackages") == Value(True)
    assert c.parse("'baz' in SubPackages") == Value(False)


def test_index_and_slice():
    c = ExpressionChecker()

    assert c.parse("'hello world'[0]") == Value("h")
    assert c.parse("'hello world'[10]") == Value("d")
    assert c.parse("'hello world'[-1]") == Value("d")
    assert c.parse("'hello world'[-11]") == Value("h")

    with pytest.raises(WizardIndexError):
        assert c.parse("'hello world'[11]")

    with pytest.raises(WizardIndexError):
        assert c.parse("'hello world'[-12]")

    assert c.parse("'hello world'[:]") == Value("hello world")
    assert c.parse("'hello world'[0:]") == Value("hello world")
    # cSpell:ignore hlowrd
    assert c.parse("'hello world'[0::2]") == Value("hlowrd")

    assert c.parse("'hello world'[:3]") == Value("hel")
    assert c.parse("'hello world'[0:4]") == Value("hell")
    assert c.parse("'hello world'[2:5]") == Value("llo")
    assert c.parse("'hello world'[2:6:2]") == Value("lo")
    assert c.parse("'hello world'[-3:]") == Value("rld")

    # From the "README":
    assert c.parse('"Hello"[0]') == Value("H")
    assert c.parse('"Hello"[2]') == Value("l")
    assert c.parse('"Hello"[0:]') == Value("Hello")
    assert c.parse('"Hello"[:]') == Value("Hello")
    assert c.parse('"Hello"[0:2]') == Value("He")
    assert c.parse('"Hello"[-1]') == Value("o")
    assert c.parse('"Hello"[1:3]') == Value("el")
    assert c.parse('"Hello"[-2:]') == Value("lo")


def test_functions():
    c = ExpressionChecker(
        functions={
            "nargs": lambda _st, vs: Value(len(vs)),
            "add": lambda _st, vs: sum(vs, Value(type(vs[0].value)())),
            "string.trim": lambda _st, vs: Value(cast(str, vs[0].value).strip()),
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

    c.visitFn = lambda st, x: 2 * x  # type: ignore
    assert c.parse("Fn(1)") == Value(2)
