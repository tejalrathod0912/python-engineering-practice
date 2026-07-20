from app.first_occurance import find_the_occurrence

import sys
import runpy


def test_binary_search_element_found():
    """
    Verify that binary_search returns the correct index
    when the target element exists in the sorted list.
    """
    numbers = [2, 3, 5, 6, 8, 9, 11, 15, 19, 20]

    result = find_the_occurrence(numbers, 11)

    assert result == 6


def test_binary_search_element_not_found():
    """
    Verify that binary_search returns the appropriate
    message when the target element is not present.
    """
    numbers = [2, 3, 5, 6, 8, 9, 11, 15, 19, 20]

    assert find_the_occurrence(numbers, 0) == "No value found"


def test_binary_search_empty_list():
    """
    Verify that binary_search handles an empty list
    and returns the appropriate message.
    """
    assert find_the_occurrence([], 10) == "No value found"


def test_binary_search_first_element():
    """
    Verify that binary_search correctly finds
    the first element in the sorted list.
    """
    numbers = [2, 3, 5, 6, 8, 9, 11, 15, 19, 20]

    assert find_the_occurrence(numbers, 2) == 0


def test_binary_search_last_element():
    """
    Verify that binary_search correctly finds
    the last element in the sorted list.
    """
    numbers = [2, 3, 5, 6, 8, 9, 11, 15, 19, 20]

    assert find_the_occurrence(numbers, 20) == 9


def test_binary_search_single_element_found():
    """
    Verify that binary_search correctly returns the index
    when the list contains only one matching element.
    """
    assert find_the_occurrence([10], 10) == 0


def test_binary_search_single_element_not_found():
    """
    Verify that binary_search returns the appropriate
    message when a single-element list does not contain
    the target value.
    """
    assert find_the_occurrence([10], 5) == "No value found"


def test_binary_search_main_execution(capsys):
    """
    Verify script execution through the __main__ block.

    The module is removed from sys.modules first so runpy re-executes
    a fresh copy instead of the one already cached from the top-level
    import above — this avoids the "found in sys.modules prior to
    execution" RuntimeWarning while still running in-process so
    coverage.py can track it.
    """
    module_name = "app.first_occurance"
    sys.modules.pop(module_name, None)

    runpy.run_module(module_name, run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out.strip() == "No value found"