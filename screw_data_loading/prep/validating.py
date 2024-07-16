# validating.py

import inspect
import os
from dataclasses import dataclass
from functools import wraps
from typing import Any, Dict, List, Union

from screw_data_loading.logs import get_logger

logger = get_logger(__name__)


class ParameterValidationError(Exception):
    """Exception raised for errors in the input parameters."""

    pass


@dataclass
class ParameterNames:
    """Simple data class for handling the parameter names."""

    source_path: str
    tightening_steps: str
    tightening_cycles: str
    tightening_values: str
    equidistancing_enabled: str
    target_length: str
    cutoff_position: str
    padding_value: str
    padding_position: str
    split_ratio: str
    split_seed: str
    return_format: str
    result_format: str
    logging_enabled: str
    verbose: str


# Define default values
PN = ParameterNames(
    "source_path",
    "tightening_steps",
    "tightening_cycles",
    "tightening_values",
    "equidistancing_enabled",
    "target_length",
    "cutoff_position",
    "padding_value",
    "padding_position",
    "split_ratio",
    "split_seed",
    "return_format",
    "result_format",
    "logging_enabled",
    "verbose",
)
ALL = "all"


def validate_parameter(func):
    @wraps(func)
    def wrapper(**kwargs):
        # Build a dictionary of parameter names to their default values
        default_args = {
            k: v.default
            for k, v in inspect.signature(func).parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        # Override defaults with any kwargs provided
        params = {**default_args, **kwargs}
        logging_enabled = params.get(PN.logging_enabled, True)

        if logging_enabled:
            logger.info(f"Starting the parameter check with parameters: {params}")

        # Perform parameter validation and update
        validate_and_update_params(params)

        if logging_enabled:
            logger.info("Finished the parameter check successfully with no errors.")
        return func(**params)

    return wrapper


def validate_and_update_params(params: Dict[str, Any]):
    """Validate and update parameters."""
    check_source_path(params.get(PN.source_path))
    params[PN.tightening_steps] = check_and_update_steps(
        params.get(PN.tightening_steps, ALL)
    )
    params[PN.tightening_cycles] = check_and_update_cycles(
        params.get(PN.tightening_cycles, ALL)
    )
    params[PN.tightening_values] = check_and_update_values(
        params.get(PN.tightening_values, ALL)
    )
    check_boolean_param(
        params.get(PN.equidistancing_enabled, False), PN.equidistancing_enabled
    )
    check_equidistancing(
        params.get(PN.equidistancing_enabled, False), params.get(PN.tightening_values)
    )
    check_positive_integer(params.get(PN.target_length), PN.target_length)
    check_choice_param(
        params.get(PN.cutoff_position), PN.cutoff_position, ["pre", "post"]
    )
    check_numeric_param(params.get(PN.padding_value), PN.padding_value)
    check_choice_param(
        params.get(PN.padding_position), PN.padding_position, ["pre", "post"]
    )
    check_split_ratio(params.get(PN.split_ratio))
    check_integer_param(params.get(PN.split_seed), PN.split_seed)
    check_choice_param(
        params.get(PN.return_format), PN.return_format, ["nested_list", "numpy_array"]
    )
    check_choice_param(
        params.get(PN.result_format), PN.result_format, ["binary", "raw"]
    )
    check_boolean_param(params.get(PN.logging_enabled, True), PN.logging_enabled)
    check_boolean_param(params.get(PN.verbose, True), PN.verbose)


def check_source_path(source_path: str):
    """Check if source path is valid."""
    if source_path is None:
        handle_error(f"Source path is not provided.")
    elif not os.path.exists(source_path):
        handle_error(f"Source path does not exist: {source_path}")


def check_and_update_steps(tightening_steps: Union[str, int, List[int]]) -> List[int]:
    """Check and update tightening steps."""
    valid_steps = list(range(1, 5))  # valid steps are 1 through 4
    if tightening_steps == ALL:
        return valid_steps
    elif isinstance(tightening_steps, int):
        if tightening_steps not in valid_steps:
            handle_error(
                f"Tightening_steps as int must be between 1 and 4, got {tightening_steps}."
            )
        return [tightening_steps]
    elif isinstance(tightening_steps, list):
        if not all(isinstance(item, int) for item in tightening_steps) or not all(
            item in valid_steps for item in tightening_steps
        ):
            handle_error(
                f"All items in tightening_steps must be integers between 1 and 4, got {tightening_steps}."
            )
        return tightening_steps
    else:
        handle_error(
            f"Invalid type for tightening_steps, expected 'all', an int, or a list of ints, got {type(tightening_steps).__name__}."
        )


def check_and_update_cycles(tightening_cycles: Union[str, int, List[int]]) -> List[int]:
    """Check and update tightening cycles."""
    valid_cycles = list(range(1, 51))  # cycles from 1 to 50
    if tightening_cycles == ALL:
        return valid_cycles
    elif isinstance(tightening_cycles, int):
        if tightening_cycles not in valid_cycles:
            handle_error(
                f"Tightening_cycles as int must be between 1 and 50, got {tightening_cycles}."
            )
        return [tightening_cycles]
    elif isinstance(tightening_cycles, list):
        if not all(isinstance(item, int) for item in tightening_cycles) or not all(
            item in valid_cycles for item in tightening_cycles
        ):
            handle_error(
                f"All items in tightening_cycles must be integers between 1 and 50, got {tightening_cycles}."
            )
        return tightening_cycles
    else:
        handle_error(
            f"Invalid type for tightening_cycles, expected 'all', an int, or a list of ints, got {type(tightening_cycles).__name__}."
        )


def check_and_update_values(tightening_values: Union[str, List[str]]) -> List[str]:
    """Check and update tightening values."""
    valid_values = ["time", "torque", "angle", "gradient"]
    if tightening_values == ALL:
        return valid_values
    elif isinstance(tightening_values, str):
        if tightening_values not in valid_values:
            handle_error(
                f"Tightening_values as str must be one of {valid_values}, got {tightening_values}"
            )
        return [tightening_values]
    elif isinstance(tightening_values, list):
        if not all(isinstance(item, str) for item in tightening_values) or not all(
            item in valid_values for item in tightening_values
        ):
            handle_error(
                f"All items in tightening_values must be strings and one of {valid_values}, got {tightening_values}."
            )
        return tightening_values
    else:
        handle_error(
            f"Invalid type for tightening_values, expected 'all', a string, or a list of strings, got {type(tightening_values).__name__}."
        )


def check_equidistancing(equidistancing_enabled: bool, tightening_values: List[str]):
    """Check if equidistancing is valid."""
    if (
        equidistancing_enabled
        and "time" not in tightening_values
        and tightening_values != ALL
    ):
        handle_error(
            f"The 'time' is required in tightening_values if equidistancing is enabled."
        )


def check_boolean_param(param: Any, param_name: str):
    """Check if the parameter is a boolean."""
    if not isinstance(param, bool):
        handle_error(
            f"Invalid type for {param_name}, expected 'bool', got {type(param).__name__}."
        )


def check_positive_integer(param: Any, param_name: str):
    """Check if the parameter is a positive integer."""
    if param is not None and (not isinstance(param, int) or param <= 0):
        handle_error(f"Invalid {param_name}, expected a positive integer, got {param}.")


def check_choice_param(param: Any, param_name: str, valid_choices: List[str]):
    """Check if the parameter is one of the valid choices."""
    if param is not None and param not in valid_choices:
        handle_error(
            f"Invalid {param_name}, expected one of {valid_choices}, got {param}."
        )


def check_numeric_param(param: Any, param_name: str):
    """Check if the parameter is a numeric type."""
    if param is not None and not isinstance(param, (int, float)):
        handle_error(
            f"Invalid {param_name}, expected a numeric type, got {type(param).__name__}."
        )


def check_split_ratio(split_ratio: Any):
    """Check if the split ratio is valid."""
    if split_ratio is not None and (
        not isinstance(split_ratio, float) or not (0 < split_ratio < 1)
    ):
        handle_error(
            f"Invalid split_ratio, expected a float between 0 and 1, got {split_ratio}."
        )


def check_integer_param(param: Any, param_name: str):
    """Check if the parameter is an integer."""
    if param is not None and not isinstance(param, int):
        handle_error(
            f"Invalid {param_name}, expected an integer, got {type(param).__name__}."
        )


def handle_error(message: str):
    """Log and raise an error with a given message."""
    logger.error(message)
    raise ParameterValidationError(message)
