import json
import sys
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, Callable

from antlr4 import BailErrorStrategy, CommonTokenStream, InputStream

from wizard.antlr4.wizardLexer import wizardLexer
from wizard.antlr4.wizardParser import wizardParser
from wizard.contexts import WizardInterpreterContext, WizardTerminationContext
from wizard.expr import SubPackage, Value, WizardExpressionVisitor
from wizard.interpreter import WizardInterpreter
from wizard.manager import SelectOption
from wizard.runner import WizardRunnerState
from wizard.scriptrunner import WizardScriptRunner
from wizard.severity import SeverityContext
from wizard.state import WizardInterpreterState
from wizard.utils import make_basic_context_factory
from wizard.value import SubPackages


class MockSubPackage(SubPackage):
    _files: list[str]

    def __init__(self, name: str, files: list[str]):
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
        variables: MutableMapping[str, Value[Any]] | None = None,
        state: WizardInterpreterState | None = None,
        subpackages: SubPackages | None = None,
        functions: Mapping[
            str, Callable[[WizardInterpreterState, Sequence[Value[Any]]], Value[Any]]
        ] = {},
        severity: SeverityContext | None = None,
    ):
        super().__init__(
            subpackages or SubPackages(), functions, severity or MockSeverityContext()
        )

        assert variables is None or state is None

        if state is None and variables is None:
            self.state = WizardInterpreterState()
        elif state is None and variables is not None:
            self.state = WizardInterpreterState(variables)
        elif state is not None:
            self.state = state

    def parse(self, expr: str) -> Value[Any]:
        input_stream = InputStream(expr)
        lexer = wizardLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = wizardParser(stream)
        parser._errHandler = BailErrorStrategy()
        return self.visitExpr(parser.parseWizard().body().expr(0), self.state)


class InterpreterChecker(WizardInterpreter[WizardInterpreterState]):
    def __init__(
        self,
        subpackages: SubPackages | None = None,
        severity: SeverityContext | None = None,
    ):
        super().__init__(
            make_basic_context_factory(
                subpackages or SubPackages(), severity or MockSeverityContext()
            )
        )

    def run(self, script: str) -> WizardTerminationContext[WizardInterpreterState]:
        ctx: WizardInterpreterContext[WizardInterpreterState, Any] = (
            self.make_top_level_context(script, WizardInterpreterState())
        )

        while not isinstance(ctx, WizardTerminationContext):
            ctx = ctx.exec()

        return ctx

    def register_function(
        self,
        name: str,
        function: Callable[
            [WizardInterpreterState, Sequence[Value[Any]]], Value[Any] | None
        ],
    ):
        self._factory.evisitor._functions[name] = function  # type: ignore


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

    _next_opts: list[str | list[str]]
    _returns: MutableMapping[str, Callable[..., Any]]
    _calls: list[str]

    def __init__(self, subpackages: SubPackages | None = None):
        super().__init__(subpackages or SubPackages())
        self.clear()

    def clear(self):
        self._returns = {}
        self._next_opts = []
        self._calls = []

    @property
    def calls(self) -> list[str]:
        return self._calls

    def __getattribute__(self, item: Any) -> Any:
        fn: Callable[..., Any] = object.__getattribute__(self, item)
        if hasattr(fn, "__isabstractmethod__") and fn.__isabstractmethod__:  # type: ignore

            def _fn(*args: Any) -> Any:
                # Note using str() otherwise we would loose quote around strings, and
                # not use repr() because the quote (" or ') is inconsistent. JSON is
                # consistent:
                self._calls.append(
                    "{}({})".format(item, ", ".join(map(json.dumps, args)))
                )

                if item in self._returns:
                    return self._returns[item](*args)

            fn = _fn

        return fn

    def register_function(
        self,
        name: str,
        function: Callable[
            [WizardRunnerState, Sequence[Value[Any]]], Value[Any] | None
        ],
    ):
        self._factory.evisitor._functions[name] = function  # type: ignore

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

    def setReturnFunction(self, fn: str, value: Callable[..., Any]):
        """
        Sets a function to use in place of the specified one. This replace a previous
        call to setReturnValue.

        Args:
            fn: Name of the function to 'replace'.
            value: The function to call instead of the current one.
        """
        self._returns[fn] = value

    def onSelect(self, options: str | Sequence[str]):
        """
        Specify the option(s) to return on the next selectXXX call.

        Args:
            options: Options to return on the next select call.
        """
        if isinstance(options, str):
            self._next_opts = [options]
        else:
            self._next_opts = [list(options)]

    def onSelects(self, options: list[str | list[str]]):
        """
        Specify the option(s) to return on the next selectXXX calls.

        Args:
            options: Options to return on the next select calls.
        """
        self._next_opts = options

    def selectOne(
        self, description: str, options: Sequence[SelectOption], default: SelectOption
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
        options: Sequence[SelectOption],
        default: Sequence[SelectOption] = [],
    ) -> list[SelectOption]:
        if not self._next_opts:
            return list(default)

        if not isinstance(self._next_opts[0], list):
            raise ValueError(
                "MOCK: Next option for selectMany() is not a list "
                f"(desc. = {description})."
            )

        opts = self._next_opts.pop(0)
        return [opt for opt in options if opt.name in opts]
