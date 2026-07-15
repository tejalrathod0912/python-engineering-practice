"""
    Sort a list of integers using Selection Sort.

    Algorithm:
    - Divide the list into sorted and unsorted sections.
    - Find the smallest element from the unsorted section.
    - Swap it with the first element of the unsorted section.

    Time Complexity:
        Best Case    : O(n²)
        Average Case : O(n²)
        Worst Case   : O(n²)

    Space Complexity:
        O(1) - Sorting is performed in-place.
"""

from typing import List

def selection_sort_arr(arr: List[int]) -> List[int]:
   

    n = len(arr)

    for i in range(n - 1):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


if __name__ == "__main__":
    numbers: List[int] = [0, 2, 3, 12, 20, 21, 90]

    print(selection_sort_arr(numbers))