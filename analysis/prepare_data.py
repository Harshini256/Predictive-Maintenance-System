
import pandas as pd
from pathlib import Path

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Input file
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "SensorReadings.csv"

# Output folder
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

def prepare_data():

    print("Starting Data Preparation...")

    # Create processed folder if it does not exist
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Read the original dataset
    df = pd.read_csv(INPUT_FILE)

    print("\nOriginal dataset shape:", df.shape)

    # Select required columns
    model_data = df[
        ["sensor_type", "reading_value", "failure_label"]
    ].copy()

    # Check for missing values
    print("\nMissing values:")
    print(model_data.isnull().sum())

    # Remove rows with missing values
    model_data = model_data.dropna()

    # Save prepared dataset
    output_file = OUTPUT_FOLDER / "model_data.csv"
    model_data.to_csv(output_file, index=False)

    print("\nPrepared dataset shape:", model_data.shape)

    print("\nTarget distribution:")
    print(model_data["failure_label"].value_counts())

    print("\nPrepared dataset saved:", output_file)

    print("\nData preparation completed successfully!")


if __name__ == "__main__":
    prepare_data()
