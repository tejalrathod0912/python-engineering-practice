"""Tests for the pure recursive Longest Common Subsequence implementation."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from data_algorithm.dynamic_programing.string_dynamic_program.string_dynamic_code import (
    recursive_str_longest_com_seq_code as lcs_module,
)
from data_algorithm.dynamic_programing.string_dynamic_program.string_dynamic_code.recursive_str_longest_com_seq_code import (
    LCSInputValidator,
    LongestCommonSequence,
    RecursiveLongestCommonSubsequenceSolver,
    longest_common_subsequence,
    run_lcs_example,
)


LOGGER_NAME = (
    "data_algorithm.dynamic_programing.string_dynamic_program."
    "string_dynamic_code.recursive_str_longest_com_seq_code"
)


class TestRecursiveLongestCommonSubsequence(unittest.TestCase):
    """Validate recursive LCS behavior and defensive input handling."""

    def test_longest_common_subsequence_returns_expected_lengths(self) -> None:
        """The function should solve normal and edge-case LCS scenarios."""
        scenarios = [
            ("abcdgh", "abedfhr", 4),
            ("abcde", "ace", 3),
            ("abc", "abc", 3),
            ("abc", "def", 0),
            ("", "abc", 0),
            ("abc", "", 0),
            ("", "", 0),
        ]

        for first_text, second_text, expected in scenarios:
            with self.subTest(first_text=first_text, second_text=second_text):
                self.assertEqual(
                    longest_common_subsequence(first_text, second_text),
                    expected,
                )

    def test_validator_returns_validated_text_values(self) -> None:
        """Valid strings should be returned unchanged."""
        validator = LCSInputValidator()

        self.assertEqual(validator.validate("abc", "ace"), ("abc", "ace"))

    def test_validator_rejects_invalid_first_text(self) -> None:
        """The validator should fail fast when the first input is invalid."""
        validator = LCSInputValidator()

        with self.assertRaisesRegex(TypeError, "first_text must be a string"):
            validator.validate(123, "abc")  # type: ignore[arg-type]

    def test_validator_rejects_invalid_second_text(self) -> None:
        """The validator should fail fast when the second input is invalid."""
        validator = LCSInputValidator()

        with self.assertRaisesRegex(TypeError, "second_text must be a string"):
            validator.validate("abc", 123)  # type: ignore[arg-type]

    def test_solver_uses_injected_validator(self) -> None:
        """The solver should depend on the validator dependency passed to it."""

        class StubValidator(LCSInputValidator):
            """Test double that proves dependency injection is used."""

            def __init__(self) -> None:
                self.received_first_text: str | None = None
                self.received_second_text: str | None = None

            def validate(self, first_text: str, second_text: str) -> tuple[str, str]:
                self.received_first_text = first_text
                self.received_second_text = second_text
                return "abc", "abc"

        validator = StubValidator()
        solver = RecursiveLongestCommonSubsequenceSolver(validator=validator)

        self.assertEqual(solver.longest_common_subsequence("ignored", "values"), 3)
        self.assertEqual(validator.received_first_text, "ignored")
        self.assertEqual(validator.received_second_text, "values")

    def test_solver_logs_invalid_input_before_reraising(self) -> None:
        """The solver should fail loud while preserving the original exception."""
        solver = RecursiveLongestCommonSubsequenceSolver()

        with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
            with self.assertRaisesRegex(TypeError, "first_text must be a string"):
                solver.longest_common_subsequence(123, "abc")  # type: ignore[arg-type]

        self.assertIn(
            "Invalid LCS input: first_type=int, second_type=str",
            "\n".join(captured_logs.output),
        )

    def test_solver_writes_debug_logs_for_successful_calculation(self) -> None:
        """The solver should expose useful progress through debug logs."""
        solver = RecursiveLongestCommonSubsequenceSolver()

        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(solver.longest_common_subsequence("abc", "abc"), 3)

        log_output = "\n".join(captured_logs.output)
        self.assertIn(
            "Calculating LCS for first_text_length=3, second_text_length=3",
            log_output,
        )
        self.assertIn("Matched character=c at first_index=2 second_index=2", log_output)
        self.assertIn("LCS length calculated: 3", log_output)

    def test_legacy_class_wrapper_returns_lcs_length(self) -> None:
        """The original exercise class name should remain usable."""
        calculator = LongestCommonSequence()

        self.assertEqual(
            calculator.longest_comman_subsequence("abcdgh", "abedfhr", 6, 7),
            4,
        )

    def test_legacy_class_wrapper_uses_requested_prefix_lengths(self) -> None:
        """The wrapper should calculate only against the requested prefixes."""
        calculator = LongestCommonSequence()

        self.assertEqual(
            calculator.longest_comman_subsequence("abczzz", "abczzz", 3, 3),
            3,
        )

    def test_run_lcs_example_prints_sample_answer(self) -> None:
        """The example runner should print the sample LCS length."""
        with patch("builtins.print") as mock_print:
            exit_code = run_lcs_example()

        self.assertEqual(exit_code, 0)
        mock_print.assert_called_once_with(4)

    def test_run_lcs_example_returns_error_code_for_invalid_input(self) -> None:
        """The example runner should convert validation errors into an exit code."""
        with patch.object(
            lcs_module,
            "longest_common_subsequence",
            side_effect=TypeError("first_text must be a string"),
        ):
            with self.assertLogs(LOGGER_NAME, level="ERROR") as captured_logs:
                exit_code = run_lcs_example()

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "Could not calculate LCS length: first_text must be a string",
            "\n".join(captured_logs.output),
        )

    def test_module_prints_sample_output_when_run_as_script(self) -> None:
        """When executed directly, the module should print the sample result."""
        module_path = (
            Path(__file__).resolve().parents[1]
            / "string_dynamic_code"
            / "recursive_str_longest_com_seq_code.py"
        )
        completed_process = subprocess.run(
            [sys.executable, str(module_path)],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual(completed_process.returncode, 0)
        self.assertEqual(completed_process.stdout.strip(), "4")


if __name__ == "__main__":
    unittest.main()
