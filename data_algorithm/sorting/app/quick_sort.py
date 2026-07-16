"""
Sort a list of integers using Quick Sort.

Algorithm:
- Select the first element as the pivot.
- Partition the array into two parts:
    - Elements smaller than or equal to pivot.
    - Elements greater than pivot.
- Recursively sort both partitions.

Time Complexity:
    Best Case    : O(n log n)
    Average Case : O(n log n)
    Worst Case   : O(n²) - > array is sorted 

Space Complexity:
     O(n) - Recursive call stack in the worst case.
"""

from typing import List


def partition(arr: List[int], left: int, right: int) -> int:
    """
    Partition the array around a pivot element.

    Parameters:
        arr   : List of integers
        left  : Starting index (inclusive)
        right : Ending index (exclusive)

    Returns:
        Pivot index after partitioning.
    """

    pivot = arr[left]

    i = left + 1
    j = right - 1

    while True:

        while i <= j and arr[i] <= pivot:
            i += 1

        while i <= j and arr[j] >= pivot:
            j -= 1

        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break

    arr[left], arr[j] = arr[j], arr[left]

    return j


def quick_sort(arr: List[int], left: int, right: int) -> List[int]:
    """
    Recursively sort the array using Quick Sort.

    Parameters:
        arr   : List of integers
        left  : Starting index (inclusive)
        right : Ending index (exclusive)

    Returns:
        Sorted list.
    """

    if right - left > 1:

        pivot_index = partition(arr, left, right)

        quick_sort(arr, left, pivot_index)
        quick_sort(arr, pivot_index + 1, right)

    return arr


if __name__ == "__main__":

    numbers: List[int] = [40, 2, 1, 223, 33]

    print(quick_sort(numbers, 0, len(numbers)))