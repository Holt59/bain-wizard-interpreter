# -*- encoding: utf-8 -*-


from abc import abstractmethod
from typing import List, Optional


class ManagerModInterface:

    """
    The ManagerModInterface represents the interface to implement to let the
    interpreter (or runner) interact with the game information and files.
    """

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
        ...

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
        ...

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
        ...

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
        ...

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


class SelectOption:

    """
    Option from SelectOne or SelectMany statement.
    """

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SelectOption):
            return False
        return (self.name, self.description, self.image) == (
            other.name,
            other.description,
            other.image,
        )

    def __repr__(self) -> str:
        return f"SelectOption({self.name}, {self.description}, {self.image})"


class ManagerUserInterface:

    """
    The ManagerUserInterface represents the interface to implement to let the
    interpreter (or runner) interact with the user.
    """

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

    @abstractmethod
    def requiresVersions(
        self,
        game_version: str,
        se_version: Optional[str],
        ge_version: Optional[str],
        wrye_bash_version: Optional[str],
    ):
        """
        Tests the user system against version requirements you specify. If the
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
