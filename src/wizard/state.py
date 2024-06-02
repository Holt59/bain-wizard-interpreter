from collections.abc import Mapping, MutableMapping
from typing import Any, Self, TypeVar

from .value import Value


class WizardInterpreterState:
    """
    State of the interpreter, stored in the context. This class can be
    inherited to use custom states that should implement a proper copy().
    """

    # The variables - The underlying mapping is mutable but is never
    # modified, except right after constructing the state:
    _variables: MutableMapping[str, Value[Any]]

    def __init__(self, variables: Mapping[str, Value[Any]] = {}):
        self._variables = dict(variables)

    @property
    def variables(self) -> Mapping[str, Value[Any]]:
        """
        Returns:
            The variables in this state.
        """
        return self._variables

    def set(self, name: str, value: Value[Any]):
        self._variables[name] = value

    def copy(self) -> Self:
        """
        Copy this state. This can be a mix between a shallow or a deep copy, the
        restriction is that modifying the returned state should not impact the
        current state.

        Returns:
            A copy of this state.
        """
        state = type(self)()
        state._variables.update(self._variables)
        return state


ContextState = TypeVar("ContextState", bound=WizardInterpreterState)
