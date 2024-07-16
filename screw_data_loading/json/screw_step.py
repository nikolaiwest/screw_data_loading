from typing import List, Dict, Union, Any


class ScrewStep:
    def __init__(self, step_dict: Dict[str, Any]) -> None:
        """
        Initialize a ScrewStep object.

        Parameters:
        -----------
        `step_dict (dict):` Dictionary containing all data for the screw step.

        Example:
        --------
        ```
        step_dict = {
            "step type": "standard",
            "row": "2",
            "column": "A",
            "name": "Finding",
            "last cmd": "TF Angle",
            "quality code": "1",
            "speed": 150,
            "category": 0,
            "docu buffer": 0,
            "result": "OK", # binary label "OK or "NOK"
            "angle threshold": {"nom": 0, "act": -0.005000},
            "tightening functions": [
                {"name": "TF Angle","nom": 100, "act": 100.500000, "add": [
                    {"angle threshold": {"nom": 0, "act": -0.005000}}]},
                {"name": "MFs TimeMax",  "nom":5, "act":0.120000},
                {"name": "MF TorqueMin", "nom": 0, "act": 0.243000},
                {"name": "MFs TorqueMax","nom": 1.200000, "act": 0.243000}
            ],
            "graph": {
                "angle values": [0, 0, 0.500000, 1.750000, ..., 98.500000, 99.500000, 100.500000],
                "torque values": [-0.005000, -0.003000, 0.061000, 0.247000 ..., 0.239000, 0.245000, 0.243000],
                "gradient values": [-0.002200, -0.002200, 0.002200, 0.037800 ..., 0.001100, 0.000500, 0.001800],
                "torqueRed values": [0, 0, 0, 0, ..., 0, 0, 0],
                "angleRed values": [0, 0, 0, 0, ..., 0, 0, 0],
                "time values": [0, 0.003600, 0.007200, 0.008400,..., 0.114000, 0.115200, 0.116400]
            }
        }

        screw_step = ScrewStep(step_dict)
        ```

        """
        # Name of the step, e.g. "Finding", "Thread forming", "Pre-tightening" or "Tightening 1.4"
        self.name: str = step_dict.get("name", "")

        # Measured values of the screw run, such as angle, torque gradient or time
        self.values: Dict[str, List[Union[int, float]]] = step_dict.get("graph", {})

        # For sake of documentation, the remaining attributes can be loded as well
        if False:
            # Type of tightening step
            self.step_type = str(step_dict["step type"])  # "standard"
            # Row number
            self.row = int(step_dict["row"])
            # Column letter
            self.column = str(step_dict["column"])
            # Last command executed
            self.last_cmd = str(step_dict["last cmd"])
            # Quality code
            self.quality_code = str(step_dict["quality code"])  # "1"
            # Tightening speed
            self.speed = int(step_dict["speed"])
            # Category of the step
            self.category = int(step_dict["category"])  # "0"
            # Documentation buffer
            self.docu_buffer = int(step_dict["docu buffer"])  # "0"
            # Result of the tightening step
            self.result = str(step_dict["result"])
            # Angle threshold information
            self.angle_threshold = dict(step_dict["angle threshold"])
            # List with dicts of tightening functions
            self.tightening_functions = list(step_dict["tightening functions"])

    def get_values(self, value_type: str) -> List[Union[int, float]]:
        """
        Retrieve specified values from the graph data.

        Parameters:
        -----------
        `value_type (str)`: Type of values to retrieve from the tightening step.

        Returns:
        --------
        `List[Union[int, float]]`:List of values from the specified graph.

        """
        valid_types = [
            "angle values",
            "torque values",
            "gradient values",
            "torqueRed values",
            "angleRed values",
            "time values",
        ]
        if value_type not in valid_types:
            raise ValueError(f"Invalid type for value provided: {value_type}")
        return self.values.get(value_type, [])
