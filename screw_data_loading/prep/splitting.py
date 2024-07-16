# splitting.py

import random
from typing import Any, List, Optional, Tuple, Union

import numpy as np


def apply_split(
    data: List[List[Any]],
    split_ratio: float,
    split_seed: Optional[int] = None,
) -> Union[
    Tuple[List[Any], List[Any], List[Any], List[Any]],
    Tuple[List[Any], List[Any]],
]:
    """
    Split data into training and testing sets based on the given split ratio.

    Parameters
    ----------
    data : List[List[Any]]
        The data to split. Each sublist represents a type of measurement.
    split_ratio : float
        The ratio for the training set. Should be between 0 and 1.
    split_seed : Optional[int], optional
        The random seed for reproducibility. Defaults to None.

    Returns
    -------
    Union[Tuple[List[Any], List[Any], List[Any], List[Any]], Tuple[List[Any], List[Any]]]
        If split_ratio is defined, returns (x_train, x_test, y_train, y_test).
        If split_ratio is None, returns (x_values, y_values).

    Examples
    --------
    >>> data = [
    >>>     [1, 2, 3, 4, 5],
    >>>     [10, 20, 30, 40, 50]
    >>> ]
    >>> split_ratio = 0.8
    >>> split_seed = 42
    >>> x_train, x_test, y_train, y_test = apply_split(data, split_ratio, split_seed)
    >>> print(f"x_train: {x_train}, x_test: {x_test}, y_train: {y_train}, y_test: {y_test}")
    """

    if split_seed is not None:
        random.seed(split_seed)

    # Determine the length of the data
    data_length = len(data[0])

    # Generate shuffled indices
    indices = list(range(data_length))
    random.shuffle(indices)

    # Shuffle the data according to the shuffled indices
    shuffled_data = [[values[i] for i in indices] for values in data]

    # Flatten the data
    flattened_data = flatten(shuffled_data)

    # Split the data into training and testing sets
    if split_ratio is not None and 0 < split_ratio < 1:
        split_index = int(data_length * split_ratio)
        training_data = [values[:split_index] for values in flattened_data]
        testing_data = [values[split_index:] for values in flattened_data]

        # Return the training and testing sets
        return (
            training_data[:-1],  # x_train
            testing_data[:-1],  # x_test
            training_data[-1],  # y_train
            testing_data[-1],  # y_test
        )
    else:
        # Return the entire data as x_values and y_values
        return flattened_data[:-1], flattened_data[-1]


def flatten(data: List[List[Any]]) -> List[List[Any]]:
    """
    Flatten nested lists within the data.

    Parameters
    ----------
    data : List[List[Any]]
        The data to flatten.

    Returns
    -------
    List[List[Any]]
        The flattened data.
    """
    return [
        [
            array.tolist() if isinstance(array, np.ndarray) else array
            for array in sublist
        ]
        for sublist in data
    ]
