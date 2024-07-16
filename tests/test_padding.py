# test_padding.py

import unittest

import numpy as np

from screw_data_loading.prep import apply_padding


class TestPadding(unittest.TestCase):
    def setUp(self):
        self.cycle_values = {"time": [0.0, 0.0012, 0.0024], "torque": [10, 20, 30]}
        self.target_length = 5
        self.padding_value = 0

    def test_apply_padding_pre(self):
        """
        Test padding applied at the beginning of the sequence.
        """
        padded_values, initial_len, final_len = apply_padding(
            self.cycle_values, self.padding_value, "pre", self.target_length
        )

        # Check the lengths
        self.assertEqual(initial_len, 3)
        self.assertEqual(final_len, 5)

        # Check the values
        expected_time = np.linspace(
            0, (self.target_length - 1) * 0.0012, self.target_length
        )
        np.testing.assert_almost_equal(padded_values["time"], expected_time)
        np.testing.assert_almost_equal(padded_values["torque"], [0, 0, 10, 20, 30])

    def test_apply_padding_post(self):
        """
        Test padding applied at the end of the sequence.
        """
        padded_values, initial_len, final_len = apply_padding(
            self.cycle_values, self.padding_value, "post", self.target_length
        )

        # Check the lengths
        self.assertEqual(initial_len, 3)
        self.assertEqual(final_len, 5)

        # Check the values
        expected_time = np.linspace(
            0, (self.target_length - 1) * 0.0012, self.target_length
        )
        np.testing.assert_almost_equal(padded_values["time"], expected_time)
        np.testing.assert_almost_equal(padded_values["torque"], [10, 20, 30, 0, 0])


if __name__ == "__main__":
    unittest.main()
