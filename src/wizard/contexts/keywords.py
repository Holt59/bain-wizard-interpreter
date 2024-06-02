from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVarTuple, cast

from ..antlr4.wizardParser import wizardParser
from ..errors import WizardNameError, WizardTypeError
from ..severity import Issue
from ..value import AnyValueType, VariableType
from .contexts import ContextState, WizardInterpreterContext

if TYPE_CHECKING:
    from .factory import WizardInterpreterContextFactory


_Args = TypeVarTuple("_Args")


class WizardKeywordContext(
    WizardInterpreterContext[ContextState, wizardParser.KeywordStmtContext]
): ...


class _WizardKeywordContext(
    WizardKeywordContext[ContextState],
    Generic[ContextState, *_Args],
):
    """
    Top-level class for keyword contexts.
    """

    @property
    def _argtypes(self) -> list[type]:
        return []

    @abstractmethod
    def _visit(self, state: ContextState, *args: *_Args) -> None: ...

    def _get_args(self, types: Sequence[type]) -> tuple[*_Args]:
        keyword = self.context.Keyword().getText()
        arglist = [
            self._factory.evisitor.visitExpr(ex, self.state)
            for ex in self.context.argList().expr()
        ]

        n_arg_none = sum(int(isinstance(None, t)) for t in types)
        min_args = len(types) - n_arg_none
        max_args = len(types)

        if len(arglist) < min_args:
            raise WizardTypeError(
                self._context,
                f"Keyword {keyword}: not enough arguments, expected {len(types)}.",
            )
        elif len(arglist) > max_args:
            raise WizardTypeError(
                self._context,
                f"Keyword {keyword}: too many arguments, expected {len(types)}.",
            )
        elif len(arglist) < len(types):
            raise WizardTypeError(
                self._context,
                f"Keyword {keyword}: not enough arguments, expected {len(types)}.",
            )

        # extract value from arguments and pad with None to reach the exact number of
        # arguments
        args = tuple(arg.value for arg in arglist)
        args += (None,) * (len(types) - len(args))

        return cast(
            "tuple[*_Args]",
            tuple(arg.value for arg in arglist),
        )

    def exec_(self) -> WizardInterpreterContext[ContextState, Any]:
        state = self.state.copy()
        self._visit(state, *self._get_args(self._argtypes))
        return self._factory.copy_parent(self, state)


class WizardDeSelectAllContext(_WizardKeywordContext[ContextState]):
    def _visit(self, state: ContextState) -> None:
        return self._factory.kvisitor.visitDeSelectAll(self, state)


class WizardDeSelectAllPluginsContext(_WizardKeywordContext[ContextState]):
    def _visit(self, state: ContextState) -> None:
        return self._factory.kvisitor.visitDeSelectAllPlugins(self, state)


class WizardDeSelectPluginContext(_WizardKeywordContext[ContextState, str]):
    def _visit(self, state: ContextState, plugin: str) -> None:
        return self._factory.kvisitor.visitDeSelectPlugin(self, state, plugin)

    @property
    def _argtypes(self):
        return [str]


class WizardDeSelectSubPackageContext(_WizardKeywordContext[ContextState, str]):
    def _visit(self, state: ContextState, package: str) -> None:
        return self._factory.kvisitor.visitDeSelectSubPackage(self, state, package)

    @property
    def _argtypes(self):
        return [str]


class WizardRenamePluginContext(_WizardKeywordContext[ContextState, str, str]):
    def _visit(self, state: ContextState, name1: str, name2: str) -> None:
        return self._factory.kvisitor.visitRenamePlugin(self, state, name1, name2)

    @property
    def _argtypes(self):
        return [str, str]


class WizardResetPluginNameContext(_WizardKeywordContext[ContextState, str]):
    def _visit(self, state: ContextState, plugin: str) -> None:
        return self._factory.kvisitor.visitResetPluginName(self, state, plugin)

    @property
    def _argtypes(self):
        return [str]


class WizardResetAllPluginNamesContext(_WizardKeywordContext[ContextState]):
    def _visit(self, state: ContextState) -> None:
        return self._factory.kvisitor.visitResetAllPluginNames(self, state)


class WizardSelectAllContext(_WizardKeywordContext[ContextState]):
    def _visit(self, state: ContextState) -> None:
        return self._factory.kvisitor.visitSelectAll(self, state)


class WizardSelectAllPluginsContext(_WizardKeywordContext[ContextState]):
    def _visit(self, state: ContextState) -> None:
        return self._factory.kvisitor.visitSelectAllPlugins(self, state)


class WizardSelectPluginContext(_WizardKeywordContext[ContextState, str]):
    def _visit(self, state: ContextState, plugin: str) -> None:
        return self._factory.kvisitor.visitSelectPlugin(self, state, plugin)

    @property
    def _argtypes(self):
        return [str]


class WizardSelectSubPackageContext(_WizardKeywordContext[ContextState, str]):
    def _visit(self, state: ContextState, subpackage: str) -> None:
        return self._factory.kvisitor.visitSelectSubPackage(self, state, subpackage)

    @property
    def _argtypes(self):
        return [str]


class WizardRequireVersionsContext(
    _WizardKeywordContext[ContextState, str, str | None, str | None, str | None]
):
    """
    The require versions context is a bit special since it probably requires
    user interaction which is why we parse the arguments inside constructor.
    """

    def __init__(
        self,
        factory: WizardInterpreterContextFactory[ContextState],
        context: wizardParser.KeywordStmtContext,
        parent: WizardInterpreterContext[ContextState, Any],
        state: ContextState | None = None,
    ):
        super().__init__(factory, context, parent, state)

        self._args = self._get_args(self._argtypes)

    # these property are useful to use the interpreter
    @property
    def game_version(self) -> str:
        return self._args[0]

    @property
    def script_extender_version(self) -> str | None:
        return self._args[1]

    @property
    def graphics_extender_version(self) -> str | None:
        return self._args[2]

    @property
    def wrye_bash_version(self) -> str | None:
        return self._args[3]

    def _get_args(
        self, types: Sequence[type]
    ) -> tuple[str, str | None, str | None, str | None]:
        # weird stuff to please type checkers
        gv, sew, gew, wbv = super()._get_args(types)
        return (gv, sew or None, gew or None, wbv or None)

    def _visit(
        self,
        state: ContextState,
        game_version: str,
        script_extender_version: str | None,
        graphics_extender_version: str | None,
        wrye_bash_version: str | None,
    ) -> None:
        return self._factory.kvisitor.visitRequireVersions(
            state,
            game_version=game_version,
            script_extender_version=script_extender_version,
            graphics_extender_version=graphics_extender_version,
            wrye_bash_version=wrye_bash_version,
        )

    @property
    def _argtypes(self):
        return [str, str | None, str | None, str | None]


class WizardNoteContext(_WizardKeywordContext[ContextState, str]):
    # note context is a bit special as it accepts any type but warn if the type is
    # not str

    def _visit(self, state: ContextState, note: AnyValueType) -> None:
        if not isinstance(note, str):
            type_ = VariableType.from_pytype(type(note))  # type: ignore
            self._factory.severity.raise_or_warn(
                Issue.USAGE_OF_ANYTHING_IN_NOTE,
                WizardTypeError(
                    self.context,
                    f"'Note' keyword expected string, found {type_}.",
                ),
                f"'Note' keyword expected string, found {type_}.",
            )
        return self._factory.kvisitor.visitNote(self, state, str(note))

    @property
    def _argtypes(self):
        return [object]


def make_keyword_context(
    factory: WizardInterpreterContextFactory[ContextState],
    context: wizardParser.KeywordStmtContext,
    parent: WizardInterpreterContext[ContextState, Any],
) -> WizardInterpreterContext[ContextState, wizardParser.KeywordStmtContext]:
    name: str = context.Keyword().getText()
    if name == "RequireVersions":
        return WizardRequireVersionsContext(factory, context, parent)
    if name in ["ResetAllPluginNames", "ResetAllEspmNames"]:
        return WizardResetAllPluginNamesContext(factory, context, parent)
    if name == "DeSelectSubPackage":
        return WizardDeSelectSubPackageContext(factory, context, parent)
    if name in ["SelectAllPlugins", "SelectAllEspms"]:
        return WizardSelectAllPluginsContext(factory, context, parent)
    if name == "SelectSubPackage":
        return WizardSelectSubPackageContext(factory, context, parent)
    if name in ["DeSelectAllPlugins", "DeSelectAllEspms"]:
        return WizardDeSelectAllPluginsContext(factory, context, parent)
    if name in ["ResetPluginName", "ResetEspmName"]:
        return WizardResetPluginNameContext(factory, context, parent)
    if name in ["DeSelectPlugin", "DeSelectEspm"]:
        return WizardDeSelectPluginContext(factory, context, parent)
    if name in ["SelectPlugin", "SelectEspm"]:
        return WizardSelectPluginContext(factory, context, parent)
    if name in ["RenamePlugin", "RenameEspm"]:
        return WizardRenamePluginContext(factory, context, parent)
    if name == "DeSelectAll":
        return WizardDeSelectAllContext(factory, context, parent)
    if name == "SelectAll":
        return WizardSelectAllContext(factory, context, parent)
    if name == "Note":
        return WizardNoteContext(factory, context, parent)

    raise WizardNameError(context, name)
