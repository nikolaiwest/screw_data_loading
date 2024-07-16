# from_directory.py

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import numpy as np
from tqdm import tqdm

from screw_data_loading.json.get_dict_from_json import get_dict_from_json
from screw_data_loading.logs import get_logger
from screw_data_loading.prep import (
    apply_conversion,
    apply_equidistancing,
    apply_padding,
    apply_split,
    apply_truncating,
)


@dataclass
class KeyNames:
    """Data class for handling the JSON keys."""

    id: str
    label: str
    steps: str
    graph: str


# Configure logging
logger = get_logger(__name__)


def from_directory(
    source_path: str,
    tightening_steps: Union[str, int, List[int]],
    tightening_cycles: Union[str, int, List[int]],
    tightening_values: Union[str, List[str]],
    equidistancing_enabled: bool,
    target_length: int,
    cutoff_position: str,
    padding_value: float,
    padding_position: str,
    split_ratio: float,
    split_seed: int,
    return_format: str,
    result_format: str,
    logging_enabled: bool,
    verbose: bool,
) -> Union[
    Tuple[List[Any], List[Any], List[Any], List[Any]],
    Tuple[List[Any], List[Any]],
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    Tuple[np.ndarray, np.ndarray],
]:
    """Load screwdriving data from a directory and apply preprocessing steps.

    Parameters
    ----------
    source_path : str
        Path to the data source (directory of JSON files).
    tightening_steps : Union[str, int, List[int]]
        Specify tightening steps to return. Can be 'all', a single integer, or a list of integers.
    tightening_cycles : Union[str, int, List[int]]
        Specify cycles to return. Can be 'all', a single integer, or a list of integers.
    tightening_values : Union[str, List[str]]
        Specify tightening measurements to return. Can be one or a list of "time", "torque", "angle", "gradient".
    equidistancing_enabled : bool
        Enable equidistancing.
    target_length : int
        Max length for series cut-off.
    cutoff_position : str
        Position to truncate the padding ('pre' or 'post').
    padding_value : float
        Value to use for padding.
    padding_position : str
        Position to perform the padding ('pre' or 'post').
    split_ratio : float
        Split ratio for data.
    split_seed : int
        Seed for random splitting to ensure reproducibility.
    return_format : str
        Format for returning the data. Can be "nested_list" or "numpy_array".
    result_format : str
        Format for returning result values. Can be "raw" or "binary".
    logging_enabled : bool
        Enable logging.
    verbose : bool
        Enable verbose output.

    Returns
    -------
    Union[Tuple[List[Any], List[Any], List[Any], List[Any]], Tuple[List[Any], List[Any]]]
        Loaded and processed data.
        - If split_ratio is defined, returns (x_train, x_test, y_train, y_test).
        - If split_ratio is None, returns (x_data, y_data).
    """
    KN = KeyNames("id code", "result", "tightening steps", "graph")

    # Get all file names in the source path
    all_file_names = os.listdir(source_path)

    # Initialize a dictionary to count tightening cycles
    all_cycle_counts: Dict[str, int] = {}

    # Initialize a nested list to return all tightening values (including label)
    return_values: List[List[Any]] = [[] for _ in range(len(tightening_values) + 1)]

    # Initialize lists to store metrics for logging
    equidistancing_logs: List[Tuple[int, int]] = []
    padding_logs: List[Tuple[int, int]] = []
    truncating_logs: List[Tuple[int, int]] = []

    # Iterate over all JSON file names
    for file_name in tqdm(
        all_file_names, desc="Loading and preparing data: ", disable=not verbose
    ):
        # Load file content from json
        file = get_dict_from_json(source_path, file_name)

        # Extract required values from the file
        file_id = file.get(KN.id)
        file_label = file.get(KN.label)
        file_steps = file.get(KN.steps)

        # Skip files with missing key values
        if file_id is None or file_label is None or file_steps is None:
            if logging_enabled:
                logger.warning(f"Missing keys in file: {file_name}")
            continue

        # Update the count of tightening cycles for the current file ID
        all_cycle_counts[file_id] = all_cycle_counts.get(file_id, 0) + 1

        # Check if the current tightening cycle count is in the requested cycles
        if all_cycle_counts[file_id] in tightening_cycles or tightening_cycles == "all":
            # Initialize dictionary to store values for the current cycle
            all_cycle_values = {k: [] for k in tightening_values}

            # Iterate only the requested tightening steps
            for step in [
                file_steps[step_idx - 1]
                for step_idx in tightening_steps
                if step_idx <= len(file_steps)
            ]:
                # Add requested values to the cycle values dictionary
                for value in tightening_values:
                    all_cycle_values[value].extend(
                        step[KN.graph].get(f"{value} values", [])
                    )

            # Apply equidistancing if enabled
            if equidistancing_enabled:
                all_cycle_values, initial_length, final_length = apply_equidistancing(
                    all_cycle_values
                )
                equidistancing_logs.append((initial_length, final_length))

            # Apply truncating if target length and cutoff position are specified
            if target_length is not None and cutoff_position is not None:
                all_cycle_values, trunc_initial_lengths, trunc_final_lengths = (
                    apply_truncating(all_cycle_values, target_length, cutoff_position)
                )
                truncating_logs.append((trunc_initial_lengths, trunc_final_lengths))

            # Apply padding if padding value and position are specified
            if padding_value is not None and padding_position is not None:
                all_cycle_values, pad_initial_lengths, pad_final_lengths = (
                    apply_padding(
                        all_cycle_values, padding_value, padding_position, target_length
                    )
                )
                padding_logs.append((pad_initial_lengths, pad_final_lengths))

            # Append cycle values to the return values list
            for i, value in enumerate(tightening_values):
                return_values[i].append(all_cycle_values[value])

            # Append the label to the return values list
            return_values[-1].append(file_label)

    # Apply split_ratio
    return_values = apply_split(return_values, split_ratio, split_seed)

    # Apply conversion to the return values
    return_values = apply_conversion(return_values, result_format, return_format)

    # Optionally log the metrics
    if logging_enabled:
        logger.info("Finished loading and preparing the data.")
        log_metrics(
            equidistancing_logs,
            truncating_logs,
            padding_logs,
            return_values,
            result_format,
            return_format,
        )

    return return_values


def log_metrics(
    equidistancing_logs: List[Tuple[int, int]],
    truncating_logs: List[Tuple[int, int]],
    padding_logs: List[Tuple[int, int]],
    return_values: Any,
    result_format: str,
    return_format: str,
) -> None:
    """Log metrics for equidistancing, truncating, and padding."""
    if equidistancing_logs:
        average_initial_length = sum(length[0] for length in equidistancing_logs) / len(
            equidistancing_logs
        )
        average_final_length = sum(length[1] for length in equidistancing_logs) / len(
            equidistancing_logs
        )
        logger.info(
            f"- Equidistancing results (avg. lengths): {average_initial_length:.2f} -> {average_final_length:.2f}"
        )

    if truncating_logs:
        average_initial_length = sum(length[0] for length in truncating_logs) / len(
            truncating_logs
        )
        average_final_length = sum(length[1] for length in truncating_logs) / len(
            truncating_logs
        )
        logger.info(
            f"- Truncating results (avg. lengths): {average_initial_length:.2f} -> {average_final_length:.2f}"
        )

    if padding_logs:
        average_initial_length = sum(length[0] for length in padding_logs) / len(
            padding_logs
        )
        average_final_length = sum(length[1] for length in padding_logs) / len(
            padding_logs
        )
        logger.info(
            f"- Padding results (avg. lengths): {average_initial_length:.2f} -> {average_final_length:.2f}"
        )

    if isinstance(return_values, tuple) and len(return_values) == 4:
        x_train, x_test, y_train, y_test = return_values
        logger.info(
            f"Training data count: {len(x_train[0])}, Testing data count: {len(x_test[0])}"
        )

        if result_format == "binary":
            train_labels = y_train
            test_labels = y_test
        else:  # result_format == "raw"
            train_labels = [1 if label == "NOK" else 0 for label in y_train]
            test_labels = [1 if label == "NOK" else 0 for label in y_test]

        logger.info(
            f"Training labels - 0 count: {train_labels.count(0)}, 1 count: {train_labels.count(1)}"
        )
        logger.info(
            f"Testing labels - 0 count: {test_labels.count(0)}, 1 count: {test_labels.count(1)}"
        )

    if return_format == "numpy_array":
        for i, array in enumerate(return_values):
            logger.info(f"Array {i} shape: {array.shape}")
