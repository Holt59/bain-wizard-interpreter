# -*- encoding: utf-8 -*-

"""
This file contains the implementation of the "basic" functions for BAIN Wizard,
i.e. functions that do not require specific handling.
"""

import inspect
from typing import Callable, Dict, List, Mapping, Union

from .expr import SubPackage, SubPackages, Value, VariableType, Void
from .manager import ManagerModInterface
from .severity import SeverityContext
from .state import WizardInterpreterState


class WizardFunctions:

    """
    This is simply a class containing all the basic functions.
    """

    def str(self, value: Value) -> Value:
        return Value(str(value.value))

    def int(self, value: Value) -> Value:
        if isinstance(value.value, (SubPackage, SubPackages, Void)):
            return Value(0)
        return Value(int(value.value))

    def float(self, value: Value) -> Value:
        if isinstance(value.value, (SubPackage, SubPackages, Void)):
            return Value(0.0)
        return Value(float(value.value))

    def len(self, value: Value) -> Value:
        if not isinstance(value.value, str):
            return Value(0)
        return Value(len(value.value))

    def startswith(self, value: Value, *args: Value) -> Value:
        if not isinstance(value.value, str):
            return Value(False)
        for prefix in args:
            if not isinstance(prefix.value, str):
                continue
            if value.value.startswith(prefix.value):
                return Value(True)
        return Value(False)

    def endswith(self, value: Value, *args: Value) -> Value:
        if not isinstance(value.value, str):
            return Value(False)
        for prefix in args:
            if not isinstance(prefix.value, str):
                continue
            if value.value.endswith(prefix.value):
                return Value(True)
        return Value(False)

    def lower(self, value: Value) -> Value:
        if not isinstance(value.value, str):
            return value
        return Value(value.value.lower())

    def find(
        self,
        string: Value,
        substring: Value,
        start: Value = Value(0),
        end: Value = Value(-1),
    ) -> Value:
        if (
            not isinstance(string.value, str)
            or not isinstance(substring.value, str)
            or not isinstance(start.value, int)
            or not isinstance(end.value, int)
        ):
            return Value(-1)

        return Value(
            string.value.find(
                substring.value, start.value, end.value if end.value != -1 else None
            )
        )

    def rfind(
        self,
        string: Value,
        substring: Value,
        start: Value = Value(0),
        end: Value = Value(-1),
    ) -> Value:
        if (
            not isinstance(string.value, str)
            or not isinstance(substring.value, str)
            or not isinstance(start.value, int)
            or not isinstance(end.value, int)
        ):
            return Value(-1)

        return Value(
            string.value.rfind(
                substring.value, start.value, end.value if end.value != -1 else None
            )
        )


class optional:
    t: type

    def __init__(self, t: type):
        self.t = t


def wrap_function(
    name: str,
    method,
    *args: Union[optional, type],
    varargs: bool = False,
    rawargs: bool = False,
) -> Callable[[WizardInterpreterState, List[Value]], Value]:

    """
    Wrap the given function to be usable by the Wizard expression visitor.

    Args:
        name: The name of the function, for logging purpose (warning / errors).
        method: The function to wrap.
        *args: The type of arguments expected by the method.
        varargs: True if the method accept any number of arguments.
        rawargs: True if the method accept Value(), False to extract the underlying
            object.
    """

    def fn(st: WizardInterpreterState, vs: List[Value]) -> Value:

        # List of Python arguments:
        pargs: List = []

        if not varargs and len(vs) > len(args):
            raise TypeError(f"{name}: too many arguments.")

        for iarg, arg in enumerate(args):
            if iarg >= len(vs) and not isinstance(arg, optional):
                raise TypeError(f"{name}: missing required positional argument(s).")

            tp: type
            if isinstance(arg, optional):
                tp = arg.t
            else:
                tp = arg

            if not isinstance(vs[iarg].value, tp):
                raise TypeError(
                    f"Argument at position {iarg} has incorrect type for"
                    f" {name}, expected {VariableType.from_pytype(tp)} got"
                    f" {vs[iarg].type}."
                )

            if rawargs:
                pargs.append(vs[iarg])
            else:
                pargs.append(vs[iarg].value)

        ret: Value = method(*pargs)
        if ret is None:
            ret = Void()

        if not rawargs:
            ret = Value(ret)  # type: ignore

        return ret

    return fn


def make_basic_functions() -> Dict[
    str, Callable[[WizardInterpreterState, List[Value]], Value]
]:
    """
    Create a list of basic functions.

    Args:
        wf: The WizardFunctions object to use for the basic functions.

    Returns:
        A mapping from function name to basic functions, including methods.
    """

    wf = WizardFunctions()
    fns: Dict[str, Callable[[WizardInterpreterState, List[Value]], Value]] = {}

    # Add all the free functions:
    for fname in dir(wf):
        if fname.startswith("__"):
            continue
        sig = inspect.signature(getattr(wf, fname))
        varargs = "args" in sig.parameters
        fns[fname] = wrap_function(
            fname,
            getattr(wf, fname),
            *(object for _ in range(len(sig.parameters) - varargs)),
            varargs=varargs,
            rawargs=True,
        )

    # Add methods:
    for fname in dir(wf):
        if fname.startswith("__"):
            continue
        fns["string." + fname] = fns[fname]

    for t in ("integer", "float", "bool"):
        fns[t + ".str"] = fns["str"]

    return fns


def make_manager_functions(
    manager: ManagerModInterface, scontext: SeverityContext
) -> Mapping[str, Callable[[WizardInterpreterState, List[Value]], Value]]:
    """
    Add manager functions to the _functions member variables. These functions
    calls method of the manager passed in.

    Args:
        manager: The manager to delete the call to.
        scontext: The severity context to use (for the Note keyword for instance).
    """

    fns: Dict[str, Callable[[WizardInterpreterState, List[Value]], Value]] = {}

    for t in [
        # Functions:
        ("CompareGameVersion", manager.compareGameVersion, str),
        ("CompareSEVersion", manager.compareSEVersion, str),
        ("CompareGEVersion", manager.compareGEVersion, str),
        ("CompareWBVersion", manager.compareWBVersion, str),
        ("GetPluginLoadOrder", manager.getPluginLoadOrder, str, optional(int)),
        ("GetPluginStatus", manager.getPluginStatus, str),
        ("GetEspmStatus", manager.getPluginStatus, str),
        ("GetFilename", manager.getFilename, str),
        ("GetFolder", manager.getFolder, str),
    ]:
        fns[t[0]] = wrap_function(*t)  # type: ignore

    # Varargs:
    fns["DataFileExists"] = wrap_function(
        "DataFileExists", manager.dataFileExists, str, varargs=True
    )

    return fns
