# -*- encoding: utf-8 -*-

from abc import abstractproperty
from enum import Enum, auto
from typing import (
    List,
    Iterable,
    Optional,
    Sequence,
    Type,
    Union,
)


class Void:

    """
    Simple class representing the result of a function call without a return
    value.
    """

    pass


class SubPackage(str):
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

    @abstractproperty
    def files(self) -> Iterable[str]:
        pass


class SubPackages(List[SubPackage]):

    """
    Class to wrap the 'SubPackages' variable.
    """

    def __init__(self, subpackages: Sequence[SubPackage]):
        super().__init__(subpackages)


class VariableType(Enum):

    BOOL = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    VOID = auto()

    # Note: This is used only for SubPackages and item in SubPackages.
    LIST_SUBPACKAGES = auto()
    SUBPACKAGE = auto()

    @staticmethod
    def from_pytype(pytype: Type) -> "VariableType":
        if pytype is Void:
            return VariableType.VOID
        if issubclass(pytype, SubPackages):
            return VariableType.LIST_SUBPACKAGES
        if issubclass(pytype, SubPackage):
            return VariableType.SUBPACKAGE
        if pytype is bool:
            return VariableType.BOOL
        if pytype is int:
            return VariableType.INTEGER
        if pytype is float:
            return VariableType.FLOAT
        if pytype is str:
            return VariableType.STRING
        raise ValueError(f"Unknow type: {pytype}.")

    def __str__(self) -> str:
        if self is VariableType.LIST_SUBPACKAGES:
            return "SubPackage[]"

        if self is VariableType.SUBPACKAGE:
            return "SubPackage"

        return super().__str__().lower().split(".")[-1]


# Union of possible type for Wizard value:
WizardValueType = Union[bool, int, float, str, SubPackage, SubPackages, Void]


class Value:

    """
    Represent a value of a given type, that can be a constant or the reuslt of
    a complex expression.

    Value expose operators from the BAIN Wizard specification with proper type
    checking so you can use them directly.
    """

    _value: WizardValueType

    def __init__(self, value: WizardValueType):
        self._type = VariableType.from_pytype(type(value))
        self._value = value

    @property
    def type(self) -> VariableType:
        """
        Returns:
            The type of the variable.
        """
        return self._type

    def is_void(self) -> bool:
        """
        Returns:
            True if this value represent the "void" value.
        """
        return self._type == VariableType.VOID

    @property
    def value(self) -> WizardValueType:
        """
        Returns:
            The value of this constant.
        """
        return self._value

    def __pos__(self) -> "Value":
        if not isinstance(self._value, (int, float)):
            raise TypeError(
                f"Cannot use plus operator on variable of type {self._type}."
            )
        return Value(self._value)

    def __neg__(self) -> "Value":
        if not isinstance(self._value, (int, float)):
            raise TypeError(
                f"Cannot use minus operator on variable of type {self._type}."
            )
        return Value(-self._value)

    def __add__(self, other: "Value") -> "Value":
        if (
            not isinstance(self._value, (int, float, str))
            or not isinstance(other._value, (int, float, str))
            or isinstance(self._value, str) != isinstance(other._value, str)
        ):
            raise TypeError(f"Cannot add values of types {self._type}, {other._type}.")
        return Value(self._value + other._value)  # type: ignore

    def __sub__(self, other: "Value") -> "Value":
        if not isinstance(self._value, (int, float)) or not isinstance(
            other._value, (int, float)
        ):
            raise TypeError("Cannot substract non-numeric values.")
        return Value(self._value - other._value)

    def __mul__(self, other: "Value") -> "Value":
        if not isinstance(self._value, (int, float)) or not isinstance(
            other._value, (int, float)
        ):
            raise TypeError("Cannot multiply non-numeric values.")
        return Value(self._value * other._value)

    def __div__(self, other: "Value") -> "Value":
        if not isinstance(self._value, (int, float)) or not isinstance(
            other._value, (int, float)
        ):
            raise TypeError("Cannot divide non-numeric values.")
        return Value(self._value / other._value)

    def __pow__(self, other: "Value") -> "Value":
        if not isinstance(self._value, (int, float)) or not isinstance(
            other._value, (int, float)
        ):
            raise TypeError("Cannot raise non-numeric values.")
        return Value(self._value ** other._value)

    def __mod__(self, other: "Value") -> "Value":
        if not isinstance(self._value, (int, float)) or not isinstance(
            other._value, (int, float)
        ):
            raise TypeError("Cannot modulo non-numeric values.")
        return Value(self._value % other._value)

    def logical_not(self) -> "Value":
        return Value(not self._value)

    def equals(self, other: "Value") -> "Value":
        return Value(self._value == other._value)

    def not_equals(self, other: "Value") -> "Value":
        return Value(self._value != other._value)

    def __or__(self, other: "Value") -> "Value":
        return Value(self._value or other._value)

    def __and__(self, other: "Value") -> "Value":
        return Value(self._value and other._value)

    def __gt__(self, other: "Value") -> "Value":
        if isinstance(self._value, (int, float)) and isinstance(
            other._value, (int, float)
        ):
            return Value(self._value > other._value)
        if isinstance(self._value, str) and isinstance(other._value, str):
            return Value(self._value > other._value)
        raise TypeError(f"Cannot compare values of types {self._type}, {other._type}.")

    def __ge__(self, other: "Value") -> "Value":
        if isinstance(self._value, (int, float)) and isinstance(
            other._value, (int, float)
        ):
            return Value(self._value >= other._value)
        if isinstance(self._value, str) and isinstance(other._value, str):
            return Value(self._value >= other._value)
        raise TypeError(f"Cannot compare values of types {self._type}, {other._type}.")

    def __lt__(self, other: "Value") -> "Value":
        if isinstance(self._value, (int, float)) and isinstance(
            other._value, (int, float)
        ):
            return Value(self._value < other._value)
        if isinstance(self._value, str) and isinstance(other._value, str):
            return Value(self._value < other._value)
        raise TypeError(f"Cannot compare values of types {self._type}, {other._type}.")

    def __le__(self, other: "Value") -> "Value":
        if isinstance(self._value, (int, float)) and isinstance(
            other._value, (int, float)
        ):
            return Value(self._value <= other._value)
        if isinstance(self._value, str) and isinstance(other._value, str):
            return Value(self._value <= other._value)
        raise TypeError(f"Cannot compare values of types {self._type}, {other._type}.")

    def contains(self, item: "Value", case_insensitive: bool = False) -> "Value":
        if not isinstance(self._value, (SubPackage, SubPackages)):
            raise TypeError(f"Cannot iterate variable of type {self._type}.")

        if not isinstance(item._value, (str, SubPackage)):
            raise TypeError(f"Cannot check presence of variable of type {self._type}.")

        if case_insensitive:
            item = Value(item._value.lower())

        it: Iterable[str]
        if isinstance(self._value, SubPackages):
            it = iter(self._value)
        else:
            it = self._value.files

        for istr in it:
            if case_insensitive:
                istr = istr.lower()
            if item._value == istr:
                return Value(True)

        return Value(False)

    def __getitem__(self, index: "Value") -> "Value":
        if not isinstance(self._value, (str, SubPackage, SubPackages)):
            raise TypeError(f"Cannot index variable of type {self._type}.")
        if not isinstance(index._value, (int)):
            raise TypeError(f"Cannot index with variable of type {index._type}.")

        try:
            return Value(self._value[index._value])
        except IndexError:
            raise IndexError(index._value)

    def slice(
        self, start: Optional["Value"], end: Optional["Value"], step: Optional["Value"]
    ) -> "Value":

        if not isinstance(self._value, str):
            raise TypeError(f"Cannot access slice of variable of type {self._type}.")

        for v in (start, end, step):
            if v is not None and not isinstance(v.value, int):
                raise TypeError(f"Cannot index with variable of type {v.type}.")

        return Value(
            self._value[
                slice(*(None if v is None else v.value for v in (start, end, step)))
            ]
        )

    def __iter__(self) -> Iterable["Value"]:
        if not isinstance(self._value, (SubPackage, SubPackages)):
            raise TypeError(f"Cannot iterate variable of type {self._type}.")

        it: Iterable[str]
        if isinstance(self._value, SubPackages):
            it = iter(self._value)
        else:
            it = self._value.files

        return (Value(x) for x in it)

    # Those operations are not "Wizardly", i.e. they make sense in Python:

    def __eq__(self, other: object) -> bool:
        value: Value
        if not isinstance(other, Value):
            value = Value(other)  # type: ignore
        else:
            value = other

        if self.is_void() and value.is_void():
            return True

        return value._type == self._type and value._value == self._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __repr__(self) -> str:
        return "{}({})".format(self.type, self.value)
