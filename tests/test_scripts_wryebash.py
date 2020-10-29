# -*- encoding: utf-8 -*-

"""
This files contain tests for scripts in tests/data. The results of the test
where obtain with Wrye-Bash (version 307).

Each folder under tests/data should contain:
- The wizard.txt file containing the actual scripts.
- A files.txt file containing all the files in the archive (not the folder).
"""

from pathlib import Path
from typing import List, Mapping

from wizard.expr import SubPackage, SubPackages

from .test_utils import InterpreterChecker, MockManager, MockSubPackage


class MockManagerPlus(MockManager):

    _all_subpackages: Mapping[str, SubPackage]
    _all_plugins: List[str]

    _notes: List[str]
    _subpackages: List[str]
    _plugins: List[str]

    def __init__(self, subpackages: List[SubPackage]):
        super().__init__()

        self._all_subpackages = {str(sp): sp for sp in subpackages}
        self._all_plugins = [
            f
            for sp in subpackages
            for f in sp.files
            if f.endswith(".esp") or f.endswith(".esm")
        ]

    def clear(self):
        self._notes = []
        self._subpackages = []
        self._plugins = []
        super().clear()

    @property
    def notes(self):
        """
        Returns:
            The notes set during script execution (not sorted).
        """
        return self._notes

    @property
    def subpackages(self) -> List[str]:
        """
        Returns:
            The list of selected subpackages, in alphabetical order (easier
            for comparison).
        """
        return sorted(list(set(self._subpackages)))

    @property
    def plugins(self) -> List[str]:
        """
        Returns:
            The list of selected plugins, in alphabetical order (easier
            for comparison).
        """
        return sorted(list(set(self._plugins)))

    def deselectAll(self):
        self._subpackages.clear()
        self._plugins.clear()

    def deselectAllPlugins(self):
        self._plugins.clear()

    def deselectPlugin(self, plugin_name: str):
        if plugin_name in self._plugins:
            self._plugins.remove(plugin_name)

    def deselectSubPackage(self, name: str):
        if name in self._subpackages:
            self._subpackages.remove(name)

    def note(self, text: str):
        self._notes.append(text)

    def selectAll(self):
        self._plugins = list(self._all_plugins)
        self._subpackages = list(self._all_subpackages.keys())

    def selectAllPlugins(self):
        # Guess we only select plugins from selected subpackages?
        self._plugins = [
            f
            for sp in self._all_subpackages
            for f in sp.files
            if sp in self._subpackages and (f.endswith(".esp") or f.endswith(".esm"))
        ]

    def selectPlugin(self, plugin_name: str):
        self._plugins.append(plugin_name)

    def selectSubPackage(self, name: str):
        self._subpackages.append(name)

        # Auto-select plugins?
        for f in self._all_subpackages[name].files:
            if f.endswith(".esp") or f.endswith(".esm"):
                self.selectPlugin(f.split("\\")[-1])


def read_subpackages(files_txt: Path) -> SubPackages:
    with open(files_txt, "r") as fp:
        files = [line.strip() for line in fp.readlines()]

    # This is dirty, but I would have to write a proper checker...
    spnames = set(f.split("\\")[0] for f in files if f.split(" ")[0].isdigit())

    sp: List[MockSubPackage] = []
    for spname in sorted(spnames):
        sp.append(
            MockSubPackage(spname, [f for f in files if f.startswith(spname + "\\")])
        )

    return SubPackages(sp)


def test_better_cities():

    # You can get this one Nexus: https://www.nexusmods.com/oblivion/mods/16513
    folder = Path("tests/data/Better Cities v6.0.13-16513-6-0-13-1590843631")

    # Read the script:
    with open(folder.joinpath("wizard.txt"), "r") as fp:
        script = fp.read()

    # Read the subpackages:
    subpackages = read_subpackages(folder.joinpath("files.txt"))

    # Create the manager and interpreter:
    m = MockManagerPlus(subpackages)
    c = InterpreterChecker(m, subpackages)

    # I had these installed, so I use them to check:
    m.setReturnFunction(
        "dataFileExists", lambda s: s in ["Knights.esp", "All Natural.esp"]
    )

    # First run:
    m.onSelects(
        [
            "No",
            "Everything",
            "Vanilla",
            "No",
            "No",
            "No",
            "No",
            "No",
            "No",
            "No",
            ["Clocks of Cyrodiil", "IC Expanded"],
        ]
    )

    expected = ['requiresVersions("1.2.0.416", "0.0.18.6", "", "294")']

    notes = [
        "No FPS Patch will be installed.",
        "You won't see the Aristocratic District or the extended Arena District walls"
        " when outside the city.",
        "You won't see Better Cities VWD items of the IC.",
        "The water height in Leyawiin will remain low as in the original game.",
        "Open Better Cities ESP not installed. Toggling the Open Better Cities option"
        " in-game will not work correctly.",
        "Ships added by Better Cities will use vanilla textures.",
        "You won't have the meshes for Roberts Body mods installed.",
        "Do not forget to download and install the resources for Clocks of Cyrodiil.",
        "Do not forget to download and install the resources for IC Expanded.",
    ]

    packages = [
        "00 Core",
        "01 Better Cities Full",
        "02 Better Imperial City Full",
        "20 Clocks of Cyrodiil",
        "21 ICExpand",
        "30 All Natural",
        "30 Knights of the Nine Chorrol",
        "30 OOO",
        "30 Oblivifall",
        "31 OOO",
        "40 Bravil Vanilla",
    ]

    plugins = sorted(
        [
            "Better Cities - All Natural.esp",
            "Better Cities .esp",  # Seriously?
            "Better Cities Chorrol - Knights of the Nine.esp",
            "Better Cities Full.esp",
            "Better Cities Resources.esm",
            "Better Imperial City.esp",
            "ClocksOfCyrodiil.esp",
            "ICEXPAND.esp",
        ]
    )

    c.parse(script)

    for ex in expected:
        assert ex in m.calls

    assert m.notes == notes
    assert m.subpackages == packages
    assert m.plugins == plugins


def test_majestic_mountains():

    # You can get this one Nexus: https://www.nexusmods.com/skyrim/mods/86292
    folder = Path("tests/data/Majestic Mountains Main-86292-1-4")

    # Read the script:
    with open(folder.joinpath("wizard.txt"), "r") as fp:
        script = fp.read()

    # Read the subpackages:
    subpackages = read_subpackages(folder.joinpath("files.txt"))

    # Create the manager and interpreter:
    m = MockManagerPlus(subpackages)
    c = InterpreterChecker(m, subpackages)

    # I had these installed, so I use them to check:
    m.setReturnFunction(
        "dataFileExists", lambda s: s in ["Knights.esp", "All Natural.esp"]
    )

    # First run:
    m.onSelects(
        ["Welcome", "Begin Installation", ["Landscape Textures", "Moss Rocks"], [],]
    )

    expected = []

    # Note: Added extra \\ because these are found in the file.
    notes = [
        """If you are manually sorting your load order, make sure that \
MajesticMountains.esp is loaded before other plugins in the mod, or sort with LOOT.

Confirm your selections above - if you are not happy with the selection use the BACK \
button below.
When ready, tick 'Apply these selections' Below, and then click the 'Finish' button.

If You Have Auto-Anneal/Install Wizards set in Wrye Bash preferences, the Wizard will \
install your selections after clicking Finish
Otherwise, right-click the installer again and choose Install""",
    ]

    packages = [
        "00 Majestic Mountains",
        "01 Moss",
        "10 Complementary Landscape Texture Pack",
    ]

    plugins = sorted(["MajesticMountains.esp", "MajesticMountains_Moss.esp"])

    c.parse(script)

    for ex in expected:
        assert ex in m.calls

    assert m.notes == notes
    assert m.subpackages == packages
    assert m.plugins == plugins

    # Second test (different choice) - The note does not change.
    m.clear()
    m.onSelects(
        ["Welcome", "Begin Installation", ["Landscape Textures"], ["SMIM"],]
    )

    packages = [
        "00 Majestic Mountains",
        "10 Complementary Landscape Texture Pack",
        "21 SMIM Patch Milestone",
    ]

    plugins = sorted(["MajesticMountains.esp"])

    c.parse(script)

    for ex in expected:
        assert ex in m.calls

    assert m.notes == notes
    assert m.subpackages == packages
    assert m.plugins == plugins
