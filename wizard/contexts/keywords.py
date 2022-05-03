# -*- encoding: utf-8 -*-

from abc import abstractproperty
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple

from ..antlr4.wizardParser import wizardParser
from ..errors import WizardNameError, WizardTypeError
from ..severity import Issue
from ..value import Value, VariableType
from .contexts import ContextState, WizardInterpreterContext

if TYPE_CHECKING:
    from .factory import WizardInterpreterContextFactory


class WizardKeywordContext(
    WizardInterpreterContext[ContextState, wizardParser.KeywordStmtContext]
):

    """
    Top-level class for keyword contexts.
    """

    @property
    def _argtypes(self) -> List[type]:
        return []

    @abstractproperty
    def _visitor(self) -> Callable[..., None]:
        ...

    def _get_args(self, types: List[type]) -> List[Value]:
        keyword = self.context.Keyword().getText()
        arglist = [
            self._factory.evisitor.visitExpr(ex, self.state)
            for ex in self.context.argList().expr()
        ]
        if len(arglist) > len(types):
            raise WizardTypeError(f"Keyword {keyword}: too many arguments.")
        elif len(arglist) < len(types):
            raise WizardTypeError(
                f"Keyword {keyword}: not enough arguments, expected {len(types)}."
            )

        for i, (a, t) in enumerate(zip(arglist, types)):
            if not isinstance(a.value, t):
                raise WizardTypeError(
                    f"Keyword {keyword}: Argument at position {i + 1} has incorrect"
                    f" type, expected {VariableType.from_pytype(t)}, got {a.type}."
                )

        return arglist

    def exec_(self) -> WizardInterpreterContext:
        state = self.state.copy()
        self._visitor(
            self, state, *(arg.value for arg in self._get_args(self._argtypes))
        )
        return self._factory._copy_parent(self, state)


class WizardDeSelectAllContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitDeSelectAll


class WizardDeSelectAllPluginsContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitDeSelectAllPlugins


class WizardDeSelectPluginContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitDeSelectPlugin

    @property
    def _argtypes(self):
        return [str]


class WizardDeSelectSubPackageContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitDeSelectSubPackage

    @property
    def _argtypes(self):
        return [str]


class WizardRenamePluginContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitRenamePlugin

    @property
    def _argtypes(self):
        return [str, str]


class WizardResetPluginNameContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitResetPluginName

    @property
    def _argtypes(self):
        return [str]


class WizardResetAllPluginNamesContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitResetAllPluginNames


class WizardSelectAllContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitSelectAll


class WizardSelectAllPluginsContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitSelectAllPlugins


class WizardSelectPluginContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitSelectPlugin

    @property
    def _argtypes(self):
        return [str]


class WizardSelectSubPackageContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitSelectSubPackage

    @property
    def _argtypes(self):
        return [str]


class WizardRequireVersionsContext(WizardKeywordContext[ContextState]):

    """
    The require versions context is a bit special since it probably requires
    user interaction which is why we parse the arguments inside constructor.
    """

    _args: Tuple[str, Optional[str], Optional[str], Optional[str]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._args = tuple(
            arg.value if arg.value else None for arg in self._get_args(self._argtypes)
        )

    # These property are useful to use the interpreter:
    @property
    def game_version(self) -> str:
        return self._args[0]

    @property
    def script_extender_version(self) -> Optional[str]:
        return self._args[1]

    @property
    def graphics_extender_version(self) -> Optional[str]:
        return self._args[2]

    @property
    def wrye_bash_version(self) -> Optional[str]:
        return self._args[3]

    # These two are not used at all but required for mypy or other tools
    # since otherwise the class is abstract.

    @property
    def _visitor(self):
        return self._factory.kvisitor.visitRequireVersions

    @property
    def _argtypes(self):
        return [str, str, str, str]

    def _get_args(self, types: List[type]) -> List[Value]:
        keyword = self.context.Keyword().getText()
        arglist = [
            self._factory.evisitor.visitExpr(ex, self.state)
            for ex in self.context.argList().expr()
        ]

        if len(arglist) < 1:
            raise WizardTypeError(
                f"Keyword {keyword}: not enough arguments, expected between 1 and 4."
            )

        if len(arglist) > 4:
            raise WizardTypeError(f"Keyword {keyword}: too many arguments.")

        if len(arglist) < 4:
            arglist = arglist + [Value("")] * (4 - len(arglist))

        for i, a in enumerate(arglist):
            if not isinstance(a.value, str):
                raise WizardTypeError(
                    f"Keyword {keyword}: Argument at position {i + 1} has incorrect"
                    f" type, expected {VariableType.from_pytype(str)}, got {a.type}."
                )

        return arglist

    def exec_(self) -> WizardInterpreterContext:
        state = self.state.copy()
        self._visitor(state, *self._args)
        return self._factory._copy_parent(self, state)


class WizardNoteContext(WizardKeywordContext[ContextState]):
    @property
    def _visitor(self):
        return self._factory.kvisitor.visitNote

    @property
    def _argtypes(self):
        return [object]

    def _get_args(self, types: List[type]):
        args = super()._get_args(types)
        if not isinstance(args[0].value, str):
            self._factory.severity.raise_or_warn(
                Issue.USAGE_OF_ANYTHING_IN_NOTE,
                WizardTypeError(
                    self.context,
                    f"'Note' keyword expected string, found {args[0].type}.",
                ),
                f"'Note' keyword expected string, found {args[0].type}.",
            )
        return [Value(str(args[0].value))]


def make_keyword_context(
    factory: "WizardInterpreterContextFactory",
    context: wizardParser.KeywordStmtContext,
    parent: WizardInterpreterContext,
) -> WizardKeywordContext:
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
