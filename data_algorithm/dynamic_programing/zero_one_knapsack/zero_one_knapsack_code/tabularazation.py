"""0/1 knapsack solved with bottom-up dynamic programming.

Definition:
    Given item weights, item values, and a maximum knapsack capacity, choose a
    subset of items that maximizes total value without exceeding capacity. In
    the 0/1 version, each item can be selected at most once.

Logic:
    The algorithm builds a table where ``dp[item_count][capacity]`` stores the
    best value possible using the first ``item_count`` items and the given
    ``capacity``. For every item, we compare two choices:

    1. Exclude the item and keep the previous best value.
    2. Include the item when it fits, then add its value to the best value for
       the remaining capacity.

    The final answer is stored in the bottom-right cell of the table.

Complexity:
    Time complexity is O(n * capacity), where n is the number of items.
    Space complexity is O(n * capacity) for the dynamic programming table.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from typing import Final, Protocol

from config.logging_config import configure_logging, get_logger


LOGGER = get_logger(__name__)
MAX_ITEMS: Final[int] = 1_000
MAX_CAPACITY: Final[int] = 100_000


class KnapsackSolver(Protocol):
    """Strategy interface for 0/1 knapsack algorithms."""

    def maximize_value(
        self,
        weights: Sequence[int],
        values: Sequence[int],
        capacity: int,
    ) -> int:
        """Return the maximum value that can fit in the knapsack."""


@dataclass(slots=True)
class KnapsackInputValidator:
    """Validate and normalize 0/1 knapsack input.

    This class has one responsibility: fail fast before the algorithm builds a
    dynamic programming table. Keeping validation separate makes the solver
    easier to test and replace.
    """

    max_items: int = MAX_ITEMS
    max_capacity: int = MAX_CAPACITY

    def validate(
        self,
        weights: Sequence[int],
        values: Sequence[int],
        capacity: int,
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Return immutable weights and values after validation.

        Args:
            weights: Positive integer item weights.
            values: Non-negative integer item values.
            capacity: Non-negative integer capacity of the knapsack.

        Raises:
            TypeError: If inputs use invalid types.
            ValueError: If inputs use invalid values or mismatched lengths.
        """
        self.validate_capacity(capacity)
        normalized_weights = self.validate_weights(weights)
        normalized_values = self.validate_values(values)
        self.validate_item_counts_match(normalized_weights, normalized_values)
        self.validate_item_count_limit(normalized_weights)

        return normalized_weights, normalized_values

    def validate_capacity(self, capacity: int) -> int:
        """Return ``capacity`` after validating type, range, and max limit."""
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")

        if capacity < 0:
            raise ValueError("capacity cannot be negative")

        if capacity > self.max_capacity:
            raise ValueError(f"capacity cannot exceed {self.max_capacity}")

        return capacity

    def validate_weights(self, weights: Sequence[int]) -> tuple[int, ...]:
        """Return item weights after validating they are positive integers."""
        if not isinstance(weights, Sequence) or isinstance(
            weights,
            (str, bytes, bytearray),
        ):
            raise TypeError("weights must be a sequence of integers")

        normalized_weights = tuple(weights)

        if any(
            not isinstance(weight, int) or isinstance(weight, bool)
            for weight in normalized_weights
        ):
            raise TypeError("weights must contain only integer values")

        if any(weight <= 0 for weight in normalized_weights):
            raise ValueError("weights must contain only positive values")

        return normalized_weights

    def validate_values(self, values: Sequence[int]) -> tuple[int, ...]:
        """Return item values after validating they are non-negative integers."""
        if not isinstance(values, Sequence) or isinstance(
            values,
            (str, bytes, bytearray),
        ):
            raise TypeError("values must be a sequence of integers")

        normalized_values = tuple(values)

        if any(
            not isinstance(value, int) or isinstance(value, bool)
            for value in normalized_values
        ):
            raise TypeError("values must contain only integer values")

        if any(value < 0 for value in normalized_values):
            raise ValueError("values must contain only non-negative values")

        return normalized_values

    def validate_item_counts_match(
        self,
        weights: Sequence[int],
        values: Sequence[int],
    ) -> None:
        """Validate that every weight has exactly one matching value."""
        if len(weights) != len(values):
            raise ValueError("weights and values must have the same length")

    def validate_item_count_limit(self, weights: Sequence[int]) -> None:
        """Validate that item count stays within the configured safe limit."""
        if len(weights) > self.max_items:
            raise ValueError(f"item count cannot exceed {self.max_items}")


@dataclass(frozen=True, slots=True)
class TabulationKnapsackSolver:
    """Compute 0/1 knapsack maximum value with bottom-up tabulation.

    The solver is stateless apart from its injected validator dependency. That
    keeps the algorithm loosely coupled and easy to test with a validator test
    double.
    """

    validator: KnapsackInputValidator = field(default_factory=KnapsackInputValidator)

    def maximize_value(
        self,
        weights: Sequence[int],
        values: Sequence[int],
        capacity: int,
    ) -> int:
        """Return the maximum value that fits within ``capacity``.

        Args:
            weights: Positive integer item weights.
            values: Non-negative integer item values at matching indexes.
            capacity: Non-negative integer capacity of the knapsack.

        Returns:
            The maximum achievable value without exceeding capacity.

        Raises:
            TypeError: If inputs use invalid types.
            ValueError: If inputs use invalid values or mismatched lengths.
        """
        try:
            normalized_weights, normalized_values = self.validator.validate(
                weights,
                values,
                capacity,
            )
        except (TypeError, ValueError):
            LOGGER.exception(
                "Invalid 0/1 knapsack input: item_count=%s, capacity=%s",
                _safe_len(weights),
                capacity,
            )
            raise

        item_count = len(normalized_weights)
        LOGGER.debug(
            "Solving 0/1 knapsack: item_count=%s, capacity=%s",
            item_count,
            capacity,
        )

        if capacity == 0 or item_count == 0:
            LOGGER.debug("No capacity or items available; maximum value is 0")
            return 0

        max_value_table = [[0] * (capacity + 1) for _ in range(item_count + 1)]

        for item_index in range(1, item_count + 1):
            item_weight = normalized_weights[item_index - 1]
            item_value = normalized_values[item_index - 1]

            for current_capacity in range(1, capacity + 1):
                value_without_item = max_value_table[item_index - 1][current_capacity]

                if item_weight > current_capacity:
                    max_value_table[item_index][current_capacity] = value_without_item
                    continue

                remaining_capacity = current_capacity - item_weight
                value_with_item = (
                    item_value + max_value_table[item_index - 1][remaining_capacity]
                )
                best_value = max(value_with_item, value_without_item)
                max_value_table[item_index][current_capacity] = best_value

            LOGGER.debug(
                "Processed item: item_index=%s weight=%s value=%s "
                "best_value_at_capacity=%s",
                item_index,
                item_weight,
                item_value,
                max_value_table[item_index][capacity],
            )

        result = max_value_table[item_count][capacity]
        LOGGER.debug("0/1 knapsack maximum value: %s", result)
        return result


def zero_one_knapsack(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> int:
    """Return the maximum value for the 0/1 knapsack problem.

    This production-facing function keeps callers decoupled from the concrete
    solver class while using the default tabulation strategy.
    """
    solver: KnapsackSolver = TabulationKnapsackSolver()
    return solver.maximize_value(weights, values, capacity)


def knapsackdp(wt: Sequence[int], val: Sequence[int], cap: int) -> int:
    """Backward-compatible wrapper for the original exercise function name."""
    return zero_one_knapsack(wt, val, cap)


@dataclass(frozen=True, slots=True)
class ZeroOneKnapsackCalculator:
    """Class wrapper for callers that prefer an injectable calculator object."""

    solver: KnapsackSolver = field(default_factory=TabulationKnapsackSolver)

    def calculate(
        self,
        weights: Sequence[int],
        values: Sequence[int],
        capacity: int,
    ) -> int:
        """Return the best achievable value for the given knapsack input."""
        return self.solver.maximize_value(weights, values, capacity)


def run_knapsack_example() -> int:
    """Run the sample 0/1 knapsack workflow and print the result.

    Returns:
        Process exit code. ``0`` means success and ``1`` means invalid input.
    """
    try:
        print(zero_one_knapsack([2, 5, 4, 3], [3, 6, 5, 2], 6))
        return 0
    except (TypeError, ValueError) as error:
        LOGGER.error("Could not calculate 0/1 knapsack result: %s", error)
        return 1


def _safe_len(values: object) -> int | str:
    """Return ``len(values)`` when possible for safe diagnostic logging."""
    try:
        return len(values)  # type: ignore[arg-type]
    except TypeError:
        return "unknown"


__all__ = [
    "KnapsackInputValidator",
    "KnapsackSolver",
    "MAX_CAPACITY",
    "MAX_ITEMS",
    "TabulationKnapsackSolver",
    "ZeroOneKnapsackCalculator",
    "knapsackdp",
    "run_knapsack_example",
    "zero_one_knapsack",
]


if __name__ == "__main__":  # pragma: no cover
    configure_logging()
    raise SystemExit(run_knapsack_example())
