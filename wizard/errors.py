# -*- encoding: utf-8 -*-


from antlr4 import ParserRuleContext


class WizardError(Exception):
    """
    Base class for all Wizard errors.
    """

    _ctx: ParserRuleContext

    def __init__(self, context: ParserRuleContext, *args):
        super().__init__(*args)
        self._ctx = context

    @property
    def context(self) -> ParserRuleContext:
        return self._ctx

    @property
    def line(self) -> int:
        return self._ctx.start.line  # type: ignore

    def __str__(self) -> str:
        return "Line {}, Column {}: {}".format(
            self._ctx.start.line, self._ctx.start.column, super().__str__()
        )


class WizardParseError(WizardError):

    """
    Error raised when a parsing error occurs.
    """

    pass


class WizardUnsupportedOperation(WizardError):
    """
    Error raised when an operation is not supported (not yet implemented).
    """

    def __init__(self, context: ParserRuleContext, operation: str):
        super().__init__(context, f"'{operation}' operation is not implemented.")


class WizardIndexError(WizardError):

    _index: int

    def __init__(self, context: ParserRuleContext, index: int):
        super().__init__(context, f"Index {index} out of range.")
        self._index = index

    @property
    def index(self) -> int:
        return self._index


class WizardNameError(WizardError):

    _name: str

    def __init__(self, context: ParserRuleContext, name):
        super().__init__(context, f"The name {name} is not defined.")
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class WizardTypeError(WizardError):
    pass


class WizardMissingPackageError(WizardError):

    _name: str

    def __init__(self, context: ParserRuleContext, name: str):
        super().__init__(f"Trying to activate missing '{name}' sub-package.")
        self._name = name

    @property
    def subpackage(self) -> str:
        return self._name


class WizardMissingPluginError(WizardError):

    _name: str

    def __init__(self, context: ParserRuleContext, name: str):
        super().__init__(f"Trying to activate missing '{name}' plugin.")
        self._name = name

    @property
    def subpackage(self) -> str:
        return self._name
