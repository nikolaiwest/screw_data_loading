# padding.py

from typing import Any, Dict, List, Tuple

import numpy as np


def apply_padding(
    cycle_values: Dict[str, List[Any]],
    padding_val: float,
    padding_pos: str,
    target_length: int,
) -> Tuple[Dict[str, np.ndarray], int, int]:
    """
    Apply padding to the given cycle values.

    Parameters
    ----------
    cycle_values : Dict[str, List[Any]]
        A dictionary containing cycle values, where the keys represent the value types
        and the values are lists of corresponding values.
    padding_val : float
        The value to use for padding.
    padding_pos : str
        Position to apply padding ('pre' or 'post').
    target_length : int
        The target length of the sequences after padding.

    Returns
    -------
    Tuple[Dict[str, np.ndarray], int, int]
        A tuple containing the dictionary with padded cycle values, the initial length, and the final length.

    Examples
    --------
    >>> cycle_values = {
    >>>     "time": [0.0, 0.1, 0.2],
    >>>     "torque": [10, 20, 30]
    >>> }
    >>> padded_values, initial_len, final_len = apply_padding(cycle_values, 0, 'post', 5)
    >>> print(padded_values)
    >>> print(f"Initial length: {initial_len}, Final length: {final_len}")
    """
    # Determine the initial length of the cycle values
    initial_length = len(next(iter(cycle_values.values())))

    def pad_sequence(
        seq: List[Any], target_length: int, padding_val: float, padding_pos: str
    ) -> np.ndarray:
        """Pad a sequence to the target length with the specified padding value and position."""
        pad_len = target_length - len(seq)
        if padding_pos == "pre":
            return np.pad(seq, (pad_len, 0), "constant", constant_values=padding_val)
        else:
            return np.pad(seq, (0, pad_len), "constant", constant_values=padding_val)

    # Apply padding to each value type in the cycle values
    padded_sequences = {
        k: pad_sequence(v, target_length, padding_val, padding_pos)
        for k, v in cycle_values.items()
    }

    # Overwrite the time to match the new length
    padded_sequences["time"] = np.linspace(
        0, (target_length - 1) * 0.0012, target_length
    )

    # Determine the final length of the padded cycle values
    final_length = len(next(iter(padded_sequences.values())))

    # Return the padded cycle values along with the initial and final lengths
    return padded_sequences, initial_length, final_length
