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

    def selectOne(
        self, description: str, options: List[SelectOption], default: SelectOption
    ) -> SelectOption:
      ...

    # TODO: List of methods to implement.


# Create the subpackages:
subpackages = SubPackages([MySubPackage(...) for ...])

# Create the runner:
runner = MyRunner(subpackages)

# Run a script:
runner.run("wizard.txt")
```

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
