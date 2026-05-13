# Recursion

Recursion is a problem-solving technique where a function calls itself to solve
smaller versions of the same problem. A recursive solution normally has two
important parts:

- **Base case:** the condition where the function can return an answer without
  calling itself again.
- **Recursive step:** the part where the function calls itself with a smaller or
  simpler input.

This folder contains small, focused recursion problems written in clean Python.
The goal is to make each solution easy to read, easy to test, and suitable for a
professional GitHub portfolio.

## Virtual Environment

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

After activation, your terminal should look similar to this:

```text
(.venv) tejalkrunal@Tejals-MacBook-Pro python-engineering-practice %
```

All commands below assume the virtual environment is activated and you are in the
`python-engineering-practice` project root.

## Run The Code

From the repository root:

```bash
python data_algorithm/recursion/recursion_code/flatten_the_array.py
```

## Run Tests

Run the recursion tests with Python's built-in `unittest` module:

```bash
python -m unittest discover -s data_algorithm/recursion/recursion_test -p "test_*.py"
```

The tests are also compatible with `pytest` if you use it for the full project:

```bash
pytest
```

## Test Coverage

Install `coverage` if it is not already available in the virtual environment:

```bash
pip install coverage
```

Run coverage for the recursion source code:

```bash
python -m coverage run --source=data_algorithm/recursion/recursion_code -m unittest discover -s data_algorithm/recursion/recursion_test -p "test_*.py"
python -m coverage report -m
```

Expected result:

```text
Name                                                           Stmts   Miss  Cover
----------------------------------------------------------------------------------
data_algorithm/recursion/recursion_code/flatten_the_array.py      15      0   100%
----------------------------------------------------------------------------------
TOTAL                                                             15      0   100%
```

Generate an HTML coverage report:

```bash
python -m coverage html
open htmlcov/index.html
```

The test suite covers:

- normal nested lists
- empty lists
- nested empty lists
- deeply nested lists
- single-element lists
- mixed value types
- input immutability
- the `FlattenTheArray` class wrapper
- the script execution block under `if __name__ == "__main__"`
