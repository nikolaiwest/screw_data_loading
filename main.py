# main.py

import os

from screw_data_loading.config import DEFAULT_PARAMS
from screw_data_loading.get_data import get_data
from screw_data_loading.load import get_logger

# Get the logger
logger = get_logger(__name__)


def main():
    """
    Main function to load and preprocess screwdriving data using the get_data function.

    This function:
    - Ensures the source path exists.
    - Logs the parameters being used.
    - Calls the get_data function with the default parameters.
    - Unpacks and logs some basic information about the loaded data.

    Note:
    - If you are here to load screw data, use the `get_data` method from `screw_data_loading/`.
    """
    # Ensure the source path exists
    if not os.path.exists(DEFAULT_PARAMS["source_path"]):
        logger.error(f"Source path {DEFAULT_PARAMS['source_path']} does not exist.")
        return

    try:
        # Log the parameters being used
        logger.info("Using parameters: %s", DEFAULT_PARAMS)

        # Load data
        data = get_data(**DEFAULT_PARAMS)

        # Check the format and unpack data if necessary
        if DEFAULT_PARAMS["split_ratio"] is not None:
            if DEFAULT_PARAMS["return_format"] == "nested_list":
                x_train, x_test, y_train, y_test = data
            else:
                x_train, x_test, y_train, y_test = data
        else:
            if DEFAULT_PARAMS["return_format"] == "nested_list":
                x_data, y_data = data
            else:
                x_data, y_data = data

        # Log some information about the loaded data
        if DEFAULT_PARAMS["split_ratio"] is not None:
            logger.info(
                f"Loaded {len(x_train)} training samples and {len(x_test)} test samples."
            )
        else:
            logger.info(f"Loaded {len(x_data)} samples.")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
