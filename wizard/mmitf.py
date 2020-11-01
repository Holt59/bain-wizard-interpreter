# -*- encoding: utf-8 -*-


from abc import abstractmethod
from typing import List, Optional


class WizardRunnerState:

    """
    State for the wizard runner that can be used to rewind to a previous
    state.
    """

    ...


class WizardRunner:

    """
    The actual wizard runner.
    """

    @abstractmethod
    def abort(self):
        """
        Abort the script execution, returning immediately.

        Raises:
            ValueError: If the runner is not running when abort() is called.
        """
        ...

    @abstractmethod
    def rewind(self, state: WizardRunnerState):
        """
        Rewind the runner to the given state.

        Args:
            state: The state to rewind to.

        Raises:
            ValueError: If the runner is not running when rewind() is called.
        """
        ...

    @abstractmethod
    def state(self) -> WizardRunnerState:
        """
        Returns:
            A (deep) copy of the current state of the interpreter, suitable
            for rewinding.
        """
        ...


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

    _runner: WizardRunner

    # Initialize the interface with a runner:
    def setup(self, runner: WizardRunner):
        self._runner = runner

    # Development methods:
    def warning(self, text: str):
        """
        Called when a warning is emitted by the interpreter, usually due
        to an improper script.

        This should be a light warning for the user, even invisible, as it is
        mostly called for script-related stuff (e.g. use of a variable before
        it is set).
        """
        ...

    def error(self, exc: Exception):
        """
        Called when an error occurs while executing the script. Unlike warning(),
        errors cannot be recovered from and cannot be safely ignored.

        By default this method simply re-raised the given exception.

        Args:
            exc: The actual Python exception that raises the error.
        """
        raise exc

    # Choice / dialog methods:
    def cancel(self) -> bool:
        """
        Called when a 'Cancel' keyword is encountered.

        Returns:
            True to stop executing the script, False to continue.
        """
        return True

    def complete(self) -> bool:
        """
        Called when a 'Return' keyword is encountered or at the end of the
        installation.

        Returns:
            True to stop executing the script, False to continue.
        """
        return True

    @abstractmethod
    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
        """
        Query user to select one of the proposed options.

        Args:
            description: Description to display to the user.
            options: List of available options.
            default: Default selected option.

        Returns:
            The option selected by the user.
        """
        ...

    @abstractmethod
    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:
        """
        Query user to select many of the proposed options.

        Args:
            description: Description to display to the user.
            options: List of available options.
            default: Default selected options.

        Returns:
            The options selected by the user. Can be empty.
        """
        ...

    # Function methods:
    @abstractmethod
    def compareGameVersion(self, version: str) -> int:
        """
        Used to test the installed version of the game against the specified version.

        Args:
            version: A string formatted to hold a file version number, eg. "1.2.0.416".

        Returns:
            -1, 0 or 1 if the installed version is less, equal or greater than the given
            version.
        """
        pass

    @abstractmethod
    def compareSEVersion(self, version: str) -> int:
        """
        Used to test the installed version of the script extender against the
        specified version.

        Args:
            version: A string formatted to hold a file version number, eg. "0.0.20.1".

        Returns:
            -1, 0 or 1 if the installed version is less, equal or greater than the given
            version.
        """
        pass

    @abstractmethod
    def compareGEVersion(self, version: str) -> int:
        """
        Used to test the installed version of the graphics extender against the
        specified version.

        Args:
            version: A string formatted to hold a file version number, eg. "3.0.1".

        Returns:
            -1, 0 or 1 if the installed version is less, equal or greater than the given
            version.
        """
        pass

    @abstractmethod
    def compareWBVersion(self, version: str) -> int:
        """
        Used to test the installed version Wrye Bash against the
        specified version.

        Args:
            version: A string formatted to hold a file version number, eg. "307".

        Returns:
            -1, 0 or 1 if the installed version is less, equal or greater than the given
            version.
        """
        pass

    @abstractmethod
    def dataFileExists(self, *filepaths: str) -> bool:
        """
        Tests for the existence of a file in the Data directory. If the file you are
        testing for is a plugin, this should also detect ghosted versions of the file.

        Args:
            filepaths: List of files to check. Path should be relative to the data
                directory but can go up with "..".

        Returns:
            True if all the files exist, False otherwise.
        """
        ...

    @abstractmethod
    def getPluginLoadOrder(self, filename: str, fallback: int = -1) -> int:
        """
        Returns the current load order index of a plugin in the Data directory.

        Args:
            filename: Path relative to the Data direcotry to the plugin.
            fallback: Value to return if the plugin has no load order index.

        Returns:
            The load order of the plugin or fallback if the plugin has no load order
            index.
        """
        ...

    @abstractmethod
    def getPluginStatus(self, filename) -> int:
        """
        Returns the status of a plugin in the Data directory.

        Args:
            filename: Path relative to the Data direcotry to the plugin.

        Returns:
            -1 if the plugin does not exist,
            0 if the plugin is not active, imported or merged,
            1 if the plugin is not active but has portions imported into Bashed Patch,
            2 if the plugin is active,
            3 if the plugin is merged into the Bashed Patch.
        """
        ...

    @abstractmethod
    def disableINILine(self, filename: str, section: str, setting: str):
        """
        Create an INI tweak file that disables the specified setting by commenting it
        out. Otherwise, behaves identically to editINI.

        Args:
            filename: The name of the INI file to edit, relative to the Data directory.
            section: The section in the INI where setting resides.
            setting: The setting to disable.
        """
        ...

    @abstractmethod
    def editINI(
        self,
        filename: str,
        section: str,
        setting: str,
        value,
        comment: Optional[str] = "",
    ):
        """
        Create an INI tweak file with some tweaks in it. If file that to apply the
        tweak to is from the current installer or is the game's ini file, then the
        tweaks are also applied, otherwise, it will just be generated for the user
        to apply manually.

        Args:
            filename: The name of the INI file to edit, relative to the Data directory.
            section: The section in the INI where setting resides.
            setting: The setting to set.
            value: The value to set the setting to.
            comment: An optional comment to add.
        """
        ...

    @abstractmethod
    def getFilename(self, path: str) -> str:
        """
        Retrieve the filename in a path (actually from the system).

        Args:
            path: Path to the file to extract the filename from.

        Returns:
            If the path does not exists, or if the path points to a directory, returns
            an empty string, otherwise returns the filename of the file the path points
            to.
        """
        ...

    @abstractmethod
    def getFolder(self, path: str) -> str:
        """
        Retrieve the folder in a path (actually from the system).

        Args:
            path: Path to the file to extract the folder from.

        Returns:
            If the path does not exists, or if the path points to a file, returns
            an empty string, otherwise returns the name of the folder the path points
            to.
        """
        ...

    # Keyword methods:

    @abstractmethod
    def deselectAll(self):
        """
        Cause all sub-packages and plugins to be de-selected from installation. This
        is equivalent to first un-checking all plugins in the Plugin Filter of the BAIN
        window, then un-checking all sub-packages in the BAIN window.
        """
        ...

    @abstractmethod
    def deselectAllPlugins(self):
        """
        Cause all plugins to be de-selected from installation. This is equivalent to
        un-checking all plugins in the Plugin Filter of the BAIN window.
        """
        ...

    @abstractmethod
    def deselectPlugin(self, plugin_name: str):
        """
        Cause the specified plugin to be deselected from installation. This is
        equivalent to un-checking the plugin in the Plugin Filter of the BAIN window.

        Args:
            plugin_name: The name of the plugin to de-select.
        """
        ...

    @abstractmethod
    def deselectSubPackage(self, name: str):
        """
        Cause the specified sub-package to be de-selected from installation. This is
        equivalent to un-checking the sub-package in the BAIN window.

        Args:
            name: Name of the sub-package to de-select.
        """
        ...

    @abstractmethod
    def note(self, text: str):
        """
        Add a note to the user to be displayed at the end of the wizard, on the finish
        page. The '- ' will be added automatically.

        Args:
            text: Note to display at the end.
        """
        ...

    @abstractmethod
    def renamePlugin(self, original_name: str, new_name: str):
        """
        Change the installed name of a plugin. Note that the file extension must stay
        the same.

        Args:
            original_name: The name of the plugin, as it appears in the BAIN package.
            new_name: The new name you want to have the plugin installed as.
        """
        ...

    @abstractmethod
    def requiresVersions(
        self,
        game_version: str,
        se_version: Optional[str],
        ge_version: Optional[str],
        wrye_bash_version: Optional[str],
    ):
        """
        Tests the users system against version requirements you specify. If the
        requirements are not met, a warning dialog will be shown asking if you wish
        to continue anyway.

        Args:
            game_version: Version of the game to test for. See compareGameVersion for
                the proper format of the string.
            se_version: Version of the Script Extender to test for. See
                compareSEVersion for the proper format of the string.
            ge_version: Version of the Graphics Extender to test for. See
                compareGEVersion for the proper format of the string.
            wrye_bash_version: Version of Wrye Bash to test for. See
                compareWBVersion for more info.
        """
        ...

    @abstractmethod
    def resetPluginName(self, original_name: str):
        """
        Resets the name of a plugin back to its default name.

        Args:
            original_name: The name of the plugin, as it appears in the BAIN package.
        """
        ...

    @abstractmethod
    def resetAllPluginNames(self):
        """
        Resets the names of all plugins back to their default names.
        """
        ...

    @abstractmethod
    def selectAll(self):
        """
        Cause all sub-packages and plugins to be selected for installation. This is
        equivalent to first checking all sub-packages in the BAIN window, then checking
        all plugins in the Plugin Filter of the BAIN window.
        """
        ...

    @abstractmethod
    def selectAllPlugins(self):
        """
        Cause all plugins to be selected for installation. This is equivalent to
        checking all plugins in the Plugin Filter of the BAIN window.
        """
        ...

    @abstractmethod
    def selectPlugin(self, plugin_name: str):
        """
        Cause the specified plugin to be selected for installation. This is equivalent
        to checking the plugin in the Plugin Filter of the BAIN window.

        Args:
            plugin_name: Name of the plugin to select.
        """
        ...

    @abstractmethod
    def selectSubPackage(self, name: str):
        """
        Cause the specified sub-package to be selected for installation. This is
        equivalent to checking the sub-package and all the plugins in that subpackage
        in the BAIN window.

        Args:
            name: Name of the sub-package to select.
        """
        ...
