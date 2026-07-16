from app.quick_sort import quick_sort

import sys
import runpy


def test_quick_sort_returns_sorted_list():
    """
    Verify that quick_sort correctly sorts an unsorted list
    containing multiple integer values in ascending order.
    """
    numbers = [40, 2, 1, 223, 33]

    result = quick_sort(numbers, 0, len(numbers))

    assert result == [1, 2, 33, 40, 223]


def test_quick_sort_empty_list():
    """
    Verify that quick_sort handles an empty list
    and returns an empty list without errors.
    """
    numbers = []

    assert quick_sort(numbers, 0, len(numbers)) == []


def test_quick_sort_single_element_list():
    """
    Verify that quick_sort correctly handles a list
    containing only one element.
    """
    numbers = [10]

    assert quick_sort(numbers, 0, len(numbers)) == [10]


def test_quick_sort_already_sorted_list():
    """
    Verify that quick_sort does not change an already
    sorted list and returns the same order.
    """
    numbers = [1, 2, 3, 4, 5]

    assert quick_sort(numbers, 0, len(numbers)) == [1, 2, 3, 4, 5]


def test_quick_sort_with_duplicate_values():
    """
    Verify that quick_sort correctly handles duplicate values
    and keeps all occurrences in the sorted output.
    """
    numbers = [5, 2, 8, 2, 1, 5]

    assert quick_sort(numbers, 0, len(numbers)) == [1, 2, 2, 5, 5, 8]


def test_quick_sort_with_negative_numbers():
    """
    Verify that quick_sort correctly sorts lists containing
    both negative and positive integer values.
    """
    numbers = [-5, 3, -1, 0, 8, -10]

    assert quick_sort(numbers, 0, len(numbers)) == [-10, -5, -1, 0, 3, 8]


def test_quick_sort_reverse_sorted_list():
    """
    Verify that quick_sort correctly sorts a list
    arranged in descending order.
    """
    numbers = [9, 7, 5, 3, 1]

    assert quick_sort(numbers, 0, len(numbers)) == [1, 3, 5, 7, 9]


def test_quick_sort_main_execution(capsys):
    """
    Verify script execution through the __main__ block.

    The module is removed from sys.modules first so runpy
    executes a fresh copy and coverage.py can track execution.
    """

    module_name = "app.quick_sort"

    sys.modules.pop(module_name, None)

    runpy.run_module(module_name, run_name="__main__")

    captured = capsys.readouterr()

    assert captured.out.strip() == "[1, 2, 33, 40, 223]"