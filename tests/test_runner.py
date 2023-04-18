# -*- encoding: utf-8 -*-

from wizard.scriptrunner import WizardScriptRunnerStatus
from wizard.value import Value

from .test_utils import RunnerChecker


def test_abort():
    c = RunnerChecker()

    # Test abort - We should not reach the "c = 10" line:
    c._factory._evisitor._functions["fn"] = lambda *args: c.abort()
    s = """
x = 1
y = 2
c = x * y
fn(x, y)
c = 10
"""
    status, result = c.run(s)
    assert status == WizardScriptRunnerStatus.CANCEL
    assert result.variables == {"x": Value(1), "y": Value(2), "c": Value(2)}

    # A kind of "while" loop using rewind():
    values = [0]

    def fn(*args):
        values[0] += 1
        if values[0] == 5:
            return Value(5)
        c.rewind(c.context())

    c._factory._evisitor._functions["fn"] = fn
    s = """
x = fn()
"""
    status, result = c.run(s)
    assert status == WizardScriptRunnerStatus.COMPLETE
    assert result.variables == {"x": Value(5)}

    # A kind of "while" loop using rewind():
    values = {"cnt": 0, "ctx": None}

    def fn1(*args):
        # On rewind(), the value of x should be 1:
        assert c.context().state.variables == {"x": Value(1)}
        values["ctx"] = c.context()

    def fn2(*args):
        # In fn2(), the value of x should be 2:
        assert c.context().state.variables == {"x": Value(2)}
        values["cnt"] += 1
        if values["cnt"] < 5:
            c.rewind(values["ctx"])

    c._factory._evisitor._functions["fn1"] = fn1
    c._factory._evisitor._functions["fn2"] = fn2
    s = """
x = 1
fn1() ; Save the context.
x = 2
fn2() ; Rewind 5 times
"""
    status, result = c.run(s)
    assert status == WizardScriptRunnerStatus.COMPLETE
    assert result.variables == {"x": Value(2)}
    assert values["cnt"] == 5
