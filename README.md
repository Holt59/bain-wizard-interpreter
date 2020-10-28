# BAIN Wizard Interpreter

A BAIN Wizard Interpreter based on [`wizparse`](https://github.com/wrye-bash/wizparse).

This is a *Work In Progress*, when done, I hope to have a fully functional interpreter that could
be used in various settings to run BAIN Wizard installers.

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
- The code in [`vendor/wizparse`] is under the `wizparse` LICENSE.
- The files in [`vendor/wizparse/tests`] have their own accompanying license. See the
  [`wizparse`](https://github.com/wrye-bash/wizparse) repository for more details.
