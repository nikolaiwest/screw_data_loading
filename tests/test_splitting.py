#

import unittest
from typing import List, Any

from screw_data_loading.prep import apply_split


class TestSplitting(unittest.TestCase):
    def setUp(self):
        self.data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [10, 20, 30, 40, 50]]
        self.split_ratio = 0.6
        self.split_seed = 42

    def test_apply_split(self):
        """
        Test the apply_split function with a defined split ratio and seed.
        """
        x_train, x_test, y_train, y_test = apply_split(
            self.data, self.split_ratio, self.split_seed
        )

        # Check the lengths of the splits
        self.assertEqual(len(x_train[0]), 3)
        self.assertEqual(len(x_test[0]), 2)
        self.assertEqual(len(y_train), 3)
        self.assertEqual(len(y_test), 2)

        # Check the actual values to ensure they are split correctly
        expected_x_train = [[4, 2, 3], [9, 7, 8]]
        expected_x_test = [[5, 1], [10, 6]]
        expected_y_train = [40, 20, 30]
        expected_y_test = [50, 10]

        self.assertEqual(x_train, expected_x_train)
        self.assertEqual(x_test, expected_x_test)
        self.assertEqual(y_train, expected_y_train)
        self.assertEqual(y_test, expected_y_test)

    def test_apply_split_no_seed(self):
        """
        Test the apply_split function without a defined seed.
        """
        x_train, x_test, y_train, y_test = apply_split(self.data, self.split_ratio)

        # Check the lengths of the splits
        self.assertEqual(len(x_train[0]), 3)
        self.assertEqual(len(x_test[0]), 2)
        self.assertEqual(len(y_train), 3)
        self.assertEqual(len(y_test), 2)

    def test_apply_split_no_split_ratio(self):
        """
        Test the apply_split function without a defined split ratio.
        """
        x_values, y_values = apply_split(self.data, None)

        # Check the lengths of the splits
        self.assertEqual(len(x_values[0]), 5)
        self.assertEqual(len(y_values), 5)

        # Check the actual values to ensure they are returned correctly
        expected_x_values = [[4, 2, 3, 1, 5], [9, 7, 8, 6, 10]]
        expected_y_values = [40, 20, 30, 10, 50]

        self.assertEqual(x_values, expected_x_values)
        self.assertEqual(y_values, expected_y_values)

    def test_apply_split_empty_data(self):
        """
        Test the apply_split function with empty data.
        """
        empty_data: List[List[Any]] = [[], []]
        x_values, y_values = apply_split(empty_data, None)

        # Check the lengths of the splits
        self.assertEqual(len(x_values[0]), 0)
        self.assertEqual(len(y_values), 0)

        # Check the actual values to ensure they are returned correctly
        self.assertEqual(x_values, [[]])
        self.assertEqual(y_values, [])


if __name__ == "__main__":
    unittest.main()
