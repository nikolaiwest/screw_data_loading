import os
import json

from itertools import chain
from typing import Union, List, Dict, Any

from .screw_step import ScrewStep


class ScrewRun:
    """
    Load screw runs from json by file name.
    """

    def __init__(
        self,
        name: str = None,
        path: str = None,
        steps: list[int] = None,
    ):
        """Initializes the ScrewRun using a file name and a system path."""

        # Set name and path
        self.name: str = name
        self.path: str = path
        self.steps: list[list] = steps

        # Load data from JSON file
        self.set_attributes_from_json()

    def set_attributes_from_json(self) -> None:
        """Loads data from JSON file."""

        # Load json as dict from source
        json_dict = self.get_json_as_dict()

        # Result of the screw run according to the process control (e.g., "NOK" for not okay)
        self.result = str(json_dict["result"])
        # Date and time of the screw run
        self.date = str(json_dict["date"])
        # Identifier code that corresponds to the workpiece data matrix code (DMC)
        self.code = str(json_dict["id code"])
        # Get screw steps as list of ScrewStrep, if they are in the list of steps provided
        self.screw_steps = [
            ScrewStep(step)
            for i, step in enumerate(json_dict["tightening steps"])
            if (i + 1) in self.steps
        ]

        # Get time series data of all steps of the screw run
        # self.time_values = self.get_run_values("time values")
        # self.angle_values = self.get_run_values("angle values")
        # self.torque_values = self.get_run_values("torque values")
        # self.gradient_values = self.get_run_values("gradient values")

        # More attributes can be loaded as well, but they contain to required information
        if False:
            # For the sake of documentation, however most values are simply constant

            # Format of the data
            self.format = str(json_dict["format"])  # "channel"
            # Node identifier
            self.node_id = float(json_dict["node id"])  # "0.1"
            # Numeric identifier
            self.nr = int(json_dict["nr"])  # "1"
            # Hardware identifier
            self.hardware = str(json_dict["hardware"])  # "CS351"
            # MAC address
            self.mac0 = str(json_dict["mac0"])  # "00-C0-3A-6E-9c-8e"
            # IP address
            self.ip0 = str(json_dict["ip0"])  # "129.217.174.137"
            # Software version of BS350
            self.sw_version = str(json_dict["sw version"])  # "2.500"
            # Software build identifier
            self.sw_build = str(json_dict["sw build"])  # "SP1"
            # Factor related to MCE (Machine Control Element)
            self.mce_factor = str(json_dict["MCE factor"])  # 1
            # Dict of MCE information (accessed via list)
            self.mce = dict(json_dict["MCE"][0])
            # Transducer function
            self.transducer_function = self.mce["Transducer function"]  # "primary"
            # Measurement method
            self.measuring = self.mce["measuring"]  # "direct"
            # Factor value
            self.factor_value = self.mce["factor"]  # "1"
            # Maximum speed
            self.max_speed = str(json_dict["max. speed"])
            # List of location names
            self.location_name = str(json_dict["location name"])
            # Channel information
            self.channel = str(json_dict["channel"])
            # Program number
            self.prg_nr = int(json_dict["prg nr"])
            # Program name
            self.prg_name = str(json_dict["prg name"])  # "SMW_4step"
            # Program date
            self.prg_date = str(json_dict["prg date"])  # "2022-08-19 15:48:16"
            # Cycle identifier
            self.cycle = str(json_dict["cycle"])
            # Redundancy sensor information
            self.redundancy_sensor = str(json_dict["redundancy sensor"])
            # Nominal torque value
            self.nominal_torque = str(json_dict["nominal torque"])
            # Torque unit
            self.torque_unit = str(json_dict["torque unit"])  # "Nm"
            # # Last command
            self.last_cmd = str(json_dict["last cmd"])
            # Last step row
            self.last_step_row = str(json_dict["last step row"])
            # Last step column
            self.last_step_column = str(json_dict["last step column"])
            # Quality code
            self.quality_code = str(json_dict["quality code"])
            # Total time duration
            self.total_time = str(json_dict["total time"])
            # Tool serial number
            self.tool_serial = str(json_dict["tool serial"])  # "955000040"
            # Redundancy transducer serial number
            self.rds = str(json_dict["redundancy transducer serial"])  # "2147483648"
            # Spindle identifier
            self.spindle_id = str(json_dict["spindle id"])
            # Rework code
            self.rework_code = int(json_dict["rework code"])
            # Rework text
            self.rework_text = str(json_dict["rework text"])
            # Batch number
            self.batch_nr = int(json_dict["batch nr"])
            # Batch canceled information
            self.batch_cancled = int(json_dict["batch canceled"])
            # Batch direction OK information
            self.batch_direction_ok = int(json_dict["batch direction OK"])
            # Batch direction NOK information
            self.batch_direction_nok = str(json_dict["batch direction NOK"])
            # Batch maximum OK information
            self.batch_max_ok = str(json_dict["batch max OK"])
            # Batch OK information
            self.batch_ok = str(json_dict["batch OK"])
            # Batch maximum NOK information
            self.batch_max_nok = str(json_dict["batch max NOK"])
            # Batch NOK information
            self.batch_nok = str(json_dict["batch NOK"])
            # Angle global threshold information
            self.agt = dict(json_dict["angle global threshold"])
            # Nominal value
            self.agt_nom = self.agt["nom"]
            # Actual value
            self.agt_act = self.agt["act"]
            # Torque CT value
            self.torque_ct = str(json_dict["Torque CT"])
            # Torque credibility value
            self.torque_cred = str(json_dict["Torque Cred"])

    def get_json_as_dict(self) -> Union[Dict[str, Any], None]:
        """Loads the JSON data to a dict from the specified file."""

        # Get file path to screw run as json file
        json_file_path = os.path.join(self.path, self.name)

        try:  # Return the json file as dict
            with open(json_file_path, "r") as json_file:
                return json.load(json_file)

        # Raise the corresponding error
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"JSON file not found ({json_file_path}): {e}",
            ) from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Error decoding JSON file ({json_file_path}): {e}",
            ) from e

    def get_dmc(self) -> str:
        """Returns the data matrix code, a unique work piece identifier, for the screw run."""
        return self.code

    def get_result(self) -> str:
        """Returns a binary value ["OK", "NOK"] that was set by the tightening control for the screw run."""
        return self.result

    def get_run_values(self, value: str) -> List[float]:
        """Returns a flattened list of values for all screw steps in self.screw_steps."""
        return list(
            chain.from_iterable(step.get_values(value) for step in self.screw_steps)
        )
