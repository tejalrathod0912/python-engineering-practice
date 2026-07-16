from app.merge_sort import merge_sort

import sys
import runpy


def test_merge_sort_returns_sorted_list():
    """
    Verify that merge_sort correctly sorts an unsorted list
    containing multiple integer values in ascending order.
    """
    numbers = [64, 34, 25, 12, 22, 11, 90]

    result = merge_sort(numbers, 0, len(numbers))

    assert result == [11, 12, 22, 25, 34, 64, 90]


def test_merge_sort_empty_list():
    """
    Verify that merge_sort handles an empty list
    and returns an empty list without errors.
    """
    assert merge_sort([], 0, 0) == []


def test_merge_sort_already_sorted_list():
    """
    Verify that merge_sort does not modify an already sorted list
    and returns the same sorted order.
    """
    numbers = [1, 2, 3, 4, 5]

    assert merge_sort(numbers, 0, len(numbers)) == [1, 2, 3, 4, 5]


def test_merge_sort_with_duplicate_values():
    """
    Verify that merge_sort correctly handles duplicate values
    and maintains all occurrences in the sorted output.
    """
    numbers = [5, 2, 8, 2, 1]

    assert merge_sort(numbers, 0, len(numbers)) == [1, 2, 2, 5, 8]


def test_merge_sort_with_negative_numbers():
    """
    Verify that merge_sort correctly sorts lists containing
    negative and positive integer values.
    """
    numbers = [-5, 3, -1, 0, 8]

    assert merge_sort(numbers, 0, len(numbers)) == [-5, -1, 0, 3, 8]


def test_merge_sort_single_element():
    """
    Verify that merge_sort correctly handles a list containing
    only one element.
    """
    numbers = [42]

    assert merge_sort(numbers, 0, len(numbers)) == [42]


def test_merge_sort_main_execution(capsys):
    """
    Verify script execution through the __main__ block.

    The module is removed from sys.modules first so runpy re-executes
    a fresh copy instead of the one already cached from the top-level
    import above — this avoids the "found in sys.modules prior to
    execution" RuntimeWarning while still running in-process so
    coverage.py can track it.
    """
    module_name = "app.merge_sort"
    sys.modules.pop(module_name, None)

    runpy.run_module(module_name, run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out.strip() == "[2, 34, 45, 100, 300]"