# -*- encoding: utf-8 -*-

from typing import List, Optional, Union

from wizard.mmitf import ModManagerInterface, SelectOption
from wizard.expr import SubPackage


class MockSubPackage(SubPackage):

    _files: List[str]

    def __new__(cls, name: str, files: List[str]):
        value = SubPackage.__new__(cls, name)
        value._files = files
        return value

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

    The format of the calls stored is "fn(a, b, c, ...)" where fn is the name of
    the method (e.g. selectPlugin) and a, b, c the repr() of the arguments.

    Current issue:
        This will not mimic returns value for method such as getFolder,
        compareGameVersion, etc., so some scripts cannot be executed.
    """

    _next_opts: List[Union[str, List[str]]]
    _calls: List[str]

    def __init__(self):
        self._next_opts = []
        self._calls = []

    def clear(self):
        self._next_opts = []
        self._calls = []

    @property
    def calls(self) -> List[str]:
        return self._calls

    def __getattribute__(self, item):
        if item in ModManagerInterface.__dict__ and item not in MockManager.__dict__:

            def fn(*args):
                self._calls.append("{}({})".format(item, ", ".join(map(repr, args))))

            return fn
        return object.__getattribute__(self, item)

    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
        assert self._next_opts and isinstance(self._next_opts[0], str)

        ret = default
        for opt in options:
            if opt.name == self._next_opts[0]:
                ret = opt
                break

        self._next_opts.pop(0)

        return ret

    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:
        assert self._next_opts and isinstance(self._next_opts[0], list)
        if not self._next_opts:
            opts = default
        else:
            opts = [opt for opt in options if opt.name in self._next_opts[0]]
        self._next_opts.pop(0)
        return opts

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
