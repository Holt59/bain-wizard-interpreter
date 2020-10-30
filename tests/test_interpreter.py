# -*- encoding: utf-8 -*-

import pytest  # noqa: F401

from wizard.errors import WizardTypeError, WizardNameError
from wizard.expr import SubPackages, Value

from .test_utils import InterpreterChecker, MockSubPackage, MockManager


def test_basic():

    c = InterpreterChecker(MockManager(), SubPackages([]), {},)

    # Test 1:
    s = """
x = 3
4 + 5
x += 4
"""
    c.parse(s)
    assert c._variables == {"x": Value(7)}


def test_forloop():

    c = InterpreterChecker(
        MockManager(),
        SubPackages(
            [
                MockSubPackage("ab", ["a", "x/y", "b"]),
                MockSubPackage("ef", ["b", "u", "c/d"]),
            ]
        ),
        {},
    )

    # Test 1:
    s = """
x = 1
For i from 0 to 4
    x += 1
EndFor
"""
    c.parse(s)
    assert c._variables == {"x": Value(6)}

    # Test 2:
    c.clear()
    s = """
s = ""
For pkg in SubPackages
    s += pkg
EndFor
"""
    c.parse(s)
    assert c._variables == {"s": Value("abef")}

    # Test 3:
    c.clear()
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
    c.parse(s)
    assert c._variables == {"c": Value(40)}
    assert values == [(i, j) for i in range(1, 5) for j in range(1, 5, 2)]


def test_whileloop():

    c = InterpreterChecker(MockManager(), SubPackages([]), {},)

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
    c.parse(s)
    assert c._variables == {"u": Value("5461"), "i": 4, "x": 5461}

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
    c.parse(s)
    assert c._variables["input"] == Value(6174)


def test_if():

    c = InterpreterChecker(MockManager(), SubPackages([]), {})

    s = """
If True
    x = 1
Else
    x = 2
EndIf
"""
    c.parse(s)
    assert c._variables == {"x": Value(1)}

    s = """
If False
    x = 1
Else
    x = 2
EndIf
"""
    c.parse(s)
    assert c._variables == {"x": Value(2)}

    c.clear()
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
    c.parse(s)
    assert c._variables == {"x": Value(1), "y": Value(3), "u": Value(2)}

    c.clear()
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
    c.parse(s)
    assert c._variables == {"x": Value(1), "y": Value(3), "u": Value(5)}


def test_select():

    m = MockManager()
    c = InterpreterChecker(m, SubPackages([]), {})

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
    m.onSelect("O1")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(2)}

    m.onSelect("O2")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(3)}

    # First option is selected by default, the "Default" case is... Useless?
    m.onSelect("OX")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(2)}

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
    m.onSelect([])
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(16)}

    m.onSelect(["O1"])
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(3)}

    m.onSelect(["O2"])
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(4)}

    m.onSelect(["O1", "O2"])
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(6)}

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
    m.onSelect("O1")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(4)}

    m.onSelect("O2")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(3)}

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
    m.onSelect("O1")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(6)}

    m.onSelect("O2")
    c.clear()
    c.parse(s)
    assert c._variables == {"x": Value(4)}


def test_default_functions():

    c = InterpreterChecker(MockManager(), SubPackages([]), {})

    c.parse("s = int('3')")
    assert c._variables["s"] == Value(3)

    c.parse("s = len('hello world')")
    assert c._variables["s"] == Value(11)

    c.parse("s = 'hello world'.len()")
    assert c._variables["s"] == Value(11)


def test_exceptions():

    c = InterpreterChecker(MockManager(), SubPackages([]), {})

    with pytest.raises(WizardTypeError):
        c.parse("s == int(1, 2, 3)")

    with pytest.raises(WizardTypeError):
        c.parse("c == int()")

    with pytest.raises(WizardTypeError):
        c.parse("1 + '2'")

    with pytest.raises(WizardNameError):
        c.parse("foo(1, 2, 3)")

    with pytest.raises(WizardNameError):
        c.parse("x += 2")
