# -*- encoding: utf-8 -*-

import json

from typing import Any, Callable, List, MutableMapping, Union

from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser

from wizard.expr import SubPackage, Value, WizardExpressionVisitor
from wizard.interpreter import WizardInterpreter, WizardInterpreterResult
from wizard.mmitf import ModManagerInterface, SelectOption


class MockSubPackage(SubPackage):

    _files: List[str]

    def __new__(cls, name: str, files: List[str] = []):
        # Important: There is a default for files() so that the object can
        # be deepcopied.
        value = SubPackage.__new__(cls, name)
        value._files = files
        return value

    @property
    def files(self):
        return iter(self._files)


class MockManager(ModManagerInterface):

    """
    This is a Mock of a ModManagerInterface. It provides the following
    functionalities:

        1. You can specify which options the call to selectOne() and
           selectMany() should return using onSelect (for the next call)
           only and onSelects (for multiple future) calls.

        2. It registers all the calls to abstract methods from ModManagerInterface
           in a list (can be accessed using .calls) so that you can check if the
           right methods were called. This does not store calls to selectOne() or
           selectMany().

        3. You can register return values for methods using setReturnValue(). The
           return value is kept until the next call to setReturnValue().

    The format of the calls stored is "fn(a, b, c, ...)" where fn is the name of
    the method (e.g. selectPlugin) and a, b, c the repr() of the arguments.
    """

    _next_opts: List[Union[str, List[str]]]
    _returns: MutableMapping[str, Callable]
    _calls: List[str]

    def __init__(self):
        self.clear()

    def clear(self):
        self._returns = {}
        self._next_opts = []
        self._calls = []

    @property
    def calls(self) -> List[str]:
        return self._calls

    def __getattribute__(self, item):

        fn = object.__getattribute__(self, item)

        if hasattr(fn, "__isabstractmethod__") and fn.__isabstractmethod__:

            def fn(*args):

                # Note using str() otherwise we would loose quote around strings, and
                # not use repr() because the quote (" or ') is inconsistent. JSON is
                # consistent:
                self._calls.append(
                    "{}({})".format(item, ", ".join(map(json.dumps, args)))
                )

                if item in self._returns:
                    return self._returns[item](*args)

        return fn

    def setReturnValue(self, fn: str, value: Any):
        """
        Sets the value to return on the next calls of fn. The value is stored and
        reused until a next call to setReturnValue() for the same function. This
        replaces a previous call to setReturnFunction.

        Args:
            fn: Name of the function.
            value: Value to return on subsequent call to fn.
        """
        self._returns[fn] = lambda *args: value

    def setReturnFunction(self, fn: str, value: Callable):
        """
        Sets a function to use in place of the specified one. This replace a previous
        call to setReturnValue.

        Args:
            fn: Name of the function to 'replace'.
            value: The function to call instead of the current one.
        """
        self._returns[fn] = value

    def onSelect(self, options: Union[str, List[str]]):
        """
        Specify the option(s) to return on the next selectXXX call.

        Args:
            options: Options to return on the next select call.
        """
        if isinstance(options, str):
            self._next_opts = [options]
        else:
            self._next_opts = [options]

    def onSelects(self, options: List[Union[str, List[str]]]):
        """
        Specify the option(s) to return on the next selectXXX calls.

        Args:
            options: Options to return on the next select calls.
        """
        self._next_opts = options

    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:

        if not self._next_opts:
            return default

        if not isinstance(self._next_opts[0], str):
            raise ValueError(
                f"Next option for selectOne() is not a string (desc. = {description})."
            )

        name = self._next_opts.pop(0)

        for opt in options:
            if opt.name == name:
                return opt

        return default

    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:

        if not self._next_opts:
            return default

        if not isinstance(self._next_opts[0], list):
            raise ValueError(
                f"Next option for selectMany() is not a list (desc. = {description})."
            )

        opts = self._next_opts.pop(0)
        return [opt for opt in options if opt.name in opts]


class ExpressionChecker(WizardExpressionVisitor):
    def parse(self, expr: str) -> Value:
        input_stream = InputStream(expr)
        lexer = wizardLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        parser._errHandler = BailErrorStrategy()
        return self.visitExpr(parser.parseWizard().body().expr(0))


class InterpreterChecker(WizardInterpreter):
    def parse(self, expr: str) -> WizardInterpreterResult:
        input_stream = InputStream(expr)
        lexer = wizardLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        parser._errHandler = BailErrorStrategy()

        return self.visit(parser.parseWizard())
