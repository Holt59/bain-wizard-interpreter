# -*- encoding: utf-8 -*-

"""
These tests are only here to check that running the test scripts do
not actually fails.

Important: If a script contains While loop that are cancelled by user,
it should not be tested here.
"""

from antlr4.error.Errors import ParseCancellationException

from pathlib import Path

from wizard.expr import SubPackages
from wizard.errors import WizardError

from .test_utils import InterpreterChecker, MockManager


def check_script(c: InterpreterChecker, script: Path):

    # Read the script:
    with open(script, "r") as fp:
        lines = fp.read()

    try:
        c.parse(lines)
    except (WizardError, ParseCancellationException) as err:
        print("Failed script: {}".format(script))
        raise err


def test_wizparse_scripts():

    # List the scripts:
    scripts = list(Path("vendor/wizparse/tests").glob("*.txt"))

    # test.txt is not valid:
    scripts.remove(Path("vendor/wizparse/tests/test.txt"))

    # Create an interpreter with a mock-manager:
    m = MockManager()

    c = InterpreterChecker(m, SubPackages([]), {})

    # IMPORTANT:
    # 1. There are no sub-packages, so some scripts might fail.
    # 2. Methods from the manager returns nothing except for selectOne and
    #    selectMany, so some scripts might fail.

    # Needed for farmhouseChimneys (at least):
    m.setReturnValue("getPluginStatus", 2)

    # Check each script:
    for script in scripts:
        check_script(c, script)
