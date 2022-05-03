# -*- encoding: utf-8 -*-

from typing import Callable, Optional, TypeVar

from antlr4 import ParserRuleContext
from antlr4.error.Errors import InputMismatchException, ParseCancellationException

from ..errors import WizardError, WizardIndexError, WizardParseError, WizardTypeError

T = TypeVar("T")


def wrap_exceptions(
    fn: Callable[[], T], context: Optional[ParserRuleContext] = None
) -> T:
    """
    Wrap the given call to `fn` in a proper try/except block to convert as many
    exceptions as possible to WizardError.
    """

    try:
        return fn()
    # Just forward wizard-errors:
    except WizardError as ex:
        raise ex
    # Wrap parser exceptions:
    except ParseCancellationException as ex:
        # Try to find a context:
        if context is None and isinstance(ex.args[0], InputMismatchException):
            context = ex.args[0].ctx

        raise WizardParseError(context, ex)
    # Wrap "known" exceptions:
    except TypeError as te:
        raise WizardTypeError(context, te)
    except IndexError as ie:
        raise WizardIndexError(context, *ie.args)
