# default
import os
from tqdm import tqdm
from typing import Union, List, Any

# Project
from screw_data_loading.connect.abstract import AbstractConnection
from screw_data_loading.json.screw_run import ScrewRun


class JsonConnection(AbstractConnection):
    """
    A loader class that extends BaseLoader to specifically handle loading screw driving
    data from JSON files in a given directory or directories. It initializes the loader
    with the path to the data and automatically loads run IDs and updates internal state
    based on the loaded data.

    Attributes inherited and used from BaseLoader include lists for run IDs, run objects,
    and various counters and dictionaries for managing and analyzing the data.
    """

    def __init__(self, path: Union[str, List[str]]) -> None:
        """
        Initializes the DataFromJSON loader with a path or paths to JSON files, loads run IDs,
        and then loads the screw runs based on those IDs, updating the loader's internal state.

        Args:
            path: A single path (str) or a list of paths (List[str]) pointing to the directories
                  containing the screw run JSON files to be loaded.

        Raises:
            ValueError: If the provided path argument is neither a string nor a list of strings.
        """
        # Initialize the base class
        super().__init__()
        # Load run IDs from the specified path(s)
        self.load_run_ids(path=path)
        # Load screw runs based on IDs and update loader state
        self.load_and_update()

    def load_run_ids(self, path: Union[str, List[str]]) -> None:
        """
        Load screw runs from a specified path or list of paths.

        Parameters:
        -----------
        path : str or List[str]
            The path or list of paths from which to load the runs.

        Returns:
        --------
        None
        """
        # Check if path is a single string or a list of strings
        if isinstance(path, str):
            paths = [path]
        elif isinstance(path, list):
            paths = path
        else:
            raise ValueError(
                "Invalid input type for 'path'. It should be a string or a list of strings."
            )

        # all_run_ids the list to store all runs
        self.all_runs = []

        # Iterate through each path
        for current_path in paths:
            # Check if the current path is valid
            if not os.path.isdir(current_path):
                raise InvalidPathError(
                    f"The specified path '{current_path}' is not a directory."
                )

            # Get all json files from the current path and append to the list
            current_runs = [f for f in os.listdir(current_path) if f.endswith(".json")]
            self.all_run_ids.extend(current_runs)


class InvalidPathError(Exception):
    """
    Exception raised for invalid paths in PathLoader.

    Attributes:
    ----------
    message : str
        Explanation of the error.
    """


def load_from_json(
    source: str,
    values: list[str],
    cycles: Any,
    steps: Any,
    log: bool,
    verbose: bool,
):
    # Check if path from source is valid (backup check)
    if not os.path.isdir(source):
        raise InvalidPathError(
            f"The specified source is not a valid directory: {source}."
        )

    # Check if `time values` is in values if make_equidistance is required
    #

    # Create empty list to collect all screw runs
    list_of_all_screw_runs = []
    # Create empty dict for cycle count by data matrix code
    dict_of_all_dmc_counts = {}
    # Create empty tuple to return according to selected values
    tuple_of_result_values = tuple([] for _ in values)

    # Iterate source path and check files with progress bar
    for file_name in tqdm(
        iterable=os.listdir(source),
        desc="Loading from JSON: ",
        disable=not verbose,
    ):
        # Check file types to load only json
        if not file_name.endswith(".json"):
            raise ImportWarning(
                f"Source {source} should contain only JSON, but found: {file_name}."
            )

        # Get current file as ScrewRun
        screw_run = ScrewRun(name=file_name, path=source, steps=steps)
        screw_run_dmc = screw_run.get_dmc()

        # Update the dict of all dmcs counts for the current screw run
        if screw_run_dmc in dict_of_all_dmc_counts.keys():
            dict_of_all_dmc_counts[screw_run_dmc] += 1
        else:
            dict_of_all_dmc_counts[screw_run_dmc] = 1

        # Get cycle of the current screw run (two screws per work piece)
        # e.g. transform [1,2,3,4,5,...,48,49,50] to [1,1,2,2,3,...,24,25,25]
        screw_run_cycle = (dict_of_all_dmc_counts[screw_run_dmc] - 1) // 2 + 1

        # Transform cycles to list if int was provided
        if isinstance(cycles, int):
            cycles = [cycles]
        # Add current screw run to list of all screw runs if in cycles
        if cycles is None or screw_run_cycle in cycles:
            list_of_all_screw_runs.append(screw_run)
        else:  # Invalid cycles
            raise ValueError(f"Provided cycles yield no screw runs: {cycles}")

        # Add values from screw_runs to return tuple
        for i, value_to_return in enumerate(values):
            if value_to_return == "cycle number":
                tuple_of_result_values[i].append(
                    dict_of_all_dmc_counts[screw_run_dmc],
                )
            elif value_to_return == "results":
                tuple_of_result_values[i].append(
                    screw_run.get_result(),
                )
            else:
                tuple_of_result_values[i].append(
                    screw_run.get_run_values(value_to_return)
                )

    return tuple_of_result_values
