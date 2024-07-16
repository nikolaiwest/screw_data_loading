import json
import os
import sqlite3

from tqdm import tqdm


def execute_script_from_file(filename, connection):
    with open(filename, "r") as file:
        script = file.read()
    cursor = connection.cursor()
    cursor.executescript(script)
    cursor.close()


def insert_screw_run(cursor, screw_run_data, file_id):
    """Insert a screw run into the screw_runs table."""
    insert_query = """
    INSERT INTO screw_runs (
        id, 
        format, 
        node_id, 
        nr, 
        result, 
        hardware, 
        mac0, 
        ip0, 
        sw_version, 
        sw_build,
        MCE_transducer_function, 
        MCE_measuring, 
        MCE_factor, 
        max_speed, 
        location_name, 
        channel,
        prg_nr, 
        prg_name, 
        prg_date, 
        cycle, 
        redundancy_sensor, 
        nominal_torque, 
        date, 
        id_code, 
        torque_unit,
        last_cmd, 
        last_step_row, 
        last_step_column, 
        quality_code, 
        total_time, 
        tool_serial,
        redundancy_transducer_serial, 
        spindle_id, 
        rework_code, 
        rework_text, 
        batch_nr, 
        batch_canceled,
        batch_direction_ok, 
        batch_direction_nok, 
        batch_max_ok, 
        batch_ok,
        batch_max_nok, 
        batch_nok,
        angle_global_threshold_nom, 
        angle_global_threshold_act, 
        torque_ct, 
        torque_cred
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?
        );
    """
    values = (
        # Unique identifier for the screw run, derived from the filename
        file_id,
        # Defines the origin of the tightening data
        screw_run_data.get("format"),
        # Node ID of the system
        screw_run_data.get("node id"),
        # Sequence number or identifier
        screw_run_data.get("nr"),
        # Result of the tightening process (OK/NOK)
        screw_run_data.get("result"),
        # Hardware identifier
        screw_run_data.get("hardware"),
        # MAC address of the device
        screw_run_data.get("mac0"),
        # IP address of the device
        screw_run_data.get("ip0"),
        # Software version of the device
        screw_run_data.get("sw version"),
        # Software build identifier
        screw_run_data.get("sw build"),
        # MCE transducer function
        screw_run_data.get("MCE", [{}])[0].get("Transducer function"),
        # MCE measuring method
        screw_run_data.get("MCE", [{}])[0].get("measuring"),
        # MCE factor
        screw_run_data.get("MCE", [{}])[0].get("factor"),
        # Maximum speed of the screw run
        screw_run_data.get("max. speed"),
        # Location names where the process was executed (list)
        json.dumps(screw_run_data.get("location name")),
        # Channel information
        screw_run_data.get("channel"),
        # Program number
        screw_run_data.get("prg nr"),
        # Program name
        screw_run_data.get("prg name"),
        # Date when the program was executed
        screw_run_data.get("prg date"),
        # Cycle count
        screw_run_data.get("cycle"),
        # Redundancy sensor information
        screw_run_data.get("redundancy sensor"),
        # Nominal torque values
        screw_run_data.get("nominal torque"),
        # Date of the screw run
        screw_run_data.get("date"),
        # Identification code
        screw_run_data.get("id code"),
        # Unit of torque measurement
        screw_run_data.get("torque unit"),
        # Last command executed
        screw_run_data.get("last cmd"),
        # Last step row identifier
        screw_run_data.get("last step row"),
        # Last step column identifier
        screw_run_data.get("last step column"),
        # Quality code of the process
        screw_run_data.get("quality code"),
        # Total time taken for the process
        screw_run_data.get("total time"),
        # Serial number of the tool used
        screw_run_data.get("tool serial"),
        # Redundancy transducer serial number
        screw_run_data.get("redundancy transducer serial"),
        # Spindle identifier
        screw_run_data.get("spindle id"),
        # Rework code if any
        screw_run_data.get("rework code"),
        # Textual description of rework
        screw_run_data.get("rework text"),
        # Batch number
        screw_run_data.get("batch nr"),
        # Indicator if batch was canceled
        screw_run_data.get("batch canceled"),
        # Batch direction OK count
        screw_run_data.get("batch direction OK"),
        # Batch direction NOK count
        screw_run_data.get("batch direction NOK"),
        # Maximum OK batch count
        screw_run_data.get("batch max OK"),
        # Total OK batch count
        screw_run_data.get("batch OK"),
        # Maximum NOK batch count
        screw_run_data.get("batch max NOK"),
        # Total NOK batch count
        screw_run_data.get("batch NOK"),
        # Nominal angle global threshold
        screw_run_data.get("angle global threshold", {}).get("nom"),
        # Actual angle global threshold
        screw_run_data.get("angle global threshold", {}).get("act"),
        # Torque CT value
        screw_run_data.get("Torque CT"),
        # Torque Cred value
        screw_run_data.get("Torque Cred"),
    )
    try:
        cursor.execute(insert_query, values)
    except sqlite3.Error as e:
        print(f"An error occurred while inserting screw run data: {e}")
    return file_id


def insert_screw_steps(cursor, screw_run_id, steps):
    """Insert all steps of a screw run into the screw_steps table."""
    insert_query = """
    INSERT INTO screw_steps (
        id,
        screw_run_id, 
        step_number,
        step_type, 
        row, 
        column, 
        name, 
        last_cmd, 
        quality_code, 
        speed,
        category, 
        docu_buffer, 
        result, 
        angle_threshold_nom, 
        angle_threshold_act, 
        tightening_functions,
        torsion_release, 
        angle_values, 
        torque_values, 
        gradient_values, 
        torquered_values, 
        anglered_values, 
        time_values
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?);
    """
    values = []
    for step_number, step in enumerate(steps, start=1):
        values.append(
            (
                # Auto-incremented unique ID
                None,
                # Foreign key linking to the screw_run
                screw_run_id,
                # Step number (1, 2, 3, or 4)
                step_number,
                # Type of the step (e.g., standard)
                step.get("step type"),
                # Row number of the step
                step.get("row"),
                # Column identifier of the step
                step.get("column"),
                # Name of the step
                step.get("name"),
                # Last command executed in the step
                step.get("last cmd"),
                # Quality code of the step
                step.get("quality code"),
                # Speed during the step
                step.get("speed"),
                # Category of the step
                step.get("category"),
                # Documentation buffer
                step.get("docu buffer"),
                # Result of the step (OK/NOK)
                step.get("result"),
                # Nominal angle threshold
                step.get("angle threshold", {}).get("nom"),
                # Actual angle threshold
                step.get("angle threshold", {}).get("act"),
                # Nominal value of the tightening function torque
                json.dumps(step.get("tightening functions", [{}])),
                # Torsion release value if available
                step.get("graph", {}).get("torsion release"),
                # List of angle values in the graph
                json.dumps(step.get("graph", {}).get("angle values")),
                # List of torque values in the graph
                json.dumps(step.get("graph", {}).get("torque values")),
                # List of gradient values in the graph
                json.dumps(step.get("graph", {}).get("gradient values")),
                # List of reduced torque values in the graph
                json.dumps(step.get("graph", {}).get("torqueRed values")),
                # List of reduced angle values in the graph
                json.dumps(step.get("graph", {}).get("angleRed values")),
                # List of time values in the graph
                json.dumps(step.get("graph", {}).get("time values")),
            )
        )
    try:
        cursor.executemany(insert_query, values)
    except sqlite3.Error as e:
        print(f"An error occurred while inserting screw step data: {e}")


def main():
    """
    Main function to create databases, read JSON files, and insert data into SQLite database.
    - Note: Addint the raw json as text to the db adds approx. 0.5 GB per 10K observations.
    """
    # Default path
    database_path = "databases/screw_data.db"

    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)

        # Execute SQL scripts to create tables
        execute_script_from_file("databases/create/create_screw_runs.sql", conn)
        execute_script_from_file("databases/create/create_screw_steps.sql", conn)

        conn.commit()
        conn.close()
    else:
        print(f"Database {database_path} already exists. Skipping creation.")

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    json_files_path = "data/raw"
    if not os.path.exists(json_files_path):
        print(f"JSON files path {json_files_path} does not exist.")
        return

    for json_file in tqdm(os.listdir(json_files_path)):
        if json_file.endswith(".json"):
            # Use the filename without extension as the ID
            file_id = os.path.splitext(json_file)[0]
            with open(os.path.join(json_files_path, json_file), "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"An error occurred while reading {json_file}: {e}")
                    continue
                insert_screw_run(cursor, data, file_id)
                insert_screw_steps(cursor, file_id, data.get("tightening steps", []))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
