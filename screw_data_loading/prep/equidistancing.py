# equidistancing.py
from typing import Any, Dict, List, Tuple

import numpy as np


def apply_equidistancing(
    cycle_values: Dict[str, List[Any]],
    interval_length: float = 0.0012,
) -> Tuple[Dict[str, np.ndarray], int, int]:
    """
    Apply equidistancing to the given cycle values.

    Parameters
    ----------
    cycle_values : Dict[str, List[Any]]
        A dictionary containing cycle values. The keys represent the value types,
        and the values are lists of values. The "time" key is used as the index.
    interval_length : float, optional
        The desired interval length for equidistancing. Defaults to 0.0012.

    Returns
    -------
    Tuple[Dict[str, np.ndarray], int, int]
        A tuple containing the following:
        - A dictionary with equidistant cycle values, where the keys represent the value types
          and the values are numpy arrays of equidistant values.
        - The initial length of the time values before equidistancing.
        - The final length of the time values after equidistancing.

    Examples
    --------
    >>> cycle_values = {
    >>>     "time": [0.0, 0.1, 0.2, 0.3],
    >>>     "torque": [10, 20, 30, 40]
    >>> }
    >>> equidistant_values, initial_len, final_len = apply_equidistancing(cycle_values)
    >>> print(equidistant_values)
    >>> print(f"Initial length: {initial_len}, Final length: {final_len}")
    """
    # Extracting time values and determining the initial length
    time_values = np.array(cycle_values["time"])
    initial_length = len(time_values)

    # Removing duplicates in 'time' by averaging the values
    unique_times, unique_indices = np.unique(time_values, return_index=True)
    full_time_range = np.arange(
        unique_times.min(), unique_times.max() + interval_length, interval_length
    )

    # Creating the mean values for unique times
    mean_values_dict = {
        key: np.array(values)[unique_indices]
        for key, values in cycle_values.items()
        if key != "time"
    }

    # Dictionary to store equidistant cycle values
    equidistant_cycle_values = {}

    # Interpolating values to fit the equidistant time intervals
    for key, mean_values in mean_values_dict.items():
        interpolated_values = np.interp(full_time_range, unique_times, mean_values)
        equidistant_cycle_values[key] = interpolated_values

    # Store the full time range in the dictionary
    equidistant_cycle_values["time"] = full_time_range
    final_length = len(full_time_range)

    # Return the equidistant cycle values and the lengths before and after equidistancing
    return equidistant_cycle_values, initial_length, final_length
