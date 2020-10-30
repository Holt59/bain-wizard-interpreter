# -*- encoding: utf-8 -*-

from abc import abstractproperty, abstractmethod
from typing import (
    Callable,
    List,
    Mapping,
    MutableMapping,
)

from .mmitf import ModManagerInterface
from .severity import SeverityContext
from .value import SubPackage, SubPackages, Value, VariableType, Void  # noqa: F401


class AbstractWizardInterpreter:

    """
    Abstract wizard interpreter used by the expression visitor.
    """

    @abstractproperty
    def subpackages(self) -> SubPackages:
        """
        Returns:
            The list of SubPackages in the BAIN installer.
        """
        ...

    @abstractproperty
    def variables(self) -> MutableMapping[str, Value]:
        """
        Returns:
            The list of variables.
        """
        ...

    @abstractproperty
    def functions(self) -> Mapping[str, Callable[[List[Value]], Value]]:
        """
        Returns:
            The list of functions (mapping from function name to actually
            callable objects).
        """
        ...

    @abstractproperty
    def manager(self) -> ModManagerInterface:
        """
        Returns:
            The mod manager interface associated with this interpreter.
        """
        ...

    @abstractmethod
    def warning(self, text: str):
        """
        Display a warning.

        Args:
            text: The warning text.
        """
        ...

    @abstractproperty
    def severity(self) -> SeverityContext:
        """
        Returns:
            The severity context of the interpreter.
        """
        ...
