# -*- encoding: utf-8 -*-


from abc import abstractmethod
from typing import List, Optional


class SelectOption:
    def __init__(self, name: str, desc: str, image: Optional[str] = None):
        self._name = name
        self._desc = desc
        self._image = image

    @property
    def name(self) -> str:
        """
        Returns:
            The name of the option.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Returns:
            The description of the option.
        """
        return self._desc

    @property
    def image(self) -> Optional[str]:
        """
        Returns:
            The image for the option, or None if there are no image.
        """
        return self._image


class ModManagerInterface:
    @abstractmethod
    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
        ...

    @abstractmethod
    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:
        ...
