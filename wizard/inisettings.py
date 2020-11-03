# -*- encoding: utf-8 -*-

from typing import Any, List, Optional


class WizardINISetting:

    _filename: str
    _section: str
    _setting: str

    def __init__(self, filename: str, section: str, setting: str):
        self._filename = filename
        self._section = section
        self._setting = setting

    @property
    def filename(self) -> str:
        """
        Returns:
            The name of the file containing the setting.
        """
        return self._filename

    @property
    def section(self) -> str:
        """
        Returns:
            The section containing the setting.
        """
        return self._section

    @property
    def setting(self) -> str:
        """
        Returns:
            The name of the setting.
        """
        return self._setting


class WizardINISettingEdit(WizardINISetting):

    _value: Any
    _comment: Optional[str]

    def __init__(
        self,
        filename: str,
        section: str,
        setting: str,
        value: Any,
        comment: Optional[str] = None,
    ):
        super().__init__(filename, section, setting)
        self._value = value
        self._comment = comment

    @property
    def value(self) -> Any:
        """
        Returns:
            The new value for the setting.
        """
        return self._value

    @property
    def comment(self) -> Optional[str]:
        """
        Returns:
            The comment for the setting.
        """
        return self._comment


class WizardINITweaks:

    _disabled: List[WizardINISetting]
    _modified: List[WizardINISettingEdit]

    def __init__(self):
        self._disabled = []
        self._modified = []

    @property
    def disabled(self) -> List[WizardINISetting]:
        """
        Returns:
            The list of INI settings that have been disabled by the script.
        """
        return self._disabled

    @property
    def modified(self) -> List[WizardINISettingEdit]:
        """
        Returns:
            The list of settings that have been created or modified by the script. May
            contain multiple edits for the same setting.
        """
        return self._modified
