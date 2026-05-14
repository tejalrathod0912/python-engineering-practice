"""Tests for the unbounded knapsack rod cutting implementation."""

import logging  # Used to verify that debug logs are emitted by the implementation.
import runpy  # Used to execute the module's script block inside this test process.
import unittest  # The unittest framework is used to define and run the test cases.
from contextlib import redirect_stdout  # Used to capture output printed by the script block.
from io import StringIO  # Used as an in-memory stream for captured script output.
from pathlib import Path  # Used to construct the path to the module being tested.


from data_algorithm.dynamic_programing.unbounded_knapsack.unbounded_knapsack_code.rod_cutting import (
    RodCutting,
    rod_cutting,
)


LOGGER = logging.getLogger(__name__)
ROD_CUTTING_LOGGER_NAME = (
    "data_algorithm.dynamic_programing.unbounded_knapsack."
    "unbounded_knapsack_code.rod_cutting"
)


class TestRodCutting(unittest.TestCase):
    """Validate rod cutting behavior for normal and edge-case inputs."""

    def test_rod_cutting_returns_best_revenue(self) -> None:
        """The function should return the maximum revenue for a normal rod."""
        rod_length = 8
        rod_length_prices = [2, 4, 10, 4, 9]
        LOGGER.debug("Testing rod length %s with prices %s", rod_length, rod_length_prices)

        self.assertEqual(rod_cutting(rod_length, rod_length_prices), 24)

    def test_rod_cutting_can_reuse_same_piece_length(self) -> None:
        """The function should allow the same cut length to be used repeatedly."""
        self.assertEqual(rod_cutting(4, [1, 5, 8]), 10)

    def test_rod_cutting_with_zero_length_rod(self) -> None:
        """The function should return 0 when the rod length is 0."""
        self.assertEqual(rod_cutting(0, [2, 4, 10]), 0)

    def test_rod_cutting_with_no_prices(self) -> None:
        """The function should return 0 when no piece prices are available."""
        self.assertEqual(rod_cutting(5, []), 0)

    def test_rod_cutting_with_length_greater_than_price_list(self) -> None:
        """The function should reuse available piece sizes for longer rods."""
        self.assertEqual(rod_cutting(7, [2, 5, 7]), 17)

    def test_rod_cutting_rejects_negative_length(self) -> None:
        """The function should reject an invalid negative rod length."""
        with self.assertRaisesRegex(ValueError, "length cannot be negative"):
            rod_cutting(-1, [2, 4, 10])

    def test_rod_cutting_rejects_negative_prices(self) -> None:
        """The function should reject negative piece prices."""
        with self.assertRaisesRegex(ValueError, "prices cannot contain negative values"):
            rod_cutting(5, [2, -4, 10])

    def test_rod_cutting_class_wrapper(self) -> None:
        """The RodCutting class should provide the same behavior as the function."""
        rod_cutter = RodCutting()
        rod_length = 8
        rod_length_prices = [2, 4, 10, 4, 9]

        self.assertEqual(rod_cutter.rod_cutting_func(rod_length, rod_length_prices), 24)

    def test_rod_cutting_writes_debug_logs(self) -> None:
        """The function should log useful debug details while filling the table."""
        with self.assertLogs(ROD_CUTTING_LOGGER_NAME, level="DEBUG") as captured_logs:
            self.assertEqual(rod_cutting(4, [1, 5, 8]), 10)

        log_output = "\n".join(captured_logs.output)

        self.assertIn("Calculating best revenue for length=4, prices=[1, 5, 8]", log_output)
        self.assertIn("piece_length=2 current_length=4", log_output)
        self.assertIn("Best revenue: 10", log_output)

    def test_module_prints_sample_output_when_run_as_script(self) -> None:
        """When executed directly, the module should print the sample answer."""
        module_path = (
            Path(__file__).resolve().parents[1]
            / "unbounded_knapsack_code"
            / "rod_cutting.py"
        )
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            runpy.run_path(str(module_path), run_name="__main__")

        self.assertEqual(captured_output.getvalue().strip(), "24")

if __name__ == "__main__":
    unittest.main()
