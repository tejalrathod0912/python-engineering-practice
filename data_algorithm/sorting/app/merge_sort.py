"""
Sort a list of integers using Merge Sort.

Algorithm:
- Divide the list into two halves recursively.
- Continue dividing until each sublist contains only one element.
- Merge the sorted sublists by comparing their elements.
- Repeat until the entire list is merged into a single sorted list.

Time Complexity:
    Best Case    : O(n log n)
    Average Case : O(n log n)
    Worst Case   : O(n log n)

Merge Sort has a time complexity of O(n log n) because of two things happening together:

The array is divided repeatedly → contributes log n
Each level performs merging of all n elements → contributes n

So,

Time Complexity=nXlogn=O(nlogn)

Space Complexity:
    O(n) - Additional space is required for temporary sublists.
"""

from typing import List


def merge(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    Merge two sorted halves of the array.

    Parameters:
        arr   : List of integers
        left  : Starting index (inclusive)
        mid   : Middle index
        right : Ending index (exclusive)
    """

    left_part = arr[left:mid]
    right_part = arr[mid:right]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


def merge_sort(arr: List[int], left: int, right: int) -> List[int]:
    """
    Recursively sort the array using Merge Sort.

    Parameters:
        arr   : List of integers
        left  : Starting index (inclusive)
        right : Ending index (exclusive)

    Returns:
        Sorted list.
    """

    if right - left > 1:
        mid = (left + right) // 2

        merge_sort(arr, left, mid)
        merge_sort(arr, mid, right)
        merge(arr, left, mid, right)

    return arr


if __name__ == "__main__":
    numbers: List[int] = [100, 34, 2, 300, 45]

    print(merge_sort(numbers, 0, len(numbers)))