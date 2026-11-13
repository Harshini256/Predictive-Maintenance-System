
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Prepared dataset
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "model_data.csv"

# Output folder
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"


def split_data():

    print("Starting Train-Test Split...")

    # Read prepared data
    df = pd.read_csv(INPUT_FILE)

    # Input features (X)
    X = df[["sensor_type", "reading_value"]]

    # Target output (y)
    y = df["failure_label"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Save training and testing data
    X_train.to_csv(OUTPUT_FOLDER / "X_train.csv", index=False)
    X_test.to_csv(OUTPUT_FOLDER / "X_test.csv", index=False)

    y_train.to_csv(OUTPUT_FOLDER / "y_train.csv", index=False)
    y_test.to_csv(OUTPUT_FOLDER / "y_test.csv", index=False)

    # Display results
    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))

    print("\nTraining target distribution:")
    print(y_train.value_counts())

    print("\nTesting target distribution:")
    print(y_test.value_counts())

    print("\nTrain-test split completed successfully!")

if __name__ == "__main__":
    split_data()
