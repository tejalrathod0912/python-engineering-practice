"""Count coin-change combinations using unbounded knapsack dynamic programming.

Code explanation:
    This module solves the classic coin change problem: given a list of coin
    denominations and a target sum, count how many unique combinations can make
    that sum when each coin can be used any number of times.

    The dynamic programming table stores the number of combinations for every
    intermediate target sum:
        1. Base case:
           There is exactly one way to make a sum of 0: choose no coins.
        2. Recurrence:
           For each coin, add the known combinations for the remaining sum. The
           outer coin loop ensures combinations are counted once, independent of
           coin order.

    Example:
        Input:  coins=[1, 2, 3], target_sum=5
        Output: 5

    Complexity:
        Time complexity is O(n * target_sum), where n is the number of coins.

        Space complexity is O(target_sum) for the dynamic programming table.
"""

import logging
from collections.abc import Sequence


LOGGER = logging.getLogger(__name__)


class CoinChangeInputValidator:
    """Validate and normalize coin-change input.

    This class has one responsibility: protect the algorithm from invalid input.
    Keeping validation separate makes the counter easier to test and change.
    """

    def validate(self, coins: Sequence[int], target_sum: int) -> tuple[int, ...]:
        """Return normalized coins after validating the target and coins."""
        if target_sum < 0:
            raise ValueError("target_sum cannot be negative")

        normalized_coins = tuple(coins)
        if any(coin <= 0 for coin in normalized_coins):
            raise ValueError("coins must contain only positive values")

        return normalized_coins


class CoinChangeCombinationCounter:
    """Count unique coin-change combinations using dynamic programming.

    The counter depends on a validator abstraction injected through the
    constructor. This keeps the algorithm loosely coupled and makes the
    validation behavior easy to replace in tests or future extensions.
    """

    def __init__(self, validator: CoinChangeInputValidator | None = None) -> None:
        """Create a counter with a validator dependency."""
        self._validator = validator or CoinChangeInputValidator()

    def count(self, coins: Sequence[int], target_sum: int) -> int:
        """Return the number of unique combinations that make ``target_sum``.

        Args:
            coins: Positive coin denominations that can be reused.
            target_sum: Target sum to create from the available coins.

        Returns:
            The number of unique coin combinations that sum to ``target_sum``.

        Raises:
            ValueError: If ``target_sum`` is negative or any coin is not positive.

        Examples:
            >>> CoinChangeCombinationCounter().count([1, 2, 3], 5)
            5
        """
        normalized_coins = self._validator.validate(coins, target_sum)

        LOGGER.debug(
            "Counting coin combinations for coins=%s, target_sum=%s",
            list(normalized_coins),
            target_sum,
        )

        combinations_by_sum = [0] * (target_sum + 1)
        combinations_by_sum[0] = 1

        for coin_value in normalized_coins:
            for current_sum in range(coin_value, target_sum + 1):
                remaining_sum = current_sum - coin_value
                previous_combinations = combinations_by_sum[current_sum]
                combinations_by_sum[current_sum] += combinations_by_sum[remaining_sum]
                LOGGER.debug(
                    "coin_value=%s current_sum=%s previous_ways=%s added_ways=%s total_ways=%s",
                    coin_value,
                    current_sum,
                    previous_combinations,
                    combinations_by_sum[remaining_sum],
                    combinations_by_sum[current_sum],
                )

        number_of_ways = combinations_by_sum[target_sum]
        LOGGER.debug("Number of combinations: %s", number_of_ways)
        return number_of_ways


def count_coin_change_combinations(coins: Sequence[int], target_sum: int) -> int:
    """Return the number of unique combinations that make ``target_sum``.

    Args:
        coins: Positive coin denominations that can be reused.
        target_sum: Target sum to create from the available coins.

    Returns:
        The number of unique coin combinations that sum to ``target_sum``.

    Raises:
        ValueError: If ``target_sum`` is negative or any coin is not positive.

    Examples:
        >>> count_coin_change_combinations([1, 2, 3], 5)
        5
    """
    return CoinChangeCombinationCounter().count(coins, target_sum)


def max_subset_sum(coins: Sequence[int], coins_sum: int) -> int:
    """Return the number of combinations that make ``coins_sum``.

    This name is kept for existing callers. Prefer
    :func:`count_coin_change_combinations` in new code because it describes the
    business behavior more clearly.
    """
    try:
        return count_coin_change_combinations(coins, coins_sum)
    except ValueError as error:
        if str(error) == "target_sum cannot be negative":
            raise ValueError("coins_sum cannot be negative") from error
        raise


class CoinChangeMaximumNumberWays:
    """Backward-compatible class interface for existing callers."""

    def __init__(self, counter: CoinChangeCombinationCounter | None = None) -> None:
        """Create the wrapper with an injected counter dependency."""
        self._counter = counter or CoinChangeCombinationCounter()

    def max_subset_fun(self, coins: Sequence[int], target_sum: int) -> int:
        """Return the number of combinations for the given coins and target."""
        LOGGER.debug(
            "CoinChangeMaximumNumberWays wrapper called with coins=%s, target_sum=%s",
            coins,
            target_sum,
        )
        return self._counter.count(coins, target_sum)


# __all__ = [
#     "CoinChangeCombinationCounter",
#     "CoinChangeInputValidator",
#     "CoinChangeMaximumNumberWays",
#     "count_coin_change_combinations",
#     "max_subset_sum",
# ]


if __name__ == "__main__":
    coins_list = [1, 2, 3]
    required_sum = 5

    coin_change_counter = CoinChangeCombinationCounter()
    print(coin_change_counter.count(coins_list, required_sum))
