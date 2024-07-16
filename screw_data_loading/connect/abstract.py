from abc import ABC, abstractmethod
from tqdm import tqdm
from numpy import nan, nanmean, nanvar
from typing import List, Union, Dict

from json.screw_run import ScrewRun


# TODO:
# Implement ID list/dict based import by scenario numbers
# Implement load data functions with train test splits
# ... same for load with cross validation


class AbstractConnection(ABC):
    """
    Abstract base class designed for the loading and processing of screw run data.

    This class provides a structured approach to load screw run data from various sources,
    including files, databases, or external services. It defines a framework for loading
    data (via the `load_run_ids` method), updating internal state and metrics based on the
    loaded data, and retrieving specific subsets of the data for analysis.

    Subclasses must implement the `load_run_ids` method to specify the data loading
    mechanism. The class also includes methods for updating counts of OK and NOK labels,
    managing data matrix codes (DMCs), and calculating statistics for the loaded data.

    Attributes:
    -----------
        all_run_ids (List[str]):
            List of all IDs of the screw runs.
        all_runs (List[ScrewRun]):
            List of all screw runs, loaded as ScrewRun objects.
        count_of_ok (int):
            Counter for the number of runs labeled as "OK".
        count_of_nok (int):
            Counter for the number of runs labeled as "NOK".
        count_of_all (int):
            Total count of runs.
        counts_of_dmc (Dict[str, int]):
            Counts of individual DMCs.
        labels_of_dmc (Dict[str, List[str]]):
            Lists of labels ("OK" vs. "NOK") for each DMC.
        ids_of_dmc (Dict[str, List[str]]):
            Lists of IDs for each DMC.
        num_of_runs (int):
            Total number of runs processed.
        num_of_dmcs (int):
            Total number of unique DMCs processed.

    The class supports methods for loading and processing data, including updating metrics,
    retrieving data series for analysis, and aggregating statistics. It serves as a base for
    creating specific data loaders tailored to different data sources and formats.
    """

    def __init__(self) -> None:
        """
        Initializie the DataLoader.
        """
        # List of all ids of the screw runs (e.g. ["Ch_300...json", Ch_300...json", ...])
        self.all_run_ids: List[str] = []
        # List of all screw runs, loaded from as ScrewRun objects by their run id from raw data
        self.all_runs: List[ScrewRun] = []
        # Counter variables of OK and NOK labels in the data
        self.count_of_ok: int = 0
        self.count_of_nok: int = 0
        self.count_of_all: int = 0
        # Dicts to track the data matrix codes (DMC) in the data set
        self.counts_of_dmc: dict = {}  # Counts of individual DMCs
        self.labels_of_dmc: Dict[List] = {}  # Lists of their label ("OK" vs. "NOK")
        self.ids_of_dmc: Dict[List] = (
            {}
        )  # List of their IDs (aka file names, e.g. "Ch_000...json")
        # Counter variables to track the number of runs and individual DMCs
        self.num_of_runs: int = 0
        self.num_of_dmcs: int = 0

    @abstractmethod
    def load_run_ids(self, source: Union[str, List[Union[str, int]]]) -> None:
        """
        Abstract method to load run ids from a specified source.

        Args:
            source (Union[str, List[Union[str, int]]]):
                The source from which to load data that can either be a path, a list
                of scenarios, a list of scenario numbers or a list of screw runs.
        """
        pass

    def load_and_update(self):
        self.load_runs_from_ids()
        self.update()

    def load_runs_from_ids(self):
        self.all_runs = [
            ScrewRun(name=run_id)
            for run_id in tqdm(self.all_run_ids, desc="Loading screw run data")
        ]

    def update(self) -> None:
        """
        Collection of methods to update all additional metrics of the screw run.
        """
        # Update the label counts
        self.update_label_counts()
        # Update the data matrix code dictionaries
        self.update_dmc_dics()
        # Update the number of runs
        self.update_num_of_runs()
        # Update the number of DMCs
        self.update_num_of_dmcs()

    def update_label_counts(self) -> None:
        for screw_run in self.all_runs:
            # Update the count of "OK" and "NOK" screw runs
            if screw_run.result == "OK":
                self.count_of_ok += 1
            elif screw_run.result == "NOK":
                self.count_of_nok += 1
            else:
                raise ValueError(
                    f"Unkown label {screw_run.result} in screw run {screw_run.name}"
                )
        self.count_of_all = self.count_of_ok + self.count_of_nok

    def update_dmc_dics(self) -> None:
        for screw_run in self.all_runs:
            # Update the dmc dictionaries for each screw run
            if screw_run.code not in self.counts_of_dmc.keys():
                self.counts_of_dmc[screw_run.code] = 1
                self.labels_of_dmc[screw_run.code] = [screw_run.result]
                self.ids_of_dmc[screw_run.code] = [screw_run.name]
            else:
                self.counts_of_dmc[screw_run.code] += 1
                self.labels_of_dmc[screw_run.code] += [screw_run.result]
                self.ids_of_dmc[screw_run.code] += [screw_run.name]

    def update_num_of_runs(self) -> None:
        """
        Check if the lists all_run_ids and all_runs have the same lengths and assigns it to a new attribute num_of_runs.
        """
        num_of_run_ids = len(self.all_run_ids)
        num_of_runs = len(self.all_runs)
        try:
            # Double check the lengths to avoid missing runs
            assert num_of_run_ids == num_of_runs
            self.num_of_runs = num_of_runs
        except AssertionError:
            raise AssertionError(
                f"The number of run ids {num_of_run_ids} does not match the number of runs {num_of_runs}"
            )

    def update_num_of_dmcs(self) -> None:
        """
        Check if the dicts counts_of_dmc and labels_of_dmc have the same lengths and assigns it to a new attribute num_of_dmcs.
        """
        num_of_dmcs = len(self.counts_of_dmc)
        num_of_dmcs_by_label = len(self.labels_of_dmc)
        try:
            # Double check the lengths to avoid missing runs
            assert num_of_dmcs == num_of_dmcs_by_label
            self.num_of_dmcs = num_of_dmcs
        except AssertionError:
            raise AssertionError(
                f"The number of dmc labels {num_of_dmcs_by_label} does not match the number of dmcs by count {num_of_dmcs}"
            )

    def get_time_values(self) -> List[List[float]]:
        return [run.time_values for run in self.all_runs]

    def get_angle_values(self) -> List[List[float]]:
        return [run.angle_values for run in self.all_runs]

    def get_torque_values(self) -> List[List[float]]:
        return [run.torque_values for run in self.all_runs]

    def get_gradient_values(self) -> List[List[float]]:
        return [run.gradient_values for run in self.all_runs]

    def get_run_ids(self) -> List[str]:
        """
        Get the loaded run ids.

        Returns:
            List[str]
                The loaded data
        """
        return self.all_run_ids

    def get_screw_runs(self) -> List[ScrewRun]:
        """
        Get the loaded runs.

        Returns:
            List[ScrewRun]
                The loaded data
        """
        return self.all_runs

    def get_run_results(self) -> List[str]:
        """
        Get the labels of the screw data (e.g. "OK" or "NOK").

        Returns:
            List[str]
                The labels of every loaded screw run.
        """
        return [run.result for run in self.all_runs]

    def aggregate_all_series(self, list_of_series: List[List[float]]) -> List[float]:
        # Find the length of the longest time series
        max_len = max(map(len, list_of_series))

        # Pad all time series with NaN values to make them equal length
        padded_list_of_series = [
            series + [nan] * (max_len - len(series)) for series in list_of_series
        ]

        # Calculate  and return the mean for each time point, ignoring NaN values
        return nanmean(padded_list_of_series, axis=0), nanvar(
            padded_list_of_series, axis=0
        )
