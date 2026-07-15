"""
Bubble Sort Algorithm:

- In each pass, adjacent elements are compared.
- If the left element is greater than the right element, they are swapped.
- After each pass, the largest unsorted element moves ("bubbles") to its correct position.
- If no swapping happens in a complete pass, the array is already sorted.

Time Complexity:
    Best Case    : O(n)    -> Array is already sorted (optimization using swapped flag)
    Average Case : O(n²)
    Worst Case   : O(n²)

Space Complexity:
    O(1) -> Sorting is performed in-place without extra memory.
"""

from typing import List


def bubble_sort_arr(arr: List[int]) -> List[int]:
    n = len(arr)

    for i in range(n - 1):
        swapped = False

        # Last i elements are already sorted after each pass
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no swaps occurred, array is already sorted
        if not swapped:
            break

    return arr


if __name__ == "__main__":
    numbers = [90, 20, 12, 3, 21, 2, 0]
    print(bubble_sort_arr(numbers))