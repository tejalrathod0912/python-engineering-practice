'''
912. Sort an Array

Given an array of integers nums, sort the array in ascending order and return it.

You must solve the problem without using any built-in sorting functions
in O(nlog(n)) time complexity and with the smallest space complexity possible.


Example 1:

Input:
nums = [5,2,3,1]

Output:
[1,2,3,5]

Explanation:
After sorting the array, the positions of some numbers are not changed
(for example, 2 and 3), while the positions of other numbers are changed
(for example, 1 and 5).


Example 2:

Input:
nums = [5,1,1,2,0,0]

Output:
[0,0,1,1,2,5]

Explanation:
The values in nums are not necessarily unique.


Constraints:

1 <= nums.length <= 5 * 10^4

-5 * 10^4 <= nums[i] <= 5 * 10^4


----------------------- Explanation -----------------------

This problem is solved using Merge Sort.

Merge Sort follows the Divide and Conquer approach:

1. Divide:
   Split the array into two halves recursively until each sub-array
   contains one element.

2. Conquer:
   Merge two sorted sub-arrays by comparing elements and placing them
   in sorted order.

3. Combine:
   Continue merging until the complete array becomes sorted.


Time Complexity:

Best Case    : O(n log n)
Average Case : O(n log n)
Worst Case   : O(n log n)


Space Complexity:

O(n)

Extra space is required because temporary arrays are created during merging.

----------------------------------------------------------
'''


from typing import List


class Solution:

    def merge(
        self,
        nums: List[int],
        left_index: int,
        middle_index: int,
        right_index: int
    ) -> None:

        left_array = nums[left_index:middle_index]
        right_array = nums[middle_index:right_index]

        left_pointer = 0
        right_pointer = 0
        merge_pointer = left_index


        while left_pointer < len(left_array) and right_pointer < len(right_array):

            if left_array[left_pointer] <= right_array[right_pointer]:
                nums[merge_pointer] = left_array[left_pointer]
                left_pointer += 1

            else:
                nums[merge_pointer] = right_array[right_pointer]
                right_pointer += 1

            merge_pointer += 1


        while left_pointer < len(left_array):

            nums[merge_pointer] = left_array[left_pointer]
            left_pointer += 1
            merge_pointer += 1


        while right_pointer < len(right_array):

            nums[merge_pointer] = right_array[right_pointer]
            right_pointer += 1
            merge_pointer += 1



    def merge_sort(
        self,
        nums: List[int],
        left_index: int,
        right_index: int
    ) -> None:

        if right_index - left_index > 1:

            middle_index = (left_index + right_index) // 2

            self.merge_sort(
                nums,
                left_index,
                middle_index
            )

            self.merge_sort(
                nums,
                middle_index,
                right_index
            )

            self.merge(
                nums,
                left_index,
                middle_index,
                right_index
            )



    def sort_array(self, nums: List[int]) -> List[int]:

        minimum_length = 1
        maximum_length = 5 * 10**4

        minimum_value = -5 * 10**4
        maximum_value = 5 * 10**4


        if len(nums) < minimum_length or len(nums) > maximum_length:
            raise ValueError(
                "Array length must be between 1 and 50000"
            )


        for number in nums:
            if number < minimum_value or number > maximum_value:
                raise ValueError(
                    "Array values must be between -50000 and 50000"
                )


        self.merge_sort(
            nums,
            0,
            len(nums)
        )

        return nums



def run_merge_sort_example() -> None:

    input_array = [5, 1, 1000, 2, 0, 0]
    print(f"Input Array: {input_array}")

    solution = Solution()

    sorted_array = solution.sort_array(input_array)
    

    print(f"Sorted Array: {sorted_array}")



if __name__ == "__main__":

    run_merge_sort_example()