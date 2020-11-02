# -*- encoding: utf-8 -*-

from abc import abstractmethod
from enum import Enum, auto
from typing import MutableMapping


class Severity(Enum):

    ALLOW = auto()
    WARNING = auto()
    ERROR = auto()


class Issue(Enum):

    # Indicates if multiple default values are allowed in SelectOne statement.
    MULTIPLE_DEFAULTS_IN_SELECT_ON = auto()

    # Indicates if using a non-set variable is allowed or not.
    USAGE_OF_NOTSET_VARIABLES = auto()

    # Indicates if case labels can be non-string and Identifier instead.
    USAGE_OF_NON_STRING_CASE_LABELS = auto()

    # Indicates that a Note can be anything (not only a string):
    USAGE_OF_ANYTHING_IN_NOTE = auto()

    # Select a sub-package or a plugin that does not exist:
    SELECT_MISSING_SUBPACKAGE = auto()
    SELECT_MISSING_PLUGIN = auto()


class SeverityContext:

    _default_severity: Severity
    _context: MutableMapping[Issue, Severity] = {}

    def __init__(self):
        self._default_severity = Severity.WARNING

    @abstractmethod
    def warning(self, text: str):
        """
        Display a warning.

        Args:
            text: The warning text.
        """
        ...

    def set_default_severity(self, severity: Severity):
        """
        Set the default severity level used. By default it is "WARNING".

        Args:
            severity: The new default severity level.
        """
        self._default_severity = severity

    def set_severity(self, issue: Issue, severity: Severity):
        """
        Set the severity for the given issue.

        Args:
            issue: The issue to set the severity for.
            severity: The new severity of the issue.
        """
        self._context[issue] = severity

    def raise_or_warn(self, issue: Issue, exc: Exception, warn: str):
        """
        Check the severity of the given issue and eventually raise the given exception
        or warn the user with the given message. May do nothing if the severity is
        Severity.ALLOW.

        Args:
            issue: The issue to check the severity for.
            exc: The exception to raise if the severity is "ERROR".
            warn: The message to use to warn the user if the severity is "WARNING".
        """
        s = self._context.get(issue, self._default_severity)

        if s == Severity.ERROR:
            raise exc

        if s == Severity.WARNING:
            self.warning(warn)
