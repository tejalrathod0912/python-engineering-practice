"""Longest Common Subsequence using pure recursion.

Problem:
    Given two strings, find the length of the longest subsequence that appears
    in both strings in the same relative order. The characters do not need to be
    continuous.

Approach:
    This module uses a pure recursive strategy. If the last characters match,
    they are part of the answer and the recursion moves to both previous
    indexes. If they do not match, the recursion tries both possibilities:
    skipping one character from the first string or one from the second string.

Complexity:
    Time complexity is O(2^(m + n)), where m and n are the lengths of the two
    strings. Space complexity is O(m + n) for the recursion call stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Protocol


LOGGER = logging.getLogger(__name__)


class LongestCommonSubsequenceSolver(Protocol):
    """Strategy interface for Longest Common Subsequence algorithms."""

    def longest_common_subsequence(self, first_text: str, second_text: str) -> int:
        """Return the length of the longest common subsequence."""


class LCSInputValidator:
    """Validate and normalize input for LCS solvers."""

    def validate(self, first_text: str, second_text: str) -> tuple[str, str]:
        """Return validated text values.

        Args:
            first_text: First input string.
            second_text: Second input string.

        Raises:
            TypeError: If either input is not a string.
        """
        if not isinstance(first_text, str):
            raise TypeError("first_text must be a string")

        if not isinstance(second_text, str):
            raise TypeError("second_text must be a string")

        return first_text, second_text


@dataclass(frozen=True, slots=True)
class RecursiveLongestCommonSubsequenceSolver:
    """Compute LCS length with a pure recursive strategy.

    The class is stateless apart from its injected validator dependency, making
    it easy to test and swap with another ``LongestCommonSubsequenceSolver``
    implementation later.
    """

    validator: LCSInputValidator = field(default_factory=LCSInputValidator)

    def longest_common_subsequence(self, first_text: str, second_text: str) -> int:
        """Return the length of the longest common subsequence.

        Args:
            first_text: First input string.
            second_text: Second input string.

        Returns:
            Length of the longest common subsequence.

        Raises:
            TypeError: If either input is not a string.
        """
        try:
            normalized_first_text, normalized_second_text = self.validator.validate(
                first_text,
                second_text,
            )
        except TypeError:
            LOGGER.exception(
                "Invalid LCS input: first_type=%s, second_type=%s",
                type(first_text).__name__,
                type(second_text).__name__,
            )
            raise

        LOGGER.debug(
            "Calculating LCS for first_text_length=%s, second_text_length=%s",
            len(normalized_first_text),
            len(normalized_second_text),
        )

        def solve(first_index: int, second_index: int) -> int:
            """Solve LCS for prefixes ending at the given indexes."""
            if first_index == 0 or second_index == 0:
                return 0

            if (
                normalized_first_text[first_index - 1]
                == normalized_second_text[second_index - 1]
            ):
                LOGGER.debug(
                    "Matched character=%s at first_index=%s second_index=%s",
                    normalized_first_text[first_index - 1],
                    first_index - 1,
                    second_index - 1,
                )
                return 1 + solve(first_index - 1, second_index - 1)

            return max(
                solve(first_index - 1, second_index),
                solve(first_index, second_index - 1),
            )

        result = solve(len(normalized_first_text), len(normalized_second_text))
        LOGGER.debug("LCS length calculated: %s", result)
        return result


def longest_common_subsequence(first_text: str, second_text: str) -> int:
    """Return the LCS length using the default pure recursive strategy.

    This convenience function keeps callers decoupled from the concrete solver
    class while preserving a simple function-style API.
    """
    solver: LongestCommonSubsequenceSolver = RecursiveLongestCommonSubsequenceSolver()

    return solver.longest_common_subsequence(first_text, second_text)


def run_lcs_example() -> int:
    """Run a small example and print the LCS length.

    Returns:
        Process exit code. ``0`` means success and ``1`` means invalid input.
    """
    try:
        print(longest_common_subsequence("abcdgh", "abedfhr"))
        return 0
    except TypeError as error:
        LOGGER.error("Could not calculate LCS length: %s", error)
        return 1


@dataclass(frozen=True, slots=True)
class LongestCommonSequence:
    """Backward-compatible class wrapper for the original exercise name."""

    solver: RecursiveLongestCommonSubsequenceSolver = field(
        default_factory=RecursiveLongestCommonSubsequenceSolver
    )

    def longest_comman_subsequence(
        self,
        first_text: str,
        second_text: str,
        first_length: int,
        second_length: int,
    ) -> int:
        """Return LCS length for the provided text prefixes.

        The method name keeps the original exercise API, including the spelling,
        so existing callers continue to work.
        """
        return self.solver.longest_common_subsequence(
            first_text[:first_length],
            second_text[:second_length],
        )


if __name__ == "__main__":
    # Return the example runner's status code to the operating system.
    raise SystemExit(run_lcs_example())
