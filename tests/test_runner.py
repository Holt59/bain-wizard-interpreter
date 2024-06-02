from collections.abc import Sequence
from typing import Any

from wizard.scriptrunner import WizardScriptRunnerStatus
from wizard.state import WizardInterpreterState
from wizard.value import Value

from .test_utils import RunnerChecker


def test_abort():
    c = RunnerChecker()

    # Test abort - We should not reach the "c = 10" line:
    c.register_function("fn", lambda _st, _vs: c.abort())
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


def test_rewind_1():
    c = RunnerChecker()

    # A kind of "while" loop using rewind():
    values: list[int] = [0]

    def fn(_st: WizardInterpreterState, _vs: Sequence[Value[Any]]):
        values[0] += 1
        if values[0] == 5:
            return Value(5)
        c.rewind(c.context())

    c.register_function("fn", fn)
    s = """
x = fn()
"""
    status, result = c.run(s)
    assert status == WizardScriptRunnerStatus.COMPLETE
    assert result.variables == {"x": Value(5)}


def test_rewind_2():
    c = RunnerChecker()

    # A kind of "while" loop using rewind():
    values: dict[str, Any] = {"cnt": 0, "ctx": None}

    def fn1(_st: WizardInterpreterState, _vs: Sequence[Value[Any]]):
        # On rewind(), the value of x should be 1:
        assert c.context().state.variables == {"x": Value(1)}
        values["ctx"] = c.context()

    def fn2(_st: WizardInterpreterState, _vs: Sequence[Value[Any]]):
        # In fn2(), the value of x should be 2:
        assert c.context().state.variables == {"x": Value(2)}
        values["cnt"] += 1
        if values["cnt"] < 5:
            c.rewind(values["ctx"])

    c.register_function("fn1", fn1)
    c.register_function("fn2", fn2)
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
