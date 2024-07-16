from typing import Any, List, Union

import numpy as np


def apply_conversion(
    data: List[Any], result_format: str, return_format: str
) -> Union[List[Any], List[np.ndarray]]:
    """
    Apply conversion to the given data based on the specified result and return formats.

    Parameters
    ----------
    data : List[Any]
        The data to convert. It can be in the format of [x_train, x_test, y_train, y_test] or [x_values, y_values].
    result_format : str
        The format for the result values. Can be 'binary' or 'raw'.
    return_format : str
        The format for the returned data. Can be 'numpy_array' or 'nested_list'.

    Returns
    -------
    Union[List[Any], List[np.ndarray]]
        The converted data in the specified format.

    Examples
    --------
    >>> data = [
    >>>     ["OK", "NOK", "OK", "NOK"],
    >>>     ["OK", "OK", "NOK", "NOK"]
    >>> ]
    >>> converted_data = apply_conversion(data, result_format="binary", return_format="nested_list")
    >>> print(converted_data)
    >>>
    >>> data = [
    >>>     [1, 2, 3, 4],
    >>>     [5, 6, 7, 8],
    >>>     ["OK", "NOK", "OK", "NOK"],
    >>>     ["OK", "OK", "NOK", "NOK"]
    >>> ]
    >>> converted_data = apply_conversion(data, result_format="binary", return_format="numpy_array")
    >>> print(converted_data)
    """
    # Apply result format conversion
    if result_format == "binary":
        # If data is in the format of x_train, x_test, y_train, y_test
        if len(data) == 4:
            data[2] = convert_to_binary(data[2])
            data[3] = convert_to_binary(data[3])
        else:  # If data is in the format of x_values, y_values
            data[1] = convert_to_binary(data[1])
    elif result_format != "raw":
        raise ValueError(f"Unsupported result format: {result_format = }.")

    # Apply return format conversion
    if return_format == "numpy_array":
        return [np.array(d) for d in data]
    elif return_format == "nested_list":
        return data
    else:
        raise ValueError(f"Unsupported return format: {return_format = }.")


def convert_to_binary(data: List[str]) -> List[int]:
    """
    Convert result values to binary format.

    Parameters
    ----------
    data : List[str]
        The data to convert, where "NOK" is converted to 1 and anything else to 0.

    Returns
    -------
    List[int]
        The converted binary data.

    Examples
    --------
    >>> data = ["OK", "NOK", "OK", "NOK"]
    >>> binary_data = convert_to_binary(data)
    >>> print(binary_data)
    """
    return [1 if x == "NOK" else 0 for x in data]
