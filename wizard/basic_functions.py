# -*- encoding: utf-8 -*-

"""
This file contains the implementation of the "basic" functions for BAIN Wizard,
i.e. functions that do not require specific handling.
"""

from .expr import SubPackage, SubPackages, Value


class WizardFunctions:
    def str(self, value: Value) -> Value:
        return Value(str(value.value))

    def int(self, value: Value) -> Value:
        if isinstance(value.value, (SubPackage, SubPackages)):
            return Value(0)
        return Value(int(value.value))

    def float(self, value: Value) -> Value:
        if isinstance(value.value, (SubPackage, SubPackages)):
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
