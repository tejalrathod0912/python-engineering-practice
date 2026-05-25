"""322. Coin Change
Solved
Medium
Topics
premium lock icon
Companies
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

 

Example 1:

Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1
Example 2:

Input: coins = [2], amount = 3
Output: -1
Example 3:

Input: coins = [1], amount = 0
Output: 0
 

Constraints:

1 <= coins.length <= 12
1 <= coins[i] <= 231 - 1
0 <= amount <= 104


"""

from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        impossible_result = -1
        unreachable = float("inf")
        max_coin_count = 12
        max_coin_value = (2**31) - 1
        max_amount = 10**4

        #Constraints1:
        coin_count = len(coins)
        if coin_count < 1 or coin_count > max_coin_count:
            return impossible_result

        #Constraints2:
        for coin_value in coins:
            if coin_value < 1 or coin_value > max_coin_value:
                return impossible_result
        
        #Constraints3:
        if amount < 0 or amount > max_amount:
            return impossible_result

        min_coins_by_amount = [unreachable] * (amount + 1)
        min_coins_by_amount[0] = 0

        for coin_value in coins:
            for current_amount in range(coin_value, amount + 1):
                previous_amount = current_amount - coin_value
                candidate_coin_count = min_coins_by_amount[previous_amount] + 1
                min_coins_by_amount[current_amount] = min(
                    min_coins_by_amount[current_amount],
                    candidate_coin_count,
                )

        minimum_coin_count = min_coins_by_amount[amount]
        if minimum_coin_count == unreachable:
            return impossible_result

        return minimum_coin_count


def run_coin_change_example() -> None:
    coins = [1, 2, 5]
    amount = 11

    solution = Solution()
    minimum_coin_count = solution.coinChange(coins, amount)

    print(f"Coins: {coins}")
    print(f"Amount: {amount}")
    print(f"Minimum coins required: {minimum_coin_count}")


if __name__ == "__main__":
    run_coin_change_example()
