import os
import unittest

from screw_data_loading.get_data import get_data


class TestGetData(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = (
            "./tests/data/"  # Update with the actual path to your test data directory
        )
        self.default_params = {
            "source_path": os.path.join(self.test_data_dir, "testset_01"),
            "tightening_steps": "all",
            "tightening_cycles": [1, 2, 3, 4],
            "tightening_values": ["time", "torque"],
            "equidistancing_enabled": True,
            "target_length": 800,
            "cutoff_position": "post",
            "padding_value": 0,
            "padding_position": "pre",
            "split_ratio": 0.8,
            "split_seed": 42,
            "result_format": "raw",
            "return_format": "nested_list",
            "logging_enabled": True,
            "verbose": True,
        }

    def test_get_data_directory(self):
        """
        Test get_data function with source_path as a directory.
        """

        # Call the get_data function
        result = get_data(**self.default_params)

        # Check the return values (example checks, adjust according to your data)
        self.assertEqual(len(result), 4)  # x_train, x_test, y_train, y_test

    def test_get_data_database(self):
        """
        Test get_data function with source_path as a database.
        """
        pass

    def test_get_data_hierarchical(self):
        """
        Test get_data function with source_path as a hierarchical file.
        """
        pass

    def test_get_data_split(self):
        """
        Test get_data function with split_ratio defined.
        """

        # Call the get_data function
        result = get_data(**self.default_params)

        # Check the return values (example checks, adjust according to your data)
        self.assertEqual(len(result), 4)  # x_train, x_test, y_train, y_test

    def test_get_data_no_split(self):
        """
        Test get_data function without split_ratio defined.
        """
        params = self.default_params.copy()
        params["split_ratio"] = None

        # Call the get_data function
        result = get_data(**params)

        # Check the return values (example checks, adjust according to your data)
        self.assertEqual(len(result), 2)  # x_values, y_values

    def test_get_data_numpy_array(self):
        """
        Test get_data function with return_format set to numpy_array.
        """
        import numpy as np

        params = self.default_params.copy()
        params["return_format"] = "numpy_array"

        # Call the get_data function
        result = get_data(**params)

        # Check the return values (example checks, adjust according to your data)
        self.assertEqual(len(result), 4)  # x_train, x_test, y_train, y_test
        for array in result:
            self.assertIsInstance(array, np.ndarray)


if __name__ == "__main__":
    unittest.main()
