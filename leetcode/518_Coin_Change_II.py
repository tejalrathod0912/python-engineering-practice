'''518. Coin Change II
Solved
Medium
Topics
premium lock icon
Companies
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

 

Example 1:

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
Example 2:

Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.
Example 3:

Input: amount = 10, coins = [10]
Output: 1
 

Constraints:

1 <= coins.length <= 300
1 <= coins[i] <= 5000
All the values of coins are unique.
0 <= amount <= 5000'''

from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        no_combination_count = 0
        min_coin_count = 1
        max_coin_count = 300
        min_coin_value = 1
        max_coin_value = 5000
        min_amount = 0
        max_amount = 5000

        coin_count = len(coins)
        if coin_count < min_coin_count or coin_count > max_coin_count:
            return no_combination_count

        if len(set(coins)) != coin_count:
            return no_combination_count

        for coin_value in coins:
            if coin_value < min_coin_value or coin_value > max_coin_value:
                return no_combination_count

        if amount < min_amount or amount > max_amount:
            return no_combination_count

        combinations_by_amount = [0] * (amount + 1)
        combinations_by_amount[0] = 1

        for coin_value in coins:
            for current_amount in range(coin_value, amount + 1):
                remaining_amount = current_amount - coin_value
                combinations_by_amount[current_amount] += combinations_by_amount[
                    remaining_amount
                ]

        return combinations_by_amount[amount]


def run_coin_change_example() -> None:
    amount = 5
    coins = [1, 2, 5]

    solution = Solution()
    combination_count = solution.change(amount, coins)

    print(f"Amount: {amount}")
    print(f"Coins: {coins}")
    print(f"Number of combinations: {combination_count}")


if __name__ == "__main__":
    run_coin_change_example()
