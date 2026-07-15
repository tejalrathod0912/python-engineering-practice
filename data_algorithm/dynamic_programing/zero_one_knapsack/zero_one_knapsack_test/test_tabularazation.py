"""Tests for the production-style 0/1 knapsack tabulation implementation."""

from __future__ import annotations

from collections.abc import Sequence
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
import unittest
from unittest.mock import patch

from config.logging_config import configure_logging, get_logger
from data_algorithm.dynamic_programing.zero_one_knapsack.zero_one_knapsack_code.tabularazation import (
    KnapsackInputValidator,
    MAX_CAPACITY,
    MAX_ITEMS,
    TabulationKnapsackSolver,
    ZeroOneKnapsackCalculator,
    knapsackdp,
    run_knapsack_example,
    zero_one_knapsack,
)


LOGGER_NAME = (
    "data_algorithm.dynamic_programing.zero_one_knapsack."
    "zero_one_knapsack_code.tabularazation"
)



class TestZeroOneKnapsack(unittest.TestCase):
    """Validate normal behavior, edge cases, logging, and defensive checks."""

    def test_zero_one_knapsack_returns_maximum_value(self) -> None:
        """The function should solve typical, edge, and larger inputs."""
        scenarios = [
            ([2, 5, 4, 3], [3, 6, 5, 2], 6, 8),
            ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9),
            ([5], [10], 4, 0),
            ([], [], 0, 0),
            ([], [], 10, 0),
            ([2, 3, 7, 8, 10], [5, 5, 20, 24, 30], 20, 59),
        ]

        for weights, values, capacity, expected in scenarios:
            with self.subTest(weights=weights, values=values, capacity=capacity):
                self.assertEqual(zero_one_knapsack(weights, values, capacity), expected)

    def test_zero_one_knapsack_accepts_immutable_sequences(self) -> None:
        """The implementation should depend on Sequence, not concrete lists."""
        self.assertEqual(zero_one_knapsack((2, 3, 4), (4, 5, 6), 5), 9)

    def test_validator_methods_return_normalized_inputs(self) -> None:
        """Each validator method should own one validation responsibility."""
        validator = KnapsackInputValidator()

        self.assertEqual(validator.validate_capacity(6), 6)
        self.assertEqual(validator.validate_weights([2, 5, 4]), (2, 5, 4))
        self.assertEqual(validator.validate_values([3, 6, 5]), (3, 6, 5))
        self.assertIsNone(validator.validate_item_counts_match([2, 5], [3, 6]))
        self.assertIsNone(validator.validate_item_count_limit([2, 5]))
        self.assertEqual(
            validator.validate([2, 5], [3, 6], 6),
            ((2, 5), (3, 6)),
        )

    def test_validator_enforces_configured_limits(self) -> None:
        """The validator should fail fast before allocating a huge DP table."""
        validator = KnapsackInputValidator(max_items=2, max_capacity=5)

        with self.assertRaisesRegex(ValueError, "capacity cannot exceed 5"):
            validator.validate_capacity(6)

        with self.assertRaisesRegex(ValueError, "item count cannot exceed 2"):
            validator.validate_item_count_limit([1, 2, 3])

    def test_knapsackdp_keeps_original_function_name_working(self) -> None:
        """The original exercise function name should remain available."""
        self.assertEqual(knapsackdp([2, 5, 4, 3], [3, 6, 5, 2], 6), 8)

    def test_solver_uses_injected_validator(self) -> None:
        """The solver should use the validator dependency passed to it."""

        class StubValidator(KnapsackInputValidator):
            """Validator test double that proves dependency injection works."""

            def validate(
                self,
                weights: Sequence[int],
                values: Sequence[int],
                capacity: int,
            ) -> tuple[tuple[int, ...], tuple[int, ...]]:
                self.validated_weights = weights
                self.validated_values = values
                self.validated_capacity = capacity
                return (1, 4), (2, 10)

        validator = StubValidator()
        solver = TabulationKnapsackSolver(validator=validator)

        self.assertEqual(solver.maximize_value([99], [100], 5), 12)
        self.assertEqual(validator.validated_weights, [99])
        self.assertEqual(validator.validated_values, [100])
        self.assertEqual(validator.validated_capacity, 5)

    def test_calculator_uses_injected_solver(self) -> None:
        """The calculator wrapper should depend on the solver abstraction."""

        class StubSolver:
            """Solver test double for the class wrapper."""

            def maximize_value(
                self,
                weights: Sequence[int],
                values: Sequence[int],
                capacity: int,
            ) -> int:
                self.weights = weights
                self.values = values
                self.capacity = capacity
                return 42

        solver = StubSolver()
        calculator = ZeroOneKnapsackCalculator(solver=solver)

        self.assertEqual(calculator.calculate([1], [2], 3), 42)
        self.assertEqual(solver.weights, [1])
        self.assertEqual(solver.values, [2])
        self.assertEqual(solver.capacity, 3)

    def test_zero_one_knapsack_rejects_invalid_inputs(self) -> None:
        """Invalid inputs should fail fast and log useful context."""
        scenarios: list[tuple[Any, Any, Any, type[Exception], str]] = [
            (object(), [1], 5, TypeError, "weights must be a sequence of integers"),
            ("123", [1, 2, 3], 5, TypeError, "weights must be a sequence of integers"),
            ([1, 2], [3], 5, ValueError, "weights and values must have the same length"),
            ([1, 0], [3, 4], 5, ValueError, "weights must contain only positive values"),
            ([1, -2], [3, 4], 5, ValueError, "weights must contain only positive values"),
            ([1, True], [3, 4], 5, TypeError, "weights must contain only integer values"),
            ([1, 2.5], [3, 4], 5, TypeError, "weights must contain only integer values"),
            ([1, 2], object(), 5, TypeError, "values must be a sequence of integers"),
            ([1, 2], [3, -4], 5, ValueError, "values must contain only non-negative values"),
            ([1, 2], [3, False], 5, TypeError, "values must contain only integer values"),
            ([1, 2], [3, 4.5], 5, TypeError, "values must contain only integer values"),
            ([1, 2], [3, 4], True, TypeError, "capacity must be an integer"),
            ([1, 2], [3, 4], 5.5, TypeError, "capacity must be an integer"),
            ([1, 2], [3, 4], -1, ValueError, "capacity cannot be negative"),
            ([1], [1], MAX_CAPACITY + 1, ValueError, "capacity cannot exceed"),
            (
                [1] * (MAX_ITEMS + 1),
                [1] * (MAX_ITEMS + 1),
                1,
                ValueError,
                "item count cannot exceed",
            ),
        ]

        for weights, values, capacity, expected_error, expected_message in scenarios:
            with self.subTest(weights=weights, values=values, capacity=capacity):
                with self.assertLogs(LOGGER_NAME, level="ERROR"):
                    with self.assertRaisesRegex(expected_error, expected_message):
                        zero_one_knapsack(weights, values, capacity)

    def test_solver_logs_invalid_input_before_reraising(self) -> None:
        """The solver should fail loud without hiding validation errors."""
        solver = TabulationKnapsackSolver()

        with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaisesRegex(ValueError, "capacity cannot be negative"):
                solver.maximize_value([1, 2, 3], [10, 20, 30], -1)

        self.assertIn(
            "Invalid 0/1 knapsack input: item_count=3, capacity=-1",
            "\n".join(captured_logs.output),
        )

    def test_solver_logs_unknown_item_count_when_len_is_unavailable(self) -> None:
        """Diagnostic logging should stay safe for non-sized invalid inputs."""
        solver = TabulationKnapsackSolver()

        with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaisesRegex(TypeError, "weights must be a sequence"):
                solver.maximize_value(object(), [1], 5)  # type: ignore[arg-type]

        self.assertIn(
            "Invalid 0/1 knapsack input: item_count=unknown, capacity=5",
            "\n".join(captured_logs.output),
        )

    def test_solver_writes_debug_logs_for_successful_calculation(self) -> None:
        """The solver should expose useful progress through debug logs."""
        solver = TabulationKnapsackSolver()

        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(solver.maximize_value([2, 3], [4, 5], 5), 9)

        log_output = "\n".join(captured_logs.output)
        self.assertIn("Solving 0/1 knapsack: item_count=2, capacity=5", log_output)
        self.assertIn(
            "Processed item: item_index=2 weight=3 value=5 best_value_at_capacity=9",
            log_output,
        )
        self.assertIn("0/1 knapsack maximum value: 9", log_output)
        self.assertNotIn("DP transition", log_output)

    def test_solver_logs_zero_result_for_empty_or_zero_capacity_input(self) -> None:
        """The solver should return immediately for no-capacity or no-item cases."""
        solver = TabulationKnapsackSolver()

        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(solver.maximize_value([1, 2], [3, 4], 0), 0)

        self.assertIn(
            "No capacity or items available; maximum value is 0",
            "\n".join(captured_logs.output),
        )

    def test_run_knapsack_example_prints_sample_answer(self) -> None:
        """The example runner should print the sample maximum value."""
        with patch("builtins.print") as mock_print:
            exit_code = run_knapsack_example()

        self.assertEqual(exit_code, 0)
        mock_print.assert_called_once_with(8)

    def test_run_knapsack_example_returns_error_code_for_invalid_input(self) -> None:
        """The example runner should convert validation errors into a safe exit code."""
        with patch(
            "data_algorithm.dynamic_programing.zero_one_knapsack."
            "zero_one_knapsack_code.tabularazation.zero_one_knapsack",
            side_effect=ValueError("capacity cannot be negative"),
        ):
            with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
                exit_code = run_knapsack_example()

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "Could not calculate 0/1 knapsack result: capacity cannot be negative",
            "\n".join(captured_logs.output),
        )

    # def test_module_prints_sample_output_when_run_as_script(self) -> None:
    #     """When executed directly, the module should print the sample answer.""" ̑
    #     module_path = (
    #         Path(__file__).resolve().parents[1]
    #         / "zero_one_knapsack_code"
    #         / "tabularazation.py"
    #     )
    #     completed_process = subprocess.run(
    #         [sys.executable, str(module_path)],
    #         capture_output=True,
    #         check=True,
    #         text=True,
    #     )

    #     self.assertEqual(completed_process.returncode, 0)
    #     self.assertEqual(completed_process.stdout.strip(), "8")


class TestLoggingConfig(unittest.TestCase):
    """Validate the reusable logging configuration helper."""

    def test_configure_logging_uses_environment_level_by_default(self) -> None:
        """When no level is passed, LOG_LEVEL should drive root logging."""
        with patch.dict(os.environ, {"LOG_LEVEL": "WARNING"}):
            configure_logging(force=True)

        self.assertEqual(logging.getLogger().level, logging.WARNING)

    def test_configure_logging_accepts_common_level_forms(self) -> None:
        """Logging levels should work as names, integers, and numeric strings."""
        scenarios: list[tuple[int | str, int]] = [
            ("debug", logging.DEBUG),
            ("10", logging.DEBUG),
            (logging.ERROR, logging.ERROR),
        ]

        for level, expected in scenarios:
            with self.subTest(level=level):
                configure_logging(level, force=True)
                self.assertEqual(logging.getLogger().level, expected)

    def test_configure_logging_rejects_invalid_levels(self) -> None:
        """Unsupported logging levels should fail fast with clear errors."""
        with self.assertRaisesRegex(ValueError, "Unknown logging level: noisy"):
            configure_logging("noisy", force=True)

        with self.assertRaisesRegex(TypeError, "level must be an integer, string, or None"):
            configure_logging(True, force=True)

        with self.assertRaisesRegex(TypeError, "level must be an integer, string, or None"):
            configure_logging(object(), force=True)  # type: ignore[arg-type]

    def test_get_logger_adds_one_null_handler(self) -> None:
        """Library loggers should be safe before application logging is configured."""
        logger = logging.getLogger("tests.knapsack.logging_config") #Create a logger with the name "tests.knapsack.logging_config".
        #This logger is used to test the behavior of the get_logger function. No handlers are attached to this logger yet, so it has no way to handle log messages.
        logger.handlers.clear() #This removes any handlers already attached to this logger.
        self.addCleanup(logger.handlers.clear) #After this test finishes, clear the handlers again."

        configured_logger = get_logger(logger.name)
        configured_again = get_logger(logger.name)

        null_handlers = [
            handler
            for handler in configured_logger.handlers
            if isinstance(handler, logging.NullHandler)
        ]

        self.assertIs(configured_logger, configured_again)
        self.assertEqual(len(null_handlers), 1)


if __name__ == "__main__":
    unittest.main()
