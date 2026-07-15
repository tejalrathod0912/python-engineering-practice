def insertion_sort_arr(arr):
    """
    Sort a list of integers using Insertion Sort.

    Algorithm:
    - Iterate through the list, starting from the second element.
    - Compare the current element with the elements in the sorted section.
    - Shift elements in the sorted section to the right to make space for the current element.
    - Insert the current element into its correct position in the sorted section.

    Time Complexity:
        Best Case    : O(n)    -> Array is already sorted
        Average Case : O(n²)
        Worst Case   : O(n²)

    Space Complexity:
        O(1) - Sorting is performed in-place.
    """
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
       

    return arr

if __name__ == "__main__":
    numbers = [90, 20, 12, 3, 21, 2, 0]
    print(insertion_sort_arr(numbers))