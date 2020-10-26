# -*- encoding: utf-8 -*-


class WizardError(Exception):
    """
    Base class for all Wizard errors.
    """

    pass


class WizardUnsupportedOperation(WizardError):
    """
    Error raised when an operation is not supported (not yet implemented).
    """

    def __init__(self, operation: str):
        super().__init__(f"'{operation}' operation is not implemented.")


class WizardIndexError(WizardError):

    _index: int

    def __init__(self, index: int):
        super().__init__(f"Index {index} out of range.")
        self._index = index

    @property
    def index(self) -> int:
        return self._index


class WizardNameError(WizardError):

    _name: str

    def __init__(self, name):
        super().__init__(f"The name {name} is not defined.")
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class WizardTypeError(WizardError):
    pass
