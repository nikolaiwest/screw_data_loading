# truncating.py

from typing import Dict, List, Any, Tuple


def apply_truncating(
    cycle_values: Dict[str, List[Any]],
    target_length: int,
    cutoff_position: str,
) -> Tuple[Dict[str, List[Any]], int, int]:
    """
    Apply truncating to the given cycle values.

    Parameters
    ----------
    cycle_values : Dict[str, List[Any]]
        A dictionary containing cycle values, where the keys represent the value types
        and the values are lists of corresponding values.
    target_length : int
        The index to truncate to.
    cutoff_position : str
        Position to apply truncating ('pre' or 'post').

    Returns
    -------
    Tuple[Dict[str, List[Any]], int, int]
        A tuple containing the dictionary with truncated cycle values, the initial length, and the final length.

    Examples
    --------
    >>> cycle_values = {
    >>>     "time": [0.0, 0.1, 0.2, 0.3, 0.4],
    >>>     "torque": [10, 20, 30, 40, 50]
    >>> }
    >>> truncated_values, initial_len, final_len = apply_truncating(cycle_values, 3, 'post')
    >>> print(truncated_values)
    >>> print(f"Initial length: {initial_len}, Final length: {final_len}")
    """

    # Determine the initial length of the cycle values
    initial_length = len(next(iter(cycle_values.values())))

    # Function to truncate a sequence based on the target length and cutoff position
    def truncate_sequence(
        seq: List[Any], target_length: int, cutoff_position: str
    ) -> List[Any]:
        if cutoff_position == "pre":
            # If the cutoff position is 'pre', retain the last 'target_length' elements
            return seq[-target_length:]
        else:
            # Otherwise, retain the first 'target_length' elements
            return seq[:target_length]

    # Apply truncating to each value type in the cycle values
    truncated_sequences = {
        k: truncate_sequence(v, target_length, cutoff_position)
        for k, v in cycle_values.items()
    }

    # Determine the final length of the truncated cycle values
    final_length = len(next(iter(truncated_sequences.values())))

    # Return the truncated cycle values along with the initial and final lengths
    return truncated_sequences, initial_length, final_length
