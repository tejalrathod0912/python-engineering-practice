"""Tests for the recursive array flattening implementation."""

import io # Used for capturing printed output in the test case that checks module execution behavior.
import runpy # Used to execute the module as a script and capture its output for testing. 
import unittest # The unittest framework is used to define and run the test cases for the flattening function and class.
from contextlib import redirect_stdout # Used to redirect standard output to a string buffer for testing the module's print behavior when run as a script.
from pathlib import Path # Used to construct the path to the module being tested when executing it as a script in the test case.

'''import the function and class to be tested from the recursion_code module.'''
from data_algorithm.recursion.recursion_code.flatten_the_array import (
    FlattenTheArray,
    flatten_array,
)


class TestFlattenArray(unittest.TestCase):
    """Validate flattening behavior for normal and edge-case inputs."""

    def test_flatten_array_with_nested_numbers(self) -> None:
        ''' The function should correctly flatten a list containing nested lists of integers.'''
        nested_items = [1, 2, [3, 4], 5, [6, 7, 8], 9]

        self.assertEqual(
            flatten_array(nested_items),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        )

    def test_flatten_array_with_empty_list(self) -> None:
        '''The function should return an empty list when given an empty list as input.'''
        self.assertEqual(flatten_array([]), [])

    def test_flatten_array_with_empty_nested_lists(self) -> None:
        '''The function should ignore empty nested lists and only return non-list values.'''
        self.assertEqual(flatten_array([[], [1, [], [2]], []]), [1, 2])

    def test_flatten_array_with_deeply_nested_list(self) -> None:
        '''The function should correctly flatten lists nested to any depth.'''
        nested_items = [1, [2, [3, [4, [5]]]]]

        self.assertEqual(flatten_array(nested_items), [1, 2, 3, 4, 5])

    def test_flatten_array_with_single_element(self) -> None:
        '''The function should return a single-element list unchanged.'''
        self.assertEqual(flatten_array([42]), [42])

    def test_flatten_array_preserves_non_list_values(self) -> None:
        '''The function should correctly flatten nested lists while preserving non-list values of any type.'''
        nested_items = ["python", [True, [None, 3.14]], {"topic": "recursion"}]

        self.assertEqual(
            flatten_array(nested_items),
            ["python", True, None, 3.14, {"topic": "recursion"}],
        )

    def test_flatten_array_does_not_mutate_input(self) -> None:
        '''The original input list should remain unchanged after flattening.'''
        nested_items = [1, [2, [3]]]

        self.assertEqual(flatten_array(nested_items), [1, 2, 3])
        self.assertEqual(nested_items, [1, [2, [3]]])

    def test_flatten_the_array_class_wrapper(self) -> None:
        '''The FlattenTheArray class should provide the same flattening functionality as the standalone function.'''
        flattener = FlattenTheArray()

        self.assertEqual(flattener.flatten([1, [2, [3]]]), [1, 2, 3])

    def test_module_prints_sample_output_when_run_as_script(self) -> None:
        '''When the module is executed directly, it should print the flattened version of the sample input list.'''
        module_path = (
            Path(__file__).resolve().parents[1]
            / "recursion_code"
            / "flatten_the_array.py"
        )
        output = io.StringIO()

        with redirect_stdout(output):
            runpy.run_path(str(module_path), run_name="__main__")

        self.assertEqual(output.getvalue().strip(), "[1, 2, 3, 4, 5, 6, 7, 8, 9]")


if __name__ == "__main__":
    unittest.main()
