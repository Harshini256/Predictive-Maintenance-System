
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

# Keep data reproducible
random.seed(20261022)

# Find project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "data" / "raw"


# Read sensor information
def load_sensors():

    file_path = RAW_DATA / "Sensor.csv"

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


# Generate one sensor reading
def generate_reading(sensor_type):

    ranges = {
        "Temperature": (40, 75, 90, 110),
        "Vibration": (0.5, 4, 7, 10),
        "Pressure": (3, 8, 10, 13),
        "Humidity": (30, 70, 85, 100),
        "Current": (5, 20, 25, 35)
    }

    low, normal_max, warning_max, critical_max = ranges[sensor_type]

    if random.random() < 0.05:

        if random.random() < 0.7:
            value = random.uniform(normal_max, warning_max)
        else:
            value = random.uniform(warning_max, critical_max)

    else:
        value = random.uniform(low, normal_max)

    if value <= normal_max:
        condition = "Normal"
        failure_label = 0

    elif value <= warning_max:
        condition = "Warning"
        failure_label = 1

    else:
        condition = "Critical"
        failure_label = 1

    return round(value, 2), condition, failure_label


# Generate sensor readings
def generate_sensor_data(sensors):

    records = []

    start_time = datetime(2026, 11, 1, 6, 0, 0)

    reading_id = 1

    for hour in range(20):

        current_time = start_time + timedelta(hours=hour)

        for sensor in sensors:

            value, condition, failure_label = generate_reading(
                sensor["sensor_type"]
            )

            records.append({
                "reading_id": reading_id,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "sensor_id": sensor["sensor_id"],
                "machine_id": sensor["machine_id"],
                "sensor_type": sensor["sensor_type"],
                "reading_value": value,
                "unit": sensor["unit"],
                "condition": condition,
                "failure_label": failure_label
            })

            reading_id += 1

    return records


# Save readings into CSV
def save_readings(records):

    file_path = RAW_DATA / "SensorReadings.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        fieldnames = records[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(records)

    print("SensorReadings.csv created successfully!")


# Main function
def main():

    print("Generating sensor readings...")

    sensors = load_sensors()

    records = generate_sensor_data(sensors)

    save_readings(records)

    print("Total sensor readings:", len(records))
    print("Sensor data generation completed!")


if __name__ == "__main__":
    main()
