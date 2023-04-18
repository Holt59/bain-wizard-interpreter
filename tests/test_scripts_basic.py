# -*- encoding: utf-8 -*-

"""
These tests are only here to check that running the test scripts do
not actually fails.

Important: If a script contains While loop that are cancelled by user,
it should not be tested here.
"""

from pathlib import Path

from antlr4.error.Errors import ParseCancellationException

from wizard.errors import WizardError

from .test_utils import RunnerChecker


def test_wizparse_scripts():
    # List the scripts:
    scripts = list(Path("vendor/wizparse/tests/expect-success").glob("*.txt"))

    # test.txt is not valid:
    scripts.remove(Path("vendor/wizparse/tests/expect-success/test.txt"))

    # Create an interpreter with a mock-manager:
    c = RunnerChecker()

    # IMPORTANT:
    # 1. There are no sub-packages, so some scripts might fail.
    # 2. Methods from the manager returns nothing except for selectOne and
    #    selectMany, so some scripts might fail.

    # Needed for farmhouseChimneys (at least):
    c.setReturnValue("getPluginStatus", 2)

    # Check each script:
    for script in scripts:
        try:
            c.run(script)
        except (WizardError, ParseCancellationException) as err:
            print("Failed script: {}".format(script))
            raise err
