# Unbounded Knapsack

Unbounded knapsack is a dynamic programming pattern where each available item
can be chosen more than once. This is different from 0/1 knapsack, where each
item can only be used once.

This folder contains small, focused unbounded knapsack problems written in clean
Python. The goal is to make each solution easy to read, easy to test, and
suitable for a professional GitHub portfolio.

## Rod Cutting

The rod cutting problem asks for the maximum revenue that can be earned from a
rod of a given length. The price list stores the selling price for each piece
length:

- index 0 is the price for length 1
- index 1 is the price for length 2
- index 2 is the price for length 3

The same piece length can be used repeatedly, so this problem is a natural fit
for unbounded knapsack.

## Virtual Environment

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

All commands below assume the virtual environment is activated and you are in the
`python-engineering-practice` project root.

## Run The Code

From the repository root:

```bash
python data_algorithm/dynamic_programing/unbounded_knapsack/unbounded_knapsack_code/rod_cutting.py
```

## Run Tests

Run the unbounded knapsack tests with Python's built-in `unittest` module:

```bash
python -m unittest discover -s data_algorithm/dynamic_programing/unbounded_knapsack/unbounded_knapsack_test -p "test_*.py"
```

The tests are also compatible with `pytest` if you use it for the full project:

```bash
pytest
```

From the `unbounded_knapsack_test` folder, run only the
`test_rod_cutting.py` file:

```bash
python3 -m pytest test_rod_cutting.py
```

From the `unbounded_knapsack_test` folder, run all tests in that folder:

```bash
python3 -m pytest
```

## Test Coverage

Install `coverage` if it is not already available in the virtual environment:

```bash
pip install coverage
```

Run coverage for the unbounded knapsack source code:

```bash
python -m coverage run --source=data_algorithm/dynamic_programing/unbounded_knapsack/unbounded_knapsack_code -m unittest discover -s data_algorithm/dynamic_programing/unbounded_knapsack/unbounded_knapsack_test -p "test_*.py"
python -m coverage report -m
```

Generate an HTML coverage report:

```bash
python -m coverage html
open htmlcov/index.html
```

The test suite covers:

- normal rod cutting input
- repeated use of the same piece length
- zero-length rods
- empty price lists
- rod lengths greater than the price list
- invalid negative lengths
- invalid negative prices
- the `RodCutting` class wrapper
- debug logging
- the script execution block under `if __name__ == "__main__"`
