"""Minimum coin change using unbounded dynamic programming.

Problem:
    Given a sequence of positive coin denominations and a target sum, find the
    minimum number of coins required to make exactly that target. Each coin can
    be used unlimited times.

Approach:
    This module uses a bottom-up dynamic programming strategy. ``dp[amount]``
    stores the minimum number of coins needed to make ``amount``. For each coin,
    the table is updated from ``coin`` through ``target_sum`` so the same coin
    may be reused, which is the key property of unbounded coin change.

Complexity:
    Time complexity is O(n * target_sum), where n is the number of coin
    denominations. Space complexity is O(target_sum).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
import logging
from typing import Protocol


LOGGER = logging.getLogger(__name__)
IMPOSSIBLE_RESULT = -1


class CoinChangeSolver(Protocol):
    """Strategy interface for minimum coin-change algorithms."""

    def minimum_coins(self, coins: Sequence[int], target_sum: int) -> int:
        """Return the minimum coins required to make ``target_sum``."""


class CoinChangeInputValidator:
    """Validate and normalize input for coin-change solvers."""

    def validate(self, coins: Sequence[int], target_sum: int) -> tuple[int, ...]:
        """Return validated coin denominations as an immutable tuple.

        Args:
            coins: Positive integer coin denominations.
            target_sum: Non-negative amount to construct.

        Raises:
            TypeError: If ``coins`` is not a sequence or values are not integers.
            ValueError: If ``target_sum`` is negative or coins are non-positive.
        """
        if not isinstance(coins, Sequence):
            raise TypeError("coins must be a sequence of positive integers")

        if not isinstance(target_sum, int) or isinstance(target_sum, bool):
            raise TypeError("target_sum must be an integer")

        if target_sum < 0:
            raise ValueError("target_sum cannot be negative")

        if any(not isinstance(coin, int) or isinstance(coin, bool) for coin in coins):
            raise TypeError("coins must contain only integer values")

        if any(coin <= 0 for coin in coins):
            raise ValueError("coins must contain only positive values")

        # Sorting unique denominations keeps the DP deterministic and avoids
        # doing the same transition more than once for duplicate coin values.
        return tuple(sorted(set(coins)))


@dataclass(frozen=True, slots=True)
class DynamicProgrammingCoinChangeSolver:
    """Compute minimum coin count with a bottom-up DP strategy.

    The class is stateless apart from its injected validator dependency, making
    it easy to test and swap with another ``CoinChangeSolver`` implementation.
    """

    validator: CoinChangeInputValidator = field(default_factory=CoinChangeInputValidator)

    def minimum_coins(self, coins: Sequence[int], target_sum: int) -> int:
        """Return the minimum coins required to make a target sum.

        Args:
            coins: Positive integer denominations that may be reused.
            target_sum: Non-negative target amount.

        Returns:
            The minimum number of coins required, or ``-1`` when no combination
            can make the target.

        Raises:
            TypeError: If inputs have invalid types.
            ValueError: If inputs contain invalid values.
        """
        try:
            normalized_coins = self.validator.validate(coins, target_sum)
        except (TypeError, ValueError):
            LOGGER.exception(
                "Invalid minimum coin-change input: coin_count=%s, target_sum=%s",
                len(coins) if isinstance(coins, Sequence) else "unknown",
                target_sum,
            )
            raise

        LOGGER.debug(
            "Calculating minimum coins for coins=%s, target_sum=%s",
            list(normalized_coins),
            target_sum,
        )

        if target_sum == 0:
            return 0

        if not normalized_coins:
            return IMPOSSIBLE_RESULT

        unreachable = target_sum + 1
        min_coins_by_amount = [unreachable] * (target_sum + 1)
        min_coins_by_amount[0] = 0

        for coin in normalized_coins:
            for amount in range(coin, target_sum + 1):
                previous_amount = amount - coin
                candidate_count = min_coins_by_amount[previous_amount] + 1

                if candidate_count < min_coins_by_amount[amount]:
                    min_coins_by_amount[amount] = candidate_count
                    LOGGER.debug(
                        "Updated minimum coin count: coin=%s amount=%s count=%s",
                        coin,
                        amount,
                        candidate_count,
                    )

        result = min_coins_by_amount[target_sum]
        if result == unreachable:
            LOGGER.debug("No coin combination can make target_sum=%s", target_sum)
            return IMPOSSIBLE_RESULT

        LOGGER.debug("Minimum coins required: %s", result)
        return result


def min_coin_change(coins: Sequence[int], target_sum: int) -> int:
    """Return the minimum number of coins needed to make ``target_sum``.

    This convenience function keeps callers decoupled from the concrete solver
    class while using the default dynamic programming strategy.
    """
    solver: CoinChangeSolver = DynamicProgrammingCoinChangeSolver()
    return solver.minimum_coins(coins, target_sum)


def run_min_coin_change_example() -> int:
    """Run a small example and print the minimum number of coins required.

    Returns:
        Process exit code. ``0`` means success and ``1`` means invalid input.
    """
    try:
        print(min_coin_change([1, 2, 3, 5], 5))
        return 0
    except (TypeError, ValueError) as error:
        LOGGER.error("Could not calculate minimum coins: %s", error)
        return 1


@dataclass(frozen=True, slots=True)
class MinNumberOfCoinsForTargetSum:
    """Backward-compatible class wrapper for the original exercise name."""

    solver: DynamicProgrammingCoinChangeSolver = field(
        default_factory=DynamicProgrammingCoinChangeSolver
    )

    def get_min_number_of_coins(self, coins: Sequence[int], target_sum: int) -> int:
        """Return the minimum number of coins required for ``target_sum``."""
        return self.solver.minimum_coins(coins, target_sum)


if __name__ == "__main__":
    raise SystemExit(run_min_coin_change_example())
