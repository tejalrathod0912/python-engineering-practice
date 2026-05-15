"""Tests for the unbounded coin change implementation."""

import logging
import runpy
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from data_algorithm.dynamic_programing.unbounded_knapsack.unbounded_knapsack_code.max_subset_coin_change import (
    CoinChangeCombinationCounter,
    CoinChangeInputValidator,
    CoinChangeMaximumNumberWays,
    count_coin_change_combinations,
    max_subset_sum,
    run_coin_change_example,
)


LOGGER = logging.getLogger(__name__)
COIN_CHANGE_LOGGER_NAME = (
    "data_algorithm.dynamic_programing.unbounded_knapsack."
    "unbounded_knapsack_code.max_subset_coin_change"
)


class TestMaxSubsetCoinChange(unittest.TestCase):
    """Validate coin change behavior for normal and edge-case inputs."""

    def test_coin_change_combination_counter_returns_number_of_combinations(self) -> None:
        """The production class should count unique combinations."""
        counter = CoinChangeCombinationCounter()

        self.assertEqual(counter.count([1, 2, 3], 5), 5)

    def test_coin_change_combination_counter_uses_injected_validator(self) -> None:
        """The counter should accept its validator dependency from outside."""

        class StubValidator(CoinChangeInputValidator):
            """Validator test double that proves dependency injection works."""

            def validate(self, coins: list[int], target_sum: int) -> tuple[int, ...]:
                self.validated_coins = coins
                self.validated_target_sum = target_sum
                return (1, 2)

        validator = StubValidator()
        counter = CoinChangeCombinationCounter(validator=validator)

        self.assertEqual(counter.count([99], 4), 3)
        self.assertEqual(validator.validated_coins, [99])
        self.assertEqual(validator.validated_target_sum, 4)

    def test_count_coin_change_combinations_returns_number_of_combinations(self) -> None:
        """The production-facing function should count unique combinations."""
        self.assertEqual(count_coin_change_combinations([1, 2, 3], 5), 5)

    def test_count_coin_change_combinations_accepts_immutable_sequences(self) -> None:
        """The function should depend on sequence behavior, not a concrete list."""
        self.assertEqual(count_coin_change_combinations((2, 3, 5), 10), 4)

    def test_max_subset_sum_returns_number_of_combinations(self) -> None:
        """The legacy function name should keep working for existing callers."""
        coins = [1, 2, 3]
        target_sum = 5
        LOGGER.debug("Testing coins %s with target sum %s", coins, target_sum)

        self.assertEqual(max_subset_sum(coins, target_sum), 5)

    def test_max_subset_sum_can_reuse_same_coin(self) -> None:
        """The function should allow every coin denomination to be reused."""
        self.assertEqual(max_subset_sum([2, 3, 5], 10), 4)

    def test_max_subset_sum_with_zero_target(self) -> None:
        """The function should count the empty combination for a zero target."""
        self.assertEqual(max_subset_sum([1, 2, 3], 0), 1)

    def test_max_subset_sum_with_no_coins(self) -> None:
        """The function should return 0 when no coins can create the target."""
        self.assertEqual(max_subset_sum([], 5), 0)

    def test_max_subset_sum_rejects_negative_target(self) -> None:
        """The legacy function should keep its existing validation message."""
        with self.assertRaisesRegex(ValueError, "coins_sum cannot be negative"):
            max_subset_sum([1, 2, 3], -1)

    def test_count_coin_change_combinations_rejects_negative_target(self) -> None:
        """The production-facing function should reject invalid target sums."""
        with self.assertRaisesRegex(ValueError, "target_sum cannot be negative"):
            count_coin_change_combinations([1, 2, 3], -1)

    def test_counter_logs_invalid_input_before_reraising(self) -> None:
        """The production class should fail loud without hiding validation errors."""
        counter = CoinChangeCombinationCounter()

        with self.assertLogs(COIN_CHANGE_LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaisesRegex(ValueError, "target_sum cannot be negative"):
                counter.count([1, 2, 3], -1)

        self.assertIn(
            "Invalid coin-change input: coin_count=3, target_sum=-1",
            "\n".join(captured_logs.output),
        )

    def test_run_coin_change_example_exits_safely_for_invalid_input(self) -> None:
        """The script helper should convert validation errors into a safe exit."""
        with self.assertLogs(COIN_CHANGE_LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaises(SystemExit) as exit_context:
                run_coin_change_example([1, 2, 3], -1)

        self.assertEqual(exit_context.exception.code, 1)
        self.assertIn(
            "Could not count coin combinations: target_sum cannot be negative",
            "\n".join(captured_logs.output),
        )

    def test_max_subset_sum_rejects_non_positive_coins(self) -> None:
        """The function should reject zero and negative coin denominations."""
        with self.assertRaisesRegex(ValueError, "coins must contain only positive values"):
            max_subset_sum([1, 0, 3], 5)

        with self.assertRaisesRegex(ValueError, "coins must contain only positive values"):
            max_subset_sum([1, -2, 3], 5)

    def test_coin_change_class_wrapper(self) -> None:
        """The wrapper class should provide the same behavior as the function."""
        coin_change = CoinChangeMaximumNumberWays()

        self.assertEqual(coin_change.max_subset_fun([1, 2, 3], 5), 5)

    def test_max_subset_sum_writes_debug_logs(self) -> None:
        """The function should log useful debug details while filling the table."""
        with self.assertLogs(COIN_CHANGE_LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(max_subset_sum([1, 2, 3], 5), 5)

        log_output = "\n".join(captured_logs.output)

        self.assertIn(
            "Counting coin combinations for coins=[1, 2, 3], target_sum=5",
            log_output,
        )
        self.assertIn("coin_value=3 current_sum=5", log_output)
        self.assertIn("Number of combinations: 5", log_output)

    def test_module_prints_sample_output_when_run_as_script(self) -> None:
        """When executed directly, the module should print the sample answer."""
        module_path = (
            Path(__file__).resolve().parents[1]
            / "unbounded_knapsack_code"
            / "max_subset_coin_change.py"
        )
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            runpy.run_path(str(module_path), run_name="__main__")

        self.assertEqual(captured_output.getvalue().strip(), "5")


if __name__ == "__main__":
    unittest.main()
