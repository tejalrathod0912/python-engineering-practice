def find_the_occurrence(arr, ele):
    """
    Find the index of an element in a sorted list using Binary Search.

    Algorithm:
    - Initialize two pointers:
        - start at the beginning of the list.
        - end at the last index of the list.
    - Repeat until start is less than or equal to end:
        - Find the middle index.
        - If the middle element matches the target, return its index.
        - If the target is greater than the middle element,
          search the right half.
        - Otherwise, search the left half.
    - If the element is not found, return a message.

    Time Complexity:
        Best Case    : O(1)      -> Element found at the middle
        Average Case : O(log n)
        Worst Case   : O(log n)

    Space Complexity:
        O(1) - Uses constant extra space.
    """

    start = 0
    end = len(arr) - 1

    while start <= end:
        mid = (start + end) // 2

        if arr[mid] == ele:
            return mid

        elif arr[mid] < ele:
            start = mid + 1

        else:
            end = mid - 1

    return "No value found"


if __name__ == "__main__":
    arr = [2, 3, 5, 6, 8, 9, 11, 15, 19, 20]
    ele = 0

    print(find_the_occurrence(arr, ele))