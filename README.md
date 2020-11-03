# BAIN Wizard Interpreter

A BAIN Wizard Interpreter based on [`wizparse`](https://github.com/wrye-bash/wizparse).

This is a *Work In Progress*, when done, I hope to have a fully functional interpreter that could
be used in various settings to run BAIN Wizard installers.

# Basic Usage

```python
from typing import List

from wizard.mmitf import SelectOption
from wizard.runner import WizardRunner
from wizard.value import SubPackage, SubPackages


class MySubPackage(SubPackage):

    """
    Implement your own subpackage - SubPackage inherits str so you should use
    __new__ instead of __init__.
    """

    _files: List[str]

    def __new__(cls, name: str, files: List[str] = []):
        # Important: There is a default for files() so that the object can
        # be deepcopied.
        value = SubPackage.__new__(cls, name)
        value._files = files
        return value

    @property
    def files(self):
        return iter(self._files)


class MyRunner(WizardRunner):

    """
    Extends the runner and implement the missing methods.
    """

    # These are the methods you need to provide - See mmitf.ModManagerInterface for
    # the documentation of each method.

    # The WizardRunner class extends ModManagerInterface and already implements many
    # functions, but you can always override them.

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

# Create the subpackages:
subpackages = SubPackages([MySubPackage(...) for ...])

# Create the runner:
runner = MyRunner(subpackages)

# Run a script:
result = runner.run("wizard.txt")

result.status  # Status of the execution.
result.subpackages  # List of selected subpackages.
result.plugins  # List of enabled plugins.
result.notes  # List of notes.
result.tweaks.disabled  # List of disabled INI settings.
result.tweaks.modified  # List of new or modified INI settings.
```

## Handling errors

If an error occurs during the script execution, the interpreter will call
the `WizardRunner.error()` function with the Python exception. By default, this
method re-raise the error, you can change it:

```python
def error(self, exc: Exception):
    # Do whatever you want.
    ...
```

If this method returns, `result.status` will be `WizardInterpreterResult.ERROR`.

## Extra features

The `WizardRunner` exposes a few extra features through methods that you can use
during the execution, e.g. in `selectOne`, `selectMany`, `error`, `complete`, etc.

```python
runner = WizardRunner(...)

# Abort the execution - Equivalent to a 'Cancel' keyword:
runner.abort()

# Retrieve the current state():
state = runner.state()

# Rewind to the given state:
runner.rewind(state)
```

The `runner.abort` and `runner.rewind` method rely on exception to work, so these do
not return.

# Dependencies

## `wizparse`

The code under [`wizard/antlr4`](wizard/antlr4) is generated from [`wizard/antlr4/wizard.g4`](wizard/antlr4/wizard.g4)
from the [`wizparse`](https://github.com/wrye-bash/wizparse) repository.
To generate the file, you need `antlr4`, and you simply have to run:

```bash
java -jar antlr-4.8-complete.jar -visitor -Dlanguage=Python3 -o ./wizard/antlr4 ./wizard/antlr4/wizard.g4
```

**Note:** Currently, the `./wizard/antlr4/wizard.g4` is a slightly modified version of the file
from the original repository that fixes some issues.

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
