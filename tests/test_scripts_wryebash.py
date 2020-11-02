# -*- encoding: utf-8 -*-

"""
This files contain tests for scripts in tests/data. The results of the test
where obtain with Wrye-Bash (version 307).

Each folder under tests/data should contain:
- The wizard.txt file containing the actual scripts.
- A files.txt file containing all the files in the archive (not the folder).
"""

from pathlib import Path
from typing import List

from wizard.expr import SubPackages

from .test_utils import MockRunner, MockSubPackage


def read_subpackages(files_txt: Path) -> SubPackages:
    with open(files_txt, "r") as fp:
        files = [line.strip() for line in fp.readlines()]

    # This is dirty, but I would have to write a proper checker...
    spnames = set(Path(f).parts[0] for f in files if f.split(" ")[0].isdigit())

    sp: List[MockSubPackage] = []
    for spname in sorted(spnames):
        sp.append(
            MockSubPackage(spname, [f for f in files if Path(f).parts[:1] == (spname,)])
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

    # Create the runner:
    runner = MockRunner(subpackages)

    # I had these installed, so I use them to check:
    runner.setReturnFunction(
        "dataFileExists", lambda s: s in ["Knights.esp", "All Natural.esp"]
    )

    # First run:
    runner.onSelects(
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

    result = runner.run(script)

    for ex in expected:
        assert ex in runner.calls

    assert result.notes == notes
    assert result.subpackages == packages
    assert result.plugins == plugins


def test_majestic_mountains():

    # You can get this one Nexus: https://www.nexusmods.com/skyrim/mods/86292
    folder = Path("tests/data/Majestic Mountains Main-86292-1-4")

    # Read the script:
    with open(folder.joinpath("wizard.txt"), "r") as fp:
        script = fp.read()

    # Read the subpackages:
    subpackages = read_subpackages(folder.joinpath("files.txt"))

    # Create the manager and interpreter:
    runner = MockRunner(subpackages)

    # First run:
    runner.onSelects(
        ["Welcome", "Begin Installation", ["Landscape Textures", "Moss Rocks"], []]
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

    result = runner.run(script)

    for ex in expected:
        assert ex in runner.calls

    assert result.notes == notes
    assert result.subpackages == packages
    assert result.plugins == plugins

    # Second test (different choice) - The note does not change.
    runner.onSelects(
        ["Welcome", "Begin Installation", ["Landscape Textures"], ["SMIM"]]
    )

    packages = [
        "00 Majestic Mountains",
        "10 Complementary Landscape Texture Pack",
        "21 SMIM Patch Milestone",
    ]

    plugins = sorted(["MajesticMountains.esp"])

    result = runner.run(script)

    for ex in expected:
        assert ex in runner.calls

    assert result.notes == notes
    assert result.subpackages == packages
    assert result.plugins == plugins


def test_book_covers():

    # Language Pack (testing both LE and SE):
    for name in [
        "Language Pack - Book Covers Skyrim SE.7z-901-4-2",
        "Language Pack - Book Covers Skyrim 3_5 Legendary-35399-3-6",
    ]:

        folder = Path("tests/data").joinpath(name)

        # Read the script:
        with open(folder.joinpath("wizard.txt"), "r") as fp:
            script = fp.read()

        # Read the subpackages:
        subpackages = read_subpackages(folder.joinpath("files.txt"))

        # Create the runner:
        runner = MockRunner(subpackages)

        # Same for all options (LE also contains CZ, but... ):
        options = [
            ("English", "01 Skyrim ESP EN"),
            ("French", "01 Skyrim ESP FR"),
            ("German", "01 Skyrim ESP DE"),
            ("Italian", "01 Skyrim ESP IT"),
            ("Polish", "01 Skyrim ESP PO"),
            ("Spanish", "01 Skyrim ESP ES"),
            ("Russian", "01 Skyrim ESP RU"),
        ]

        for opt, sub in options:
            runner.onSelect(opt)
            result = runner.run(script)
            assert result.notes == []
            assert result.subpackages == [sub]
            assert result.plugins == ["Book Covers Skyrim.esp"]

    # Optional Paper Textures:
    folder = Path("tests/data/Optional Paper Textures-35399-2-2")

    # Read the script:
    with open(folder.joinpath("wizard.txt"), "r") as fp:
        script = fp.read()

    # Read the subpackages:
    subpackages = read_subpackages(folder.joinpath("files.txt"))

    # Create the manager and interpreter:
    runner = MockRunner(subpackages)

    runner.onSelects([[]])
    result = runner.run(script)
    assert result.notes == []
    assert result.subpackages == []
    assert result.plugins == []

    runner.onSelects([["World"]])
    result = runner.run(script)
    assert result.notes == []
    assert result.subpackages == ["01 BCS Optional Paper World"]
    assert result.plugins == []

    runner.onSelects([["Inventory"]])
    result = runner.run(script)
    assert result.notes == []
    assert result.subpackages == ["01 BCS Optional Paper Inventory"]
    assert result.plugins == []

    runner.onSelects([["World", "Inventory"]])
    result = runner.run(script)
    assert result.notes == []
    assert result.subpackages == [
        "01 BCS Optional Paper Inventory",
        "01 BCS Optional Paper World",
    ]
    assert result.plugins == []


def test_farmhouse_chimneys():

    # You can get this one Nexus: https://www.nexusmods.com/skyrimspecialedition/mods/8766 # noqa: E501
    folder = Path("tests/data/Farmhouse Chimneys v3.0.2-8766-3-0-2")

    # Read the script:
    with open(folder.joinpath("wizard.txt"), "r") as fp:
        script = fp.read()

    # Read the subpackages:
    subpackages = read_subpackages(folder.joinpath("files.txt"))

    # Create the runner:
    runner = MockRunner(subpackages)

    # I had these installed, so I use them to check:
    runner.setReturnValue("dataFileExists", False)
    runner.setReturnValue("getPluginStatus", -1)

    # First run:
    runner.onSelects(
        [
            "Welcome",
            "Original Meshes",
            "Vanilla",
            ["Falskaar", "Moon and Star"],
            ["Cutting Room Floor"],
            ["Ivarstead", "Karthwasten", "Shor's Stone"],
        ]
    )

    expected = []

    notes = [
        """Thank you for installing Farmhouse Chimneys


Confirm your selections above - if you are not happy with the selection use the BACK \
button below.
When ready, tick 'Apply these selections' Below, and then click the 'Finish' button.

If You Have Auto-Anneal/Install Wizards set in Wrye Bash preferences, the Wizard will \
install your selections after clicking Finish
Otherwise, right-click the installer again and choose Install""",
    ]

    packages = [
        "00 - Original Meshes",
        "01 - Vanilla",
        "02 - Falskaar",
        "03 - Moon and Star",
        "04 - Cutting Room Floor",
        "05 - Ivarstead",
        "05 - Karthwasten",
        "05 - Shors Stone",
    ]

    plugins = sorted(
        [
            "FarmhouseChimneys.esp",
            "FarmhouseChimneysCRF.esp",
            "FarmhouseChimneysFalskaar.esp",
            "FarmhouseChimneysIvarstead.esp",
            "FarmhouseChimneysKarthwasten.esp",
            "FarmhouseChimneysMaS.esp",
            "FarmhouseChimneysShorsStone.esp",
        ]
    )

    result = runner.run(script)

    for ex in expected:
        assert ex in runner.calls

    assert result.notes == notes
    assert result.subpackages == packages
    assert result.plugins == plugins
