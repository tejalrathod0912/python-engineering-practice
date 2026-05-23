"""Solve the rod cutting problem using unbounded knapsack dynamic programming.

Code explanation:
    This module solves the classic "rod cutting" problem. A rod has a target
    length, and ``prices[i]`` stores the selling price for a piece of length
    ``i + 1``. The goal is to choose cuts that produce the highest possible
    total price.

    Rod cutting is an unbounded knapsack problem because each cut length can be
    used more than once. For example, a rod of length 8 could be sold as eight
    pieces of length 1, four pieces of length 2, or any other combination whose
    lengths add up to 8.

    The dynamic programming list stores the best revenue for every target rod
    length from 0 through ``length``:
        1. Base case:
           A rod of length 0 has revenue 0. Before any piece sizes are checked,
           every target length also starts with revenue 0.
        2. Recurrence:
           For each piece length, check every current rod length. If the piece
           fits, compare the current best revenue with the revenue from taking
           that piece plus the best revenue for the remaining length. Because
           the same ``dp_length`` list is reused, each piece length can be used
           more than once.

    Example:
        Input:  length=8, prices=[2, 4, 10, 4, 9]
        Output: 24

    Complexity:
        Time complexity is O(n * length), where n is the number of provided
        prices.

        Space complexity is O(length) for the dynamic programming list.
"""

import logging


LOGGER = logging.getLogger(__name__)


def rod_cutting(length: int, prices: list[int]) -> int:
    """Return the maximum revenue possible for a rod of ``length``.

    Args:
        length: The total rod length to cut.
        prices: Prices for piece lengths 1 through ``len(prices)``.

    Returns:
        The best revenue that can be earned by cutting and selling the rod.

    Raises:
        ValueError: If ``length`` is negative or any price is negative.

    Examples:
        >>> rod_cutting(8, [2, 4, 10, 4, 9])
        24
    """
    if length < 0:
        raise ValueError("length cannot be negative")

    if any(price < 0 for price in prices):
        raise ValueError("prices cannot contain negative values")

    LOGGER.debug("Calculating best revenue for length=%s, prices=%s", length, prices)

    dp_length = [0] * (length + 1)

    piece_len = len(prices)
    for piece in range(1, piece_len + 1):
        for current_length in range(1, length + 1):

            if current_length >= piece:
                remaining_length = current_length - piece
                candidate_revenue = prices[piece - 1] + dp_length[remaining_length]
                dp_length[current_length] = max(dp_length[current_length], candidate_revenue)
                LOGGER.debug(
                    "piece=%s current_length=%s candidate_revenue=%s best=%s",
                    piece,
                    current_length,
                    candidate_revenue,
                    dp_length[current_length],
                )

            continue

    result = dp_length[length]
    LOGGER.debug("Best revenue: %s", result)
    return result


class RodCutting:
    """Backward-compatible wrapper around the rod cutting function."""

    def rod_cutting_func(self, length: int, prices: list[int]) -> int:
        """Return the best revenue for the given rod length and prices."""
        LOGGER.debug("RodCutting wrapper called with length=%s, prices=%s", length, prices)
        return rod_cutting(length, prices)


if __name__ == "__main__":
    rod_length = 8
    rod_length_prices = [2, 4, 10, 4, 9]
    print(rod_cutting(rod_length, rod_length_prices))
