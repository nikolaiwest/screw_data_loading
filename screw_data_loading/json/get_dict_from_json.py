# get_dict_from_json.py

from json import load, JSONDecodeError
from typing import Any, Union, Dict
from os.path import join


def get_dict_from_json(
    file_path: str,
    file_name: str,
) -> Union[Dict[str, Any], None]:
    """
    Loads JSON data from a specified file into a dictionary.

    Parameters
    ----------
    file_path : str
        Path to the directory containing the JSON file.
    file_name : str
        Name of the JSON file to be loaded.

    Returns
    -------
    Union[Dict[str, Any], None]
        A dictionary containing the JSON data if successful, None otherwise.

    Raises
    ------
    FileNotFoundError
        If the specified JSON file is not found.
    JSONDecodeError
        If there is an error decoding the JSON file.

    Examples
    --------
    >>> data = get_dict_from_json('data', 'example.json')
    >>> if data is not None:
    >>>     print(data)
    """

    # Construct the full path to the JSON file
    json_file_path = join(file_path, file_name)

    # Attempt to open and load the JSON file
    try:
        with open(json_file_path, "r") as json_file:
            return load(json_file)
    # Handle file not found error
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"JSON file not found ({json_file_path}): {e}",
        ) from e
    # Handle JSON decoding errors
    except JSONDecodeError as e:
        raise JSONDecodeError(
            f"Error decoding JSON file ({json_file_path}): {e}",
        ) from e
    # Handle any other unexpected errors
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred while loading JSON file ({json_file_path}): {e}",
        ) from e
