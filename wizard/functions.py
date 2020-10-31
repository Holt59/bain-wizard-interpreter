# -*- encoding: utf-8 -*-

"""
This file contains the implementation of the "basic" functions for BAIN Wizard,
i.e. functions that do not require specific handling.
"""

import inspect

from typing import Dict, Mapping, Callable, List

from .expr import SubPackage, SubPackages, Value, Void
from .mmitf import ModManagerInterface
from .utils import optional, wrap_function
from .severity import Issue, SeverityContext
from .value import VariableType


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


def make_basic_functions() -> Mapping[str, Callable[[List[Value]], Value]]:
    """
    Create a list of basic functions.

    Args:
        wf: The WizardFunctions object to use for the basic functions.

    Returns:
        A mapping from function name to basic functions, including methods.
    """

    wf = WizardFunctions()
    fns: Dict[str, Callable[[List[Value]], Value]] = {}

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
    manager: ModManagerInterface, scontext: SeverityContext
) -> Mapping[str, Callable[[List[Value]], Value]]:
    """
    Add manager functions to the _functions member variables. These functions
    calls method of the manager passed in.

    Args:
        manager: The manager to delete the call to.
        scontext: The severity context to use (for the Note keyword for instance).
    """

    fns: Dict[str, Callable[[List[Value]], Value]] = {}

    for t in [
        # Functions:
        ("CompareGameVersion", manager.compareGameVersion, str),
        ("CompareSEVersion", manager.compareSEVersion, str),
        ("CompareGEVersion", manager.compareGEVersion, str),
        ("CompareWBVersion", manager.compareWBVersion, str),
        ("GetPluginLoadOrder", manager.getPluginLoadOrder, str, optional(int)),
        ("GetPluginStatus", manager.getPluginStatus, str),
        ("GetEspmStatus", manager.getPluginStatus, str),
        ("DisableINILine", manager.disableINILine, str, str, str),
        ("EditINI", manager.editINI, str, str, str, object, optional(str)),
        ("GetFilename", manager.getFilename, str),
        ("GetFolder", manager.getFolder, str),
        # Keywords:
        ("DeSelectAll", manager.deselectAll),
        ("DeSelectAllPlugins", manager.deselectAllPlugins),
        ("DeSelectAllEspms", manager.deselectAllPlugins),
        ("DeSelectPlugin", manager.deselectPlugin, str),
        ("DeSelectEspm", manager.deselectPlugin, str),
        ("DeSelectSubPackage", manager.deselectSubPackage, str),
        ("RenamePlugin", manager.renamePlugin, str, str),
        ("RenameEspm", manager.renamePlugin, str, str),
        (
            "RequireVersions",
            manager.requiresVersions,
            str,
            optional(str),
            optional(str),
            optional(str),
        ),
        ("ResetPluginName", manager.resetPluginName, str),
        ("ResetEspmName", manager.resetPluginName, str),
        ("ResetAllPluginNames", manager.resetAllPluginNames),
        ("ResetAllEspmNames", manager.resetAllPluginNames),
        ("SelectAll", manager.selectAll),
        ("SelectAllPlugins", manager.selectAllPlugins),
        ("SelectAllEspms", manager.selectAllPlugins),
        ("SelectPlugin", manager.selectPlugin, str),
        ("SelectEspm", manager.selectPlugin, str),
        ("SelectSubPackage", manager.selectSubPackage, str),
    ]:
        fns[t[0]] = wrap_function(*t)  # type: ignore

    # Varargs:
    fns["DataFileExists"] = wrap_function(
        "DataFileExists", manager.dataFileExists, str, varargs=True
    )

    # Any type?
    def note(x: object):
        scontext.raise_or_warn(
            Issue.USAGE_OF_ANYTHING_IN_NOTE,
            TypeError(
                "'Note' keyword expected string, found"
                f" {VariableType.from_pytype(type(x))}."
            ),
            "'Note' keyword expected string, found"
            f" {VariableType.from_pytype(type(x))}.",
        )
        return manager.note(str(x))

    fns["Note"] = wrap_function("Note", note, object)

    return fns
