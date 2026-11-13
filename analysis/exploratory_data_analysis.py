
import pandas as pd
import matplotlib

# Use a non-interactive backend to save graphs without opening windows
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Location of sensor readings CSV file
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "SensorReadings.csv"

# Folder to save graphs
OUTPUT_FOLDER = PROJECT_ROOT / "analysis"


# Main EDA function
def perform_eda():

    print("Starting Exploratory Data Analysis...\n")

    # Check whether the CSV file exists
    if not DATA_FILE.exists():
        print("ERROR: SensorReadings.csv not found!")
        return

    # Read CSV data using Pandas
    df = pd.read_csv(DATA_FILE)

    # Convert timestamp column into datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Display total records
    print("Total number of readings:", len(df))

    # Display first five records
    print("\nFirst 5 records:")
    print(df.head())

    # Display dataset information
    print("\nDataset information:")
    df.info()

    # Statistical summary
    print("\nStatistical summary:")
    print(df["reading_value"].describe())

    # Count sensor conditions
    print("\nSensor condition distribution:")
    condition_counts = df["condition"].value_counts()
    print(condition_counts)

    # Count normal and abnormal readings
    normal_count = (df["failure_label"] == 0).sum()
    abnormal_count = (df["failure_label"] == 1).sum()

    print("\nNormal readings:", normal_count)
    print("Abnormal readings:", abnormal_count)

    # Calculate average reading for each sensor type
    print("\nAverage reading by sensor type:")

    average_readings = (
        df.groupby("sensor_type")["reading_value"].mean()
    )

    print(average_readings.round(2))


    # Sensor-wise abnormal reading analysis
    print("\nAbnormal readings by sensor type:")

    # Select only abnormal readings
    abnormal_data = df[df["failure_label"] == 1]

    # Count total readings for each sensor type
    total_by_sensor = df.groupby("sensor_type").size()

    # Count abnormal readings for each sensor type
    abnormal_by_sensor = abnormal_data.groupby("sensor_type").size()

    # Create a summary table
    abnormal_summary = pd.DataFrame({
        "Total Readings": total_by_sensor,
        "Abnormal Readings": abnormal_by_sensor
    })

    # Calculate abnormal percentage
    abnormal_summary["Abnormal Percentage"] = (
        abnormal_summary["Abnormal Readings"]
        / abnormal_summary["Total Readings"] * 100
    )

    print(abnormal_summary.round(2))

    # Graph 3: Abnormal readings by sensor type
    plt.figure(figsize=(8, 5))

    abnormal_by_sensor.plot(kind="bar")

    plt.title("Abnormal Readings by Sensor Type")
    plt.xlabel("Sensor Type")
    plt.ylabel("Number of Abnormal Readings")
    plt.xticks(rotation=0)
    plt.tight_layout()

    graph3 = OUTPUT_FOLDER / "abnormal_by_sensor.png"

    plt.savefig(graph3)
    plt.close()

    print("\nGraph saved:", graph3)


    # Create output folder if it does not exist
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Graph 1: Sensor condition distribution
    plt.figure(figsize=(8, 5))

    condition_counts.plot(kind="bar")

    plt.title("Sensor Condition Distribution")
    plt.xlabel("Condition")
    plt.ylabel("Number of Readings")
    plt.xticks(rotation=0)
    plt.tight_layout()

    graph1 = OUTPUT_FOLDER / "condition_distribution.png"

    plt.savefig(graph1)
    plt.close()

    print("\nGraph saved:", graph1)

    # Graph 2: Average reading by sensor type
    plt.figure(figsize=(8, 5))

    average_readings.plot(kind="bar")

    plt.title("Average Reading by Sensor Type")
    plt.xlabel("Sensor Type")
    plt.ylabel("Average Reading")
    plt.xticks(rotation=0)
    plt.tight_layout()

    graph2 = OUTPUT_FOLDER / "average_readings.png"

    plt.savefig(graph2)
    plt.close()

    print("Graph saved:", graph2)


    # Hourly abnormal reading analysis
    print("\nHourly abnormal reading analysis:")

    # Group readings by timestamp and count abnormal readings
    hourly_abnormal = (
        df.groupby("timestamp")["failure_label"].sum()
    )

    print(hourly_abnormal)

    # Graph 4: Hourly abnormal readings
    plt.figure(figsize=(10, 5))

    hourly_abnormal.plot(kind="line", marker="o")

    plt.title("Hourly Abnormal Sensor Readings")
    plt.xlabel("Time")
    plt.ylabel("Number of Abnormal Readings")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    graph4 = OUTPUT_FOLDER / "hourly_abnormal_readings.png"

    plt.savefig(graph4)
    plt.close()

    print("\nGraph saved:", graph4)


    print("\nEDA completed successfully!")


# Starting point of the program
if __name__ == "__main__":
    perform_eda()
