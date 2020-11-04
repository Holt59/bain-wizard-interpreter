# -*- encoding: utf-8 -*-

import pytest  # noqa: F401

from wizard.errors import WizardTypeError, WizardNameError
from wizard.expr import SubPackages, Value
from wizard.interpreter import WizardInterpreterResult

from .test_utils import MockRunner, MockSubPackage


def test_basic():

    c = MockRunner(SubPackages([]))

    # Test 1:
    s = """
x = 3
4 + 5
x += 4
"""
    c.run(s)
    assert c.variables == {"x": Value(7)}


def test_forloop():

    c = MockRunner(
        SubPackages(
            [
                MockSubPackage("ab", ["a", "x/y", "b"]),
                MockSubPackage("ef", ["b", "u", "c/d"]),
            ]
        )
    )

    # Test 1:
    s = """
x = 1
For i from 0 to 4
    x += 1
EndFor
"""
    c.run(s)
    assert c.variables == {"x": Value(6)}

    # Test 2:
    s = """
s = ""
For pkg in SubPackages
    s += str(pkg)
EndFor
"""
    c.run(s)
    assert c.variables == {"s": Value("abef")}

    # Test 3:
    values = []
    c._functions["fn"] = lambda vs: values.append((vs[0].value, vs[1].value))
    s = """
c = 0
For i from 1 to 4
    For j from 1 to 4 by 2
        fn(i, j)
        c += i * j
    EndFor
EndFor
"""
    c.run(s)
    assert c.variables == {"c": Value(40)}
    assert values == [(i, j) for i in range(1, 5) for j in range(1, 5, 2)]


def test_whileloop():

    c = MockRunner(SubPackages([]))

    # Test 1:
    s = """
u = "5461"
x = 0
i = 0
While i < len(u)
    x = 10 * x + int(u[i])
    i += 1
EndWhile
"""
    c.run(s)
    assert c.variables == {"u": Value("5461"), "i": 4, "x": 5461}

    # Kaprekar number, yay!
    c._functions["sort"] = lambda vs: Value("".join(sorted(vs[0].value)))
    s = """
input = 3524
target = 6174

While input != target
    input_i = sort(str(input))
    input_d = ""
    For i from 1 to len(input_i)
        input_d += input_i[len(input_i) - i]
    EndFor
    input = int(input_d) - int(input_i)
EndWhile
"""
    c.run(s)
    assert c.variables["input"] == Value(6174)


def test_if():

    c = MockRunner(SubPackages([]))

    s = """
If True
    x = 1
Else
    x = 2
EndIf
"""
    c.run(s)
    assert c.variables == {"x": Value(1)}

    s = """
If False
    x = 1
Else
    x = 2
EndIf
"""
    c.run(s)
    assert c.variables == {"x": Value(2)}

    s = """
x = 1
y = 3
If x != 1
    u = 1
Elif y == 3
    u = 2
Else
    u = 3
EndIf
"""
    c.run(s)
    assert c.variables == {"x": Value(1), "y": Value(3), "u": Value(2)}

    s = """
x = 1
y = 3
If x != 1
    u = 1
Elif y == 2
    u = 2
Elif x + y == 4
    u = 5
EndIf
"""
    c.run(s)
    assert c.variables == {"x": Value(1), "y": Value(3), "u": Value(5)}


def test_select():

    runner = MockRunner(SubPackages([]))

    s = r"""
x = 1
SelectOne "The Description",
    "O1", "Description O1", "ImgO1", \
    "O2", "Description O2", "ImgO2"
Case "O1"
    x = 2
    Break
Case "O2"
    x = 3
    Break
Default
    x = 4
    Break
EndSelect
"""
    runner.onSelect("O1")
    runner.run(s)
    assert runner.variables == {"x": Value(2)}

    runner.onSelect("O2")
    runner.run(s)
    assert runner.variables == {"x": Value(3)}

    # First option is selected by default, the "Default" case is... Useless?
    runner.onSelect("OX")
    runner.run(s)
    assert runner.variables == {"x": Value(2)}

    s = r"""
x = 1
SelectMany "The Description",
    "O1", "Description O1", "ImgO1", \
    "O2", "Description O2", "ImgO2"
Case "O1"
    x += 2
    Break
Case "O2"
    x += 3
    Break
Default
    x += 15
EndSelect
"""
    runner.onSelect([])
    runner.run(s)
    assert runner.variables == {"x": Value(16)}

    runner.onSelect(["O1"])
    runner.run(s)
    assert runner.variables == {"x": Value(3)}

    runner.onSelect(["O2"])
    runner.run(s)
    assert runner.variables == {"x": Value(4)}

    runner.onSelect(["O1", "O2"])
    runner.run(s)
    assert runner.variables == {"x": Value(6)}

    # No Case for selected:
    s = r"""
x = 1
SelectOne "The Description",
    "O1", "Description O1", "ImgO1", \
    "O2", "Description O2", "ImgO2"
Case "O2"
    x = 3
    Break
Default
    x = 4
    Break
EndSelect
"""
    runner.onSelect("O1")
    runner.run(s)
    assert runner.variables == {"x": Value(4)}

    runner.onSelect("O2")
    runner.run(s)
    assert runner.variables == {"x": Value(3)}

    # Fallthrough
    s = r"""
x = 1
SelectOne "The Description",
    "O1", "Description O1", "ImgO1", \
    "O2", "Description O2", "ImgO2"
Case "O1"
    x += 2
Case "O2"
    x += 3
    Break
EndSelect
"""
    runner.onSelect("O1")
    runner.run(s)
    assert runner.variables == {"x": Value(6)}

    runner.onSelect("O2")
    runner.run(s)
    assert runner.variables == {"x": Value(4)}


def test_default_functions():

    c = MockRunner(SubPackages([]))

    c.run("s = int('3')")
    assert c.variables["s"] == Value(3)

    c.run("s = len('hello world')")
    assert c.variables["s"] == Value(11)

    c.run("s = 'hello world'.len()")
    assert c.variables["s"] == Value(11)


def test_abort():

    c = MockRunner(SubPackages([]))

    # Test abort - We should not reach the "c = 10" line:
    c._functions["fn"] = lambda *args: c.abort()
    s = """
x = 1
y = 2
c = x * y
fn(x, y)
c = 10
"""
    assert c.run(s).status == WizardInterpreterResult.CANCEL
    assert c.variables == {"x": Value(1), "y": Value(2), "c": Value(2)}

    # A kind of "while" loop using rewind():
    values = [0]

    def fn(*args):
        values[0] += 1
        if values[0] == 5:
            return Value(5)
        c.rewind(c.state())

    c._functions["fn"] = fn
    s = """
x = fn()
"""
    assert c.run(s).status == WizardInterpreterResult.COMPLETED
    assert c.variables == {"x": Value(5)}

    # A kind of "while" loop using rewind():
    values = {"cnt": 0, "ctx": None}

    def fn1(*args):
        # On rewind(), the value of x should be 1:
        assert c.variables == {"x": Value(1)}
        values["ctx"] = c.state()

    def fn2(*args):
        # In fn2(), the value of x should be 2:
        assert c.variables == {"x": Value(2)}
        values["cnt"] += 1
        if values["cnt"] < 5:
            c.rewind(values["ctx"])

    c._functions["fn1"] = fn1
    c._functions["fn2"] = fn2
    s = """
x = 1
fn1() ; Save the context.
x = 2
fn2() ; Rewind 5 times
"""
    assert c.run(s).status == WizardInterpreterResult.COMPLETED
    assert c.variables == {"x": Value(2)}
    assert values["cnt"] == 5


def test_exceptions():

    c = MockRunner(SubPackages([]))

    with pytest.raises(WizardTypeError):
        c.run("s == int(1, 2, 3)")

    with pytest.raises(WizardTypeError):
        c.run("c == int()")

    with pytest.raises(WizardTypeError):
        c.run("1 + '2'")

    with pytest.raises(WizardNameError):
        c.run("foo(1, 2, 3)")

    with pytest.raises(WizardNameError):
        c.run("x += 2")

    with pytest.raises(WizardTypeError) as te:
        c.run(
            """x = 1
s = 2
x += str(s)
"""
        )
    assert te.value.line == 3
