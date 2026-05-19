"""Tests for the minimum coin-change dynamic programming implementation."""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy
from typing import Any
import unittest
from unittest.mock import patch

from data_algorithm.dynamic_programing.unbounded_knapsack.unbounded_knapsack_code.min_coins_require_target_sum import (
    CoinChangeInputValidator,
    DynamicProgrammingCoinChangeSolver,
    MinNumberOfCoinsForTargetSum,
    min_coin_change,
    run_min_coin_change_example,
)


LOGGER_NAME = (
    "data_algorithm.dynamic_programing.unbounded_knapsack."
    "unbounded_knapsack_code.min_coins_require_target_sum"
)


class TestMinCoinChange(unittest.TestCase):
    """Validate minimum coin-change behavior and defensive input handling."""

    def test_min_coin_change_returns_minimum_coin_count(self) -> None:
        """The function should handle normal, edge, and large target inputs."""
        scenarios = [
            ([1, 2, 3, 5], 5, 1),
            ([1, 2, 3], 5, 2),
            ([2, 4], 6, 2),
            ([5], 15, 3),
            ([5], 14, -1),
            ([], 0, 0),
            ([], 7, -1),
            ([5, 10, 25], 1_000, 40),
        ]

        for coins, target_sum, expected in scenarios:
            with self.subTest(coins=coins, target_sum=target_sum):
                self.assertEqual(min_coin_change(coins, target_sum), expected)

    def test_min_coin_change_accepts_immutable_sequences(self) -> None:
        """The implementation should depend on Sequence, not a concrete list type."""
        self.assertEqual(min_coin_change((2, 3, 5), 11), 3)

    def test_min_coin_change_rejects_invalid_inputs(self) -> None:
        """Invalid inputs should fail fast with clear messages."""
        scenarios: list[tuple[Any, Any, type[Exception], str]] = [
            (object(), 5, TypeError, "coins must be a sequence of positive integers"),
            ([1, 2, 3], -1, ValueError, "target_sum cannot be negative"),
            ([1, 0, 3], 5, ValueError, "coins must contain only positive values"),
            ([1, -2, 3], 5, ValueError, "coins must contain only positive values"),
            ([1, 2.5, 3], 5, TypeError, "coins must contain only integer values"),
            ([True, 2, 3], 5, TypeError, "coins must contain only integer values"),
            ([1, 2, 3], 5.5, TypeError, "target_sum must be an integer"),
        ]

        for coins, target_sum, expected_error, expected_message in scenarios:
            with self.subTest(coins=coins, target_sum=target_sum):
                with self.assertLogs(LOGGER_NAME, level="ERROR"):
                    with self.assertRaisesRegex(expected_error, expected_message):
                        min_coin_change(coins, target_sum)

    def test_solver_uses_injected_validator(self) -> None:
        """The solver should depend on the validator abstraction passed to it."""

        class StubValidator(CoinChangeInputValidator):
            """Test double that proves dependency injection is used."""

            def __init__(self) -> None:
                self.validated_coins: Sequence[int] | None = None
                self.validated_target_sum: int | None = None

            def validate(self, coins: Sequence[int], target_sum: int) -> tuple[int, ...]:
                self.validated_coins = coins
                self.validated_target_sum = target_sum
                return (1, 4)

        validator = StubValidator()
        solver = DynamicProgrammingCoinChangeSolver(validator=validator)

        self.assertEqual(solver.minimum_coins([99], 8), 2)
        self.assertEqual(validator.validated_coins, [99])
        self.assertEqual(validator.validated_target_sum, 8)

    def test_solver_logs_invalid_input_before_reraising(self) -> None:
        """The solver should fail loud while still preserving the original exception."""
        solver = DynamicProgrammingCoinChangeSolver()

        with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaisesRegex(ValueError, "target_sum cannot be negative"):
                solver.minimum_coins([1, 2, 3], -1)

        self.assertIn(
            "Invalid minimum coin-change input: coin_count=3, target_sum=-1",
            "\n".join(captured_logs.output),
        )

    def test_solver_writes_debug_logs_for_successful_calculation(self) -> None:
        """The solver should expose useful internal progress through debug logs."""
        solver = DynamicProgrammingCoinChangeSolver()

        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(solver.minimum_coins([1, 3, 4], 6), 2)

        log_output = "\n".join(captured_logs.output)
        self.assertIn(
            "Calculating minimum coins for coins=[1, 3, 4], target_sum=6",
            log_output,
        )
        self.assertIn("Updated minimum coin count: coin=3 amount=6 count=2", log_output)
        self.assertIn("Minimum coins required: 2", log_output)

    def test_legacy_class_wrapper_returns_minimum_coin_count(self) -> None:
        """The original exercise class name should remain usable."""
        calculator = MinNumberOfCoinsForTargetSum()

        self.assertEqual(calculator.get_min_number_of_coins([1, 2, 3], 5), 2)

    def test_run_min_coin_change_example_prints_sample_answer(self) -> None:
        """The example runner should print the sample minimum coin count."""
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            exit_code = run_min_coin_change_example()

        self.assertEqual(exit_code, 0)
        self.assertEqual(captured_output.getvalue().strip(), "1")

    def test_run_min_coin_change_example_returns_error_code_for_invalid_input(self) -> None:
        """The example runner should convert validation errors into a safe exit code."""
        with patch(
            "data_algorithm.dynamic_programing.unbounded_knapsack."
            "unbounded_knapsack_code.min_coins_require_target_sum.min_coin_change",
            side_effect=ValueError("target_sum cannot be negative"),
        ):
            with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
                exit_code = run_min_coin_change_example()

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "Could not calculate minimum coins: target_sum cannot be negative",
            "\n".join(captured_logs.output),
        )

    def test_module_prints_sample_output_when_run_as_script(self) -> None:
        """When executed directly, the module should print the sample answer."""
        module_path = (
            Path(__file__).resolve().parents[1]
            / "unbounded_knapsack_code"
            / "min_coins_require_target_sum.py"
        )
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            with self.assertRaises(SystemExit) as exit_context:
                runpy.run_path(str(module_path), run_name="__main__")

        self.assertEqual(exit_context.exception.code, 0)
        self.assertEqual(captured_output.getvalue().strip(), "1")


if __name__ == "__main__":
    unittest.main()
