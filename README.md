# BAIN Wizard Interpreter

![Python Versions](https://img.shields.io/pypi/pyversions/bain-wizard-interpreter?style=flat-square)
[![PyPi](https://img.shields.io/pypi/v/bain-wizard-interpreter?style=flat-square)](https://pypi.org/project/bain-wizard-interpreter/)
[![Tests](https://img.shields.io/github/workflow/status/holt59/bain-wizard-interpreter/Tests?label=tests&style=flat-square)](https://github.com/Holt59/bain-wizard-interpreter/actions/workflows/python-tests.yml)
[![Linters](https://img.shields.io/github/workflow/status/holt59/bain-wizard-interpreter/Linters?label=linters&style=flat-square)](https://github.com/Holt59/bain-wizard-interpreter/actions/workflows/python-linters.yml)
[![MIT License](https://img.shields.io/github/license/holt59/bain-wizard-interpreter?style=flat-square)](https://opensource.org/licenses/MIT)

A BAIN Wizard Interpreter based on [`wizparse`](https://github.com/wrye-bash/wizparse) that can
be used in various settings to run BAIN Wizard installers.

# Basic Usage

There are various way to use the interpreter.
The easiest way is to extends the `WizardScriptRunner` and add the missing
functionalities that are mod-manager or game specific.
You can then use `WizardScriptRunner.run()` to execute a script, and everything will
be called when required.

```python
from pathlib import Path
from typing import List

from wizard.manager import SelectOption
from wizard.scriptrunner import WizardScriptRunner
from wizard.value import SubPackage, SubPackages


class MySubPackage(SubPackage):

    """
    Implement your own SubPackage.
    """

    _files: List[str]

    def __init__(self, name: str, files: List[str]):
        super().__init__(name)
        self._files = files

    @property
    def files(self):
        return iter(self._files)


class MyRunner(WizardScriptRunner):

    """
    Extends the runner and implement the missing methods.
    """

    # these are the methods you need to provide, see manager.ManagerModInterface
    # and manager.ManagerUserInterface for the documentation of each method
    #
    # the WizardRunner class extends both interfaces and already implements many
    # functions, but you can always override them

    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
        ...

    def selectMany(
        self,
        description: str,
        options: List[SelectOption],
        default: List[SelectOption] = [],
    ) -> List[SelectOption]:
        ...

    def compareGameVersion(self, version: str) -> int:
        ...

    def compareSEVersion(self, version: str) -> int:
        ...

    def compareGEVersion(self, version: str) -> int:
        ...

    def compareWBVersion(self, version: str) -> int:
        ...

    def dataFileExists(self, *filepaths: str) -> bool:
        ...

    def getPluginLoadOrder(self, filename: str, fallback: int = -1) -> int:
        ...

    def getPluginStatus(self, filename) -> int:
        ...

    def getFilename(self, path: str) -> str:
        ...

    def getFolder(self, path: str) -> str:
        ...

# create the sub-packages
subpackages = SubPackages([MySubPackage(...) for ...])

# create the runner
runner = MyRunner(subpackages)

# run a script - use a Path() object, otherwise the string will be interpreted
# as a script
status, result = runner.run(Path("wizard.txt"))

status  # status of the execution
result.subpackages  # list of selected sub-packages
result.plugins  # list of enabled plugins
result.notes  # list of notes
result.tweaks.disabled  # list of disabled INI settings
result.tweaks.modified  # list of new or modified INI settings
```

## Handling errors

If an error occurs during the script execution, the interpreter will call
the `WizardScriptRunner.error()` function with the Python exception. By default, this
method re-raise the error, you can change it:

```python
def error(self, exc: Exception):
    # handle the error
    ...
```

If this method returns, `result.status` will be `WizardScriptRunnerStatus.ERROR`.

## Extra features

The `WizardScriptRunner` exposes a few extra features through methods that you can use
during the execution, e.g. in `selectOne`, `selectMany`, `error`, `complete`, etc.

```python
runner = WizardRunner(...)

# abort the execution - Equivalent to a 'Cancel' keyword
runner.abort()

# retrieve the current context
context = runner.context()

# rewind to the given context
runner.rewind(context)
```

The `runner.abort` and `runner.rewind` method rely on exception to work, so these do
not return.

# Dependencies

## `wizparse`

The code under [`wizard/antlr4`](wizard/antlr4) is generated from [`wizard/antlr4/wizard.g4`](wizard/antlr4/wizard.g4)
from the [`wizparse`](https://github.com/wrye-bash/wizparse) repository.
To generate the file, you need `antlr4`, and you simply have to run:

```bash
# IMPORTANT: use FORWARD SLASH (/) everywhere, otherwise it does not work
java -jar antlr-4.10.1-complete.jar -visitor -Dlanguage=Python3 -o ./wizard/antlr4 ./vendor/wizparse/wizards/wizard.g4
```

## Run tests

To run the tests, you need the Python 3 ANTLR4 runtime and `pytest`:

```bash
pip install antlr4-python3-runtime pytest
```

You can then run the tests using `pytest`.

# LICENSE

Unless otherwise specified, the code in this repository is licensed under the MIT license.
See [LICENSE](LICENSE) for the full text.

Exceptions:

- The code in [`wizard/antlr4`](wizard/antlr4) is generated from
  the [`wizparse`](https://github.com/wrye-bash/wizparse) repository, so the `wizparse`
  LICENSE applies to it.
- The code in [`vendor/wizparse`](vendor/wizparse) is under the `wizparse` LICENSE.
- The files in [`vendor/wizparse/tests`](vendor/wizparse/tests) have their own accompanying license. See the
  [`wizparse`](https://github.com/wrye-bash/wizparse) repository for more details.
