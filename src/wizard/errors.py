from typing import cast

from antlr4 import Parser, ParserRuleContext, Token, TokenStream
from antlr4.error.Errors import (
    FailedPredicateException,
    InputMismatchException,
    NoViableAltException,
    RecognitionException,
)


class WizardError(Exception):
    """
    Base class for all Wizard errors.

    The only case where there is no context associated is if the parser fails
    at the beginning.
    """

    _ctx: ParserRuleContext | None

    def __init__(self, context: ParserRuleContext | None, *args: object):
        super().__init__(*args)
        self._ctx = context

    @property
    def context(self) -> ParserRuleContext | None:
        return self._ctx

    @property
    def line(self) -> int:
        if not self._ctx:
            return -1
        return self._ctx.start.line  # type: ignore

    @property
    def column(self) -> int:
        if not self._ctx:
            return -1
        return self._ctx.start.column  # type: ignore

    # The messageXXX are taken from ANTLR4 error strategy (reportXXX):

    def escapeWSAndQuote(self, s: str) -> str:
        s = s.replace("\n", "\\n")
        s = s.replace("\r", "\\r")
        s = s.replace("\t", "\\t")
        return "'" + s + "'"

    def getTokenErrorDisplay(self, t: Token | None):
        if t is None:
            return "<no token>"
        s = cast(str | None, t.text)  # pyright: ignore[reportUnknownMemberType]
        if s is None:
            if t.type == Token.EOF:
                s = "<EOF>"
            else:
                s = "<" + str(t.type) + ">"
        return self.escapeWSAndQuote(s)

    def messageNoViableAlternative(
        self, recognizer: Parser, e: NoViableAltException
    ) -> str:
        tokens = cast(TokenStream | None, recognizer.getTokenStream())  # pyright: ignore[reportUnknownMemberType]
        if tokens is not None:
            if e.startToken.type == Token.EOF:
                input = "<EOF>"
            else:
                input = cast(str, tokens.getText(e.startToken, e.offendingToken))  # type: ignore
        else:
            input = "<unknown input>"
        return "no viable alternative at input " + self.escapeWSAndQuote(input)

    def messageInputMismatch(
        self, recognizer: Parser, e: InputMismatchException
    ) -> str:
        return (
            "mismatched input "
            + self.getTokenErrorDisplay(e.offendingToken)
            + " expecting "
            + cast(
                str,
                e.getExpectedTokens().toString(  # type: ignore
                    recognizer.literalNames,  # type: ignore
                    recognizer.symbolicNames,  # type: ignore
                ),
            )
        )

    def messageFailedPredicate(
        self, recognizer: Parser, e: FailedPredicateException
    ) -> str:
        ruleName: str = recognizer.ruleNames[recognizer._ctx.getRuleIndex()]  # type: ignore
        return f"rule {ruleName} {e.message}"

    @property
    def message(self) -> str:
        if not self.args or not isinstance(self.args[0], RecognitionException):
            return super().__str__()

        e = self.args[0]
        recognizer = e.recognizer

        if isinstance(e, NoViableAltException):
            return self.messageNoViableAlternative(recognizer, e)
        elif isinstance(e, InputMismatchException):
            return self.messageInputMismatch(recognizer, e)
        elif isinstance(e, FailedPredicateException):
            return self.messageFailedPredicate(recognizer, e)
        else:
            return f"unknown recognition error type: {type(e).__name__}"

    def __str__(self) -> str:
        return f"Line {self.line}, Column {self.column}: {self.message}"


class WizardParseError(WizardError):
    """
    Error raised when a parsing error occurs.
    """

    pass


class WizardUnsupportedOperation(WizardError):
    """
    Error raised when an operation is not supported (not yet implemented).
    """

    def __init__(self, context: ParserRuleContext | None, operation: str):
        super().__init__(context, f"'{operation}' operation is not implemented.")


class WizardIndexError(WizardError):
    _index: int

    def __init__(self, context: ParserRuleContext | None, index: int):
        super().__init__(context, f"Index {index} out of range.")
        self._index = index

    @property
    def index(self) -> int:
        return self._index


class WizardNameError(WizardError):
    _name: str

    def __init__(self, context: ParserRuleContext | None, name: str):
        super().__init__(context, f"The name '{name}' is not defined.")
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class WizardTypeError(WizardError):
    pass


class WizardMissingPackageError(WizardError):
    _name: str

    def __init__(self, context: ParserRuleContext, name: str):
        super().__init__(context, f"Trying to activate missing '{name}' sub-package.")
        self._name = name

    @property
    def subpackage(self) -> str:
        return self._name


class WizardMissingPluginError(WizardError):
    _name: str

    def __init__(self, context: ParserRuleContext, name: str):
        super().__init__(context, f"Trying to activate missing '{name}' plugin.")
        self._name = name

    @property
    def subpackage(self) -> str:
        return self._name
