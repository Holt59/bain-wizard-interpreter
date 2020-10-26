# BAIN Wizard Interpreter

A BAIN Wizard Interpreter based on [`wizparse`](https://github.com/wrye-bash/wizparse).

This is a *Work In Progress*, when done, I hope to have a fully functional interpreter that could
be used in various settings to run BAIN Wizard installers.

# Dependencies

## `wizparse`

The code under [`wizard/antlr4`](wizard/antlr4) is generated from [`wizard/antlr4/wizard.g4`](wizard/antlr4/wizard.g4)
which is a (slightly modified) version of `wizard.g4` from the [`wizparse`](https://github.com/wrye-bash/wizparse) repository.
To generate the file, you need `antlr4`, and you simply have to run:

```bash
java -jar ./antlr-4.8-complete.jar -visitor -Dlanguage=Python3 ./wizard.g4
```

## Run tests

To run the tests, you need the Python 3 ANTLR4 runtime and `pytest`:

```bash
pip install antlr4-python3-runtime pytest
```

You can then run the tests using `pytest`.

# LICENSE

Copyright 2020 Holt59

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
