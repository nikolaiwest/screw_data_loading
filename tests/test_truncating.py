# test_truncating.py

import unittest
from typing import Any, Dict, List

from screw_data_loading.prep import apply_truncating


class TestTruncating(unittest.TestCase):
    def setUp(self):
        self.cycle_values = {
            "time": [0.0, 0.1, 0.2, 0.3, 0.4],
            "torque": [10, 20, 30, 40, 50],
        }
        self.target_length = 3

    def test_apply_truncating_post(self):
        """
        Test truncating applied at the end of the sequence.
        """
        truncated_values, initial_len, final_len = apply_truncating(
            self.cycle_values, self.target_length, "post"
        )

        # Check the lengths
        self.assertEqual(initial_len, 5)
        self.assertEqual(final_len, 3)

        # Check the values
        expected_time = [0.0, 0.1, 0.2]
        expected_torque = [10, 20, 30]
        self.assertEqual(truncated_values["time"], expected_time)
        self.assertEqual(truncated_values["torque"], expected_torque)

    def test_apply_truncating_pre(self):
        """
        Test truncating applied at the beginning of the sequence.
        """
        truncated_values, initial_len, final_len = apply_truncating(
            self.cycle_values, self.target_length, "pre"
        )

        # Check the lengths
        self.assertEqual(initial_len, 5)
        self.assertEqual(final_len, 3)

        # Check the values
        expected_time = [0.2, 0.3, 0.4]
        expected_torque = [30, 40, 50]
        self.assertEqual(truncated_values["time"], expected_time)
        self.assertEqual(truncated_values["torque"], expected_torque)

    def test_apply_truncating_longer_target_length(self):
        """
        Test truncating with a target length longer than the sequence.
        """
        longer_target_length = 10
        truncated_values, initial_len, final_len = apply_truncating(
            self.cycle_values, longer_target_length, "post"
        )

        # Check the lengths
        self.assertEqual(initial_len, 5)
        self.assertEqual(final_len, 5)

        # Check the values remain the same since target length is longer
        expected_time = [0.0, 0.1, 0.2, 0.3, 0.4]
        expected_torque = [10, 20, 30, 40, 50]
        self.assertEqual(truncated_values["time"], expected_time)
        self.assertEqual(truncated_values["torque"], expected_torque)


if __name__ == "__main__":
    unittest.main()
