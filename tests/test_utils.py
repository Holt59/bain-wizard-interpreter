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

    _next_opts: Optional[Union[str, List[str]]]

    def __init__(self):
        self._next_opts = None

    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
        assert isinstance(self._next_opts, str)
        for opt in options:
            if opt.name == self._next_opts:
                self._next_opts = None
                return opt

        return default

    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:
        assert isinstance(self._next_opts, list)
        if not self._next_opts:
            opts = default
        else:
            opts = [opt for opt in options if opt.name in self._next_opts]
        self._next_opts = None
        return opts

    def onSelect(self, options: Union[str, List[str]]):
        """
        Specify the option(s) to return on the next selectXXX call.

        Args:
            options: Options to return on the next select call.
        """
        self._next_opts = options
