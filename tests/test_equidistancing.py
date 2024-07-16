# test_equidistancing.py

import unittest

import numpy as np

from screw_data_loading.prep import apply_equidistancing


class TestEquidistancing(unittest.TestCase):
    def setUp(self):
        """Set up initial conditions for the tests."""
        self.cycle_values = {"time": [0.0, 0.1, 0.2, 0.3], "torque": [10, 20, 30, 40]}
        self.interval_length = 0.1

    def test_apply_equidistancing(self):
        """
        Test the apply_equidistancing function with a specified interval length.

        This test checks that the function correctly converts the input data to equidistant intervals
        and verifies the initial and final lengths of the data.
        """
        equidistant_values, initial_len, final_len = apply_equidistancing(
            self.cycle_values, self.interval_length
        )

        # Check the initial and final lengths
        self.assertEqual(initial_len, 4)
        self.assertEqual(final_len, 4)

        # Check the equidistant values
        expected_time = np.arange(0.0, 0.4, self.interval_length)
        np.testing.assert_almost_equal(equidistant_values["time"], expected_time)
        np.testing.assert_almost_equal(equidistant_values["torque"], [10, 20, 30, 40])

    def test_apply_equidistancing_default_interval(self):
        """
        Test the apply_equidistancing function with the default interval length.

        This test checks that the function correctly converts the input data to equidistant intervals
        using the default interval length of 0.0012 and verifies the initial and final lengths of the data.
        """
        equidistant_values, initial_len, final_len = apply_equidistancing(
            self.cycle_values
        )

        # Check the initial and final lengths
        self.assertEqual(initial_len, 4)
        expected_time = np.arange(0.0, 0.3 + 0.0012, 0.0012)
        expected_final_length = len(expected_time)
        self.assertEqual(final_len, expected_final_length)

        # Check the equidistant values
        expected_torque = np.interp(
            expected_time, self.cycle_values["time"], self.cycle_values["torque"]
        )
        np.testing.assert_almost_equal(equidistant_values["time"], expected_time)
        np.testing.assert_almost_equal(equidistant_values["torque"], expected_torque)


if __name__ == "__main__":
    unittest.main()
