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

'''unique identifier for logging that tells where the log messages are coming from in the codebase'''
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
        """ software design test (dependency injection + mocking of validate method )
        The counter should accept its validator dependency from outside."""

        """1) You create a fake validator that records the input it receives and returns a fixed valid output. 
        Then you inject this fake into the counter and call the count method. 
        Finally, you assert that the count method returns the expected number of combinations based on the fake's output, and that the fake validator was called with the correct input parameters.
        This proves that the counter is using the injected validator to validate its input."""
        class StubValidator(CoinChangeInputValidator):
            """Validator test double that proves dependency injection works."""

            '''2. You override validate()'''
            def validate(self, coins: list[int], target_sum: int) -> tuple[int, ...]:
                '''(A) It records what was passed in'''
                self.validated_coins = coins
                self.validated_target_sum = target_sum
                '''(B) It ignores real logic and returns fake data
                So instead of real validation, it just returns dummy coins.'''
                return (1, 2)
        '''3. You inject this fake validator. 
        This is called dependency injection.'''
        validator = StubValidator()
        counter = CoinChangeCombinationCounter(validator=validator)

        '''4. You call the function'''
        self.assertEqual(counter.count([99], 4), 3) #This ensures algorithm still works even with fake validator.
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
        '''In unittest.assertRaisesRegex, with is not mainly about closing resources.
        It is used for a different kind of purpose: exception capturing scope.
        In this case, with is used to define a controlled zone where exceptions are expected and verified, not for resource cleanup.'''
        with self.assertRaisesRegex(ValueError, "coins_sum cannot be negative"):
            max_subset_sum([1, 2, 3], -1)

    def test_count_coin_change_combinations_rejects_negative_target(self) -> None:
        """The production-facing function should reject invalid target sums."""
        with self.assertRaisesRegex(ValueError, "target_sum cannot be negative"):
            count_coin_change_combinations([1, 2, 3], -1)

    def test_counter_logs_invalid_input_before_reraising(self) -> None:
        """The production class should fail loud without hiding validation errors."""
        counter = CoinChangeCombinationCounter()

        '''Watch and save all ERROR logs produced inside this block.
        we store them in captured_logs
        “Capture all logs from this logger with level ERROR or higher during this block'''
        with self.assertLogs(COIN_CHANGE_LOGGER_NAME, level="ERROR") as captured_logs:
            '''Run this code and expect a ValueError. Also verify that the error message matches the given regex pattern.'''
            with self.assertRaisesRegex(ValueError, "target_sum cannot be negative"):
                counter.count([1, 2, 3], -1)
        
        '''Check if this message exists inside captured logs.
        This checks:Was this exact log message written during execution?
        '''
        '''captured_logs.output → list of log messages
        "\n".join(...) → converts them into a single string
        assertIn → checks if expected message exists inside it'''
        self.assertIn(
            "Invalid coin-change input: coin_count=3, target_sum=-1",
            "\n".join(captured_logs.output),
        )

        '''assertLogs captures all ERROR logs generated during execution of the block.
        assertRaisesRegex ensures the function raises a ValueError and the message matches the expected pattern.
        Finally, assertIn verifies that the expected error log message was actually recorded before the exception was raised.'''

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

    def test_run_coin_change_example_returns_number_of_combinations(self) -> None:
        """The script helper should return the calculated combination count."""
        self.assertEqual(run_coin_change_example([1, 2, 3], 5), 5)

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
        '''Find the actual Python file on disk'''
        module_path = (
            Path(__file__).resolve().parents[1]
            / "unbounded_knapsack_code"
            / "max_subset_coin_change.py"
        )
        '''Create a fake output collector ,Instead of printing to screen, we capture output in memory'''
        captured_output = StringIO()  
        '''#StringIO() is a Python tool that lets you treat a string like a file in memory.write into it
            read from it but nothing is saved to disk'''

        '''3. Redirect print output to our collector while running the module as a script.
        “Everything printed inside this block should go into captured_output instead of console”'''
        with redirect_stdout(captured_output):
            #Run the file like a script, which will execute the example function and print the result.
            runpy.run_path(str(module_path), run_name="__main__")
            '''Compare output:captured_output.getvalue() → gets printed text'''
        self.assertEqual(captured_output.getvalue().strip(), "5")


if __name__ == "__main__":
    unittest.main()
