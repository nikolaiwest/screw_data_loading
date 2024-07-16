# get_data.py

import os
from typing import Any, List, Tuple, Union

import numpy as np

from screw_data_loading.load import (
    from_database,
    from_directory,
    from_hierarchical,
    get_logger,
)
from screw_data_loading.prep import validate_parameter

# Create and configure logger
logger = get_logger(__name__)


@validate_parameter
def get_data(
    source_path: str,
    tightening_steps: Union[str, int, List[int]] = "all",
    tightening_cycles: Union[str, int, List[int]] = "all",
    tightening_values: Union[str, List[str]] = ["time", "torque"],
    equidistancing_enabled: bool = False,
    target_length: int = None,
    cutoff_position: str = None,
    padding_value: float = None,
    padding_position: str = None,
    split_ratio: float = None,
    split_seed: int = None,
    return_format: str = "nested_list",
    result_format: str = "binary",
    logging_enabled: bool = True,
    verbose: bool = True,
) -> Union[
    Tuple[List[Any], List[Any], List[Any], List[Any]],
    Tuple[List[Any], List[Any]],
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    Tuple[np.ndarray, np.ndarray],
]:
    """
    Load and preprocess screwdriving data from the provided source.

    Parameters
    ----------
    source_path : str
        Path to the data source (directory of JSON files, H5 file, or database file).
    tightening_steps : Union[str, int, List[int]], optional
        Specify tightening steps to return. Can be 'all', a single integer, or a list of integers.
        Default is 'all'.
    tightening_cycles : Union[str, int, List[int]], optional
        Specify screw cycles to return. Can be 'all', a single integer, or a list of integers.
        Default is 'all'.
    tightening_values : Union[str, List[str]], optional
        Specify tightening measurements to return. Can be one or a list of "time", "torque", "angle", "gradient".
        Default is ["time", "torque"].
    equidistancing_enabled : bool, optional
        Enable equidistancing. Default is False.
    target_length : int, optional
        Max length for series cut-off. Default is None.
    cutoff_position : str, optional
        Position to truncate the padding ('pre' or 'post'). Default is None.
    padding_value : float, optional
        Value to use for padding. Default is None.
    padding_position : str, optional
        Position to perform the padding ('pre' or 'post'). Default is None.
    split_ratio : float, optional
        Split ratio for data. Default is None.
    split_seed : int, optional
        Seed for random splitting to ensure reproducibility. Default is None.
    return_format : str, optional
        Format for returning the data. Can be "nested_list" or "numpy_array". Default is "nested_list".
    result_format : str, optional
        Format for returning result values. Can be "raw" or "binary". Default is "binary".
    logging_enabled : bool, optional
        Enable logging. Default is True.
    verbose : bool, optional
        Enable verbose output. Default is True.

    Returns
    -------
    Union[Tuple[List[Any], List[Any], List[Any], List[Any]], Tuple[List[Any], List[Any]],
          Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]
        Loaded and processed data.
        - If split_ratio is defined, returns (x_train, x_test, y_train, y_test).
        - If split_ratio is None, returns (x_data, y_data).
        - The format of the returned data is determined by `return_format` (nested_list, flat_list, or numpy_array).

    Raises
    ------
    ValueError
        If the source_path is of an unsupported type.
    RuntimeError
        If data loading fails.

    Examples
    --------
    >>> from screwdata_loader import get_data
    >>> params = {
    >>>     "source_path": "data/10k_x25",
    >>>     "tightening_steps": "all",
    >>>     "tightening_cycles": [1, 2, 3, 4],
    >>>     "tightening_values": ["time", "torque"],
    >>>     "equidistancing_enabled": True,
    >>>     "target_length": 800,
    >>>     "cutoff_position": "post",
    >>>     "padding_value": 0,
    >>>     "padding_position": "pre",
    >>>     "split_ratio": 0.8,
    >>>     "split_seed": 42,
    >>>     "return_format": "nested_list",
    >>>     "result_format": "binary",
    >>>     "logging_enabled": True,
    >>>     "verbose": True,
    >>> }
    >>> x_train, x_test, y_train, y_test = get_data(**params)
    """

    # Get a dictionary containing the current parameters
    kwargs = locals()

    # Log the starting of the data loading process
    if logging_enabled:
        logger.info(f"Starting data loading process with parameters: {kwargs}")

    try:
        # Load data according to the provided source path
        if source_path.endswith(".db"):
            data = from_database(**kwargs)
            if logging_enabled:
                logger.info("Loaded data from database.")
        elif source_path.endswith(".h5"):
            data = from_hierarchical(**kwargs)
            if logging_enabled:
                logger.info("Loaded data from H5 file.")
        elif os.path.isdir(source_path):
            data = from_directory(**kwargs)
            if logging_enabled:
                logger.info("Loaded data from directory.")
        else:
            logger.error(f"Unsupported source type: {source_path}")
            raise ValueError(f"Unsupported source type: {source_path}")

    except Exception as e:
        logger.error(f"Failed to load data from {source_path}: {e}", exc_info=True)
        raise RuntimeError(f"Data loading failed for {source_path}.") from e

    return data
