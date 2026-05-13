"""Flatten a nested list using recursion.

Code explanation:
    This module solves the "flatten the array" problem. The input can contain
    normal values and other lists nested at any depth. The goal is to return a
    new single-level list while keeping the original left-to-right order.

    Recursion is a good fit because every nested list is the same problem as the
    original input, only smaller. The function repeatedly breaks the problem
    down until it reaches values that are not lists.

    The solution has two important parts:
        1. Base case:
           If the current item is not a list, append it to the result because it
           cannot be flattened any further.
        2. Recursive step:
           If the current item is a list, call ``flatten_array`` again for that
           nested list and extend the result with the flattened values.

    Example:
        Input:  [1, 2, [3, 4], [5, [6, 7]]]
        Output: [1, 2, 3, 4, 5, 6, 7]

    Complexity:
        Time complexity is O(n), where n is the total number of values and
        nested list containers visited. Each item is processed once.

        Space complexity is O(n + d), where n is the size of the flattened
        output list and d is the maximum recursion depth caused by nesting.
"""

from typing import Any


def flatten_array(items: list[Any]) -> list[Any]:
    """Return a new list with all nested list values flattened.

    The function walks through each item in ``items``. When the current item is
    another list, the same function is called again for that smaller list. When
    the current item is not a list, it is already a final value and can be
    appended directly to the result.

    Args:
        items: A list that may contain values and other nested lists.

    Returns:
        A new flat list containing all non-list values in their original order.

    Examples:
        >>> flatten_array([1, [2, [3]], 4])
        [1, 2, 3, 4]
    """
    flattened: list[Any] = []

    for item in items:
        if isinstance(item, list):
            # Recursive step: solve the same problem for the smaller nested list.
            flattened.extend(flatten_array(item))
            continue

        # Base case: a non-list value cannot be flattened further.
        flattened.append(item)

    return flattened


class FlattenTheArray:
    """Backward-compatible wrapper around the recursive flattening function."""

    def flatten(self, items: list[Any]) -> list[Any]:
        """Flatten a nested list while preserving the original item order."""
        return flatten_array(items)


if __name__ == "__main__":
    sample_input = [1, 2, [3, 4], 5, [6, 7, 8], 9]
    print(flatten_array(sample_input))
