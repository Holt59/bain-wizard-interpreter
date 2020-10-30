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
