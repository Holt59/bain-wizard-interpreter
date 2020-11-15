# -*- encoding: utf-8 -*-

import json
import sys

from typing import Any, Callable, List, Optional, Mapping, MutableMapping, Union

from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser

from wizard.contexts import (
    WizardInterpreterContext,
    WizardTerminationContext,
)
from wizard.expr import SubPackage, Value, WizardExpressionVisitor
from wizard.interpreter import WizardInterpreter
from wizard.manager import SelectOption
from wizard.scriptrunner import WizardScriptRunner
from wizard.severity import SeverityContext
from wizard.state import WizardInterpreterState
from wizard.utils import make_basic_context_factory
from wizard.value import SubPackages


class MockSubPackage(SubPackage):

    _files: List[str]

    def __init__(self, name: str, files: List[str]):
        super().__init__(name)
        self._files = files

    @property
    def files(self):
        return iter(self._files)


class MockSeverityContext(SeverityContext):
    def warning(self, text: str):
        print(f"WARNING: {text}", file=sys.stderr)


class ExpressionChecker(WizardExpressionVisitor):
    def __init__(
        self,
        variables: Optional[MutableMapping[str, Value]] = None,
        state: Optional[WizardInterpreterState] = None,
        subpackages: SubPackages = SubPackages(),
        functions: Mapping[
            str, Callable[[WizardInterpreterState, List[Value]], Value]
        ] = {},
        severity: SeverityContext = MockSeverityContext(),
    ):
        super().__init__(subpackages, functions, severity)

        assert variables is None or state is None

        if state is None and variables is None:
            self.state = WizardInterpreterState()
        elif state is None and variables is not None:
            self.state = WizardInterpreterState(variables)
        elif state is not None:
            self.state = state

    def parse(self, expr: str) -> Value:
        input_stream = InputStream(expr)
        lexer = wizardLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        parser._errHandler = BailErrorStrategy()
        return self.visitExpr(parser.parseWizard().body().expr(0), self.state)


class InterpreterChecker(WizardInterpreter):
    def __init__(
        self,
        subpackages: SubPackages = SubPackages(),
        severity: SeverityContext = MockSeverityContext(),
    ):
        super().__init__(make_basic_context_factory(subpackages, severity))

    def run(self, script: str) -> WizardTerminationContext[WizardInterpreterState]:
        ctx: WizardInterpreterContext = self.make_top_level_context(
            script, WizardInterpreterState()
        )

        while not isinstance(ctx, WizardTerminationContext):
            ctx = ctx.exec()

        return ctx


class RunnerChecker(WizardScriptRunner):

    """
    Provides the following functionalities:

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

    def __init__(
        self,
        subpackages: SubPackages = SubPackages(),
    ):
        super().__init__(subpackages)
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
                "MOCK: Next option for selectOne() is not a string "
                f"(desc. = {description})."
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
                "MOCK: Next option for selectMany() is not a list "
                f"(desc. = {description})."
            )

        opts = self._next_opts.pop(0)
        return [opt for opt in options if opt.name in opts]
