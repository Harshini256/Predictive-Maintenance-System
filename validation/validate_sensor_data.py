
import csv
from pathlib import Path

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Location of sensor readings CSV file
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "SensorReadings.csv"

# Expected sensor types
VALID_SENSOR_TYPES = [
    "Temperature",
    "Vibration",
    "Pressure",
    "Humidity",
    "Current"
]

# Expected condition labels
VALID_CONDITIONS = ["Normal", "Warning", "Critical"]


def validate_sensor_data():

    print("Starting sensor data validation...\n")

    # Check whether the CSV file exists
    if not DATA_FILE.exists():
        print("ERROR: SensorReadings.csv not found!")
        return

    # Read the CSV file
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    print("Total records:", len(records))

    # Counters for validation
    missing_values = 0
    duplicate_ids = 0
    invalid_sensor_types = 0
    invalid_conditions = 0
    invalid_labels = 0

    # Store reading IDs to find duplicates
    reading_ids = set()

    # Required columns
    required_fields = [
        "reading_id",
        "timestamp",
        "sensor_id",
        "machine_id",
        "sensor_type",
        "reading_value",
        "unit",
        "condition",
        "failure_label"
    ]

    # Check every record
    for record in records:

        # Check missing values
        for field in required_fields:
            if not record[field].strip():
                missing_values += 1
                break

        # Check duplicate reading IDs
        reading_id = record["reading_id"]

        if reading_id in reading_ids:
            duplicate_ids += 1
        else:
            reading_ids.add(reading_id)

        # Check sensor type
        if record["sensor_type"] not in VALID_SENSOR_TYPES:
            invalid_sensor_types += 1

        # Check condition
        if record["condition"] not in VALID_CONDITIONS:
            invalid_conditions += 1

        # Check failure label
        if record["failure_label"] not in ["0", "1"]:
            invalid_labels += 1

        # Check condition and failure label consistency
        elif record["condition"] == "Normal" and record["failure_label"] != "0":
            invalid_labels += 1

        elif record["condition"] in ["Warning", "Critical"] and record["failure_label"] != "1":
            invalid_labels += 1

    # Display validation results
    print("\n--- VALIDATION RESULTS ---")

    print("Missing records:", missing_values)
    print("Duplicate reading IDs:", duplicate_ids)
    print("Invalid sensor types:", invalid_sensor_types)
    print("Invalid conditions:", invalid_conditions)
    print("Invalid failure labels:", invalid_labels)

    # Check expected record count
    if len(records) == 10000:
        print("\nRecord count check: PASSED")
    else:
        print("\nRecord count check: FAILED")

    # Final result
    if (
        missing_values == 0
        and duplicate_ids == 0
        and invalid_sensor_types == 0
        and invalid_conditions == 0
        and invalid_labels == 0
        and len(records) == 10000
    ):
        print("\nSUCCESS: Sensor data is valid!")
    else:
        print("\nWARNING: Some data validation issues were found.")


# Starting point of the program
if __name__ == "__main__":
    validate_sensor_data()
