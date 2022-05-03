# -*- encoding: utf-8 -*-

import pytest  # noqa: F401

from wizard.contexts import WizardSelectContext, WizardTerminationContext
from wizard.errors import WizardNameError, WizardParseError, WizardTypeError
from wizard.expr import SubPackages, Value
from wizard.manager import SelectOption

from .test_utils import InterpreterChecker, MockSubPackage, RunnerChecker


def test_basic():

    c = InterpreterChecker()

    # Test 1:
    s = """
x = 3
4 + 5
x += 4
"""
    ctx = c.run(s)
    assert ctx.state.variables == {"x": Value(7)}


def test_forloop():

    subpackages = SubPackages(
        [
            MockSubPackage("ab", ["a", "x/y", "b"]),
            MockSubPackage("ef", ["b", "u", "c/d"]),
        ]
    )
    c = InterpreterChecker(subpackages)

    # Test 1:
    s = """
x = 1
For i from 0 to 4
    x += 1
EndFor
"""
    r = c.run(s)
    assert r.state.variables == {"x": Value(6), "i": Value(4)}

    # Test 2:
    s = """
s = ""
For pkg in SubPackages
    s += str(pkg)
EndFor
"""
    r = c.run(s)
    assert r.state.variables == {"s": Value("abef"), "pkg": Value(subpackages[-1])}

    # Test 3:
    values = []
    c._factory.evisitor._functions["fn"] = lambda st, vs: values.append(
        (vs[0].value, vs[1].value)
    )
    s = """
c = 0
For i from 1 to 4
    For j from 1 to 4 by 2
        fn(i, j)
        c += i * j
    EndFor
EndFor
"""
    r = c.run(s)
    assert r.state.variables == {"c": Value(40), "i": Value(4), "j": Value(3)}
    assert values == [(i, j) for i in range(1, 5) for j in range(1, 5, 2)]


def test_whileloop():

    c = InterpreterChecker()

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
    r = c.run(s)
    assert r.state.variables == {"u": Value("5461"), "i": 4, "x": 5461}

    # Kaprekar number, yay!
    c._factory.evisitor._functions["sort"] = lambda st, vs: Value(
        "".join(sorted(vs[0].value))
    )
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
    r = c.run(s)
    assert r.state.variables["input"] == Value(6174)


def test_if():

    c = InterpreterChecker()

    s = """
If True
    x = 1
Else
    x = 2
EndIf
"""
    r = c.run(s)
    assert r.state.variables == {"x": Value(1)}

    s = """
If False
    x = 1
Else
    x = 2
EndIf
"""
    r = c.run(s)
    assert r.state.variables == {"x": Value(2)}

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
    r = c.run(s)
    assert r.state.variables == {"x": Value(1), "y": Value(3), "u": Value(2)}

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
    r = c.run(s)
    assert r.state.variables == {"x": Value(1), "y": Value(3), "u": Value(5)}


def test_select():

    runner = RunnerChecker()

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

    context = runner.make_top_level_context(s)
    context: WizardSelectContext = runner.exec_until(context, (WizardSelectContext,))
    assert isinstance(context, WizardSelectContext)
    assert len(context.options) == 2

    runner.onSelect("O1")
    _, r = runner.run(s)
    assert r.variables == {"x": Value(2)}

    runner.onSelect("O2")
    _, r = runner.run(s)
    assert r.variables == {"x": Value(3)}

    # First option is selected by default, the "Default" case is... Useless?
    runner.onSelect("OX")
    _, r = runner.run(s)
    assert r.variables == {"x": Value(2)}

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
    _, r = runner.run(s)
    assert r.variables == {"x": Value(16)}

    runner.onSelect(["O1"])
    _, r = runner.run(s)
    assert r.variables == {"x": Value(3)}

    runner.onSelect(["O2"])
    _, r = runner.run(s)
    assert r.variables == {"x": Value(4)}

    runner.onSelect(["O1", "O2"])
    _, r = runner.run(s)
    assert r.variables == {"x": Value(6)}

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
    _, r = runner.run(s)
    assert r.variables == {"x": Value(4)}

    runner.onSelect("O2")
    _, r = runner.run(s)
    assert r.variables == {"x": Value(3)}

    # Defaults
    s = r"""
x = 1
SelectOne "The Description",
    "O1", "Description O1", "ImgO1", \
    "|O2", "Description O2", "ImgO2"
Case "O1"
    x += 2
Case "O2"
    x += 3
    Break
EndSelect
"""

    context = runner.make_top_level_context(s)
    context: WizardSelectContext = runner.exec_until(context, (WizardSelectContext,))
    assert isinstance(context, WizardSelectContext)
    assert context.options == [
        SelectOption("O1", "Description O1", "ImgO1"),
        SelectOption("O2", "Description O2", "ImgO2"),
    ]
    assert context.default == context.options[1]

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
    _, r = runner.run(s)
    assert r.variables == {"x": Value(6)}

    runner.onSelect("O2")
    _, r = runner.run(s)
    assert r.variables == {"x": Value(4)}


def test_default_functions():

    c = InterpreterChecker()

    r = c.run("s = int('3')")
    assert r.state.variables["s"] == Value(3)

    r = c.run("s = len('hello world')")
    assert r.state.variables["s"] == Value(11)

    r = c.run("s = 'hello world'.len()")
    assert r.state.variables["s"] == Value(11)


def test_cancel():
    c = InterpreterChecker()

    s = """
Cancel
"""
    ctx = c.run(s)
    assert isinstance(ctx, WizardTerminationContext)
    assert ctx.is_cancel()
    assert ctx.message() is None

    s = """
Cancel "Cancel."
"""
    ctx = c.run(s)
    assert isinstance(ctx, WizardTerminationContext)
    assert ctx.is_cancel()
    assert ctx.message() == "Cancel."


def test_exec():

    c = InterpreterChecker()

    s = """
a = 1
Exec("a = 3")
a += 2
"""
    ctx = c.run(s)
    assert ctx.state.variables == {"a": Value(5)}

    with pytest.raises(WizardTypeError):
        c.run("""Exec(0)""")
    with pytest.raises(WizardTypeError):
        c.run("""Exec()""")
    with pytest.raises(WizardTypeError):
        c.run("""Exec("a = 3", "b = 4")""")
    with pytest.raises(WizardTypeError):
        c.run("""Exec()""")


def test_exceptions():

    c = InterpreterChecker()

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

    with pytest.raises(WizardTypeError):
        c.run("Cancel 2 + 3")

    with pytest.raises(WizardNameError) as ne:
        c.run("a++")
    assert ne.value.line == 1
    assert ne.value.column == 0
    assert str(ne.value) == "Line 1, Column 0: The name 'a' is not defined."

    with pytest.raises(WizardTypeError) as te:
        c.run(
            """x = 1
s = 2
x += str(s)
"""
        )
    assert te.value.line == 3


def test_recover():

    c = InterpreterChecker()

    # Note: This is actually parsed as "If True.a = False", hence this matches
    # a member-function, and the parser expects "True.a(...)".
    with pytest.raises(WizardParseError) as te:
        c.run(
            """If True
.a = False
Else
a = 10
EndIf
"""
        )
    assert te.value.line == 1

    # Should recover from the broken line:
    ctx = c.run(
        """
If False
    a .= False  ; broken
Else
    a = 10
EndIf
"""
    )
    assert ctx.state.variables == {"a": Value(10)}

    # Should recover from the broken line:
    ctx = c.run(
        """
a = 1
If False
    a .= False  ; broken
Elif a > 4
    b = "For" 4 65  ; broken
Else
    a = 10
EndIf
"""
    )
    assert ctx.state.variables == {"a": Value(10)}
