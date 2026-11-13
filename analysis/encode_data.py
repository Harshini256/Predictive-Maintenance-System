
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder

# Find project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Input and output folders
DATA_FOLDER = PROJECT_ROOT / "data" / "processed"


def encode_data():

    print("Starting One-Hot Encoding...")

    # Read training and testing input data
    X_train = pd.read_csv(DATA_FOLDER / "X_train.csv")
    X_test = pd.read_csv(DATA_FOLDER / "X_test.csv")

    # Create encoder
    encoder = OneHotEncoder(handle_unknown="ignore")

    # Learn categories from training data and encode it
    train_sensor = encoder.fit_transform(X_train[["sensor_type"]])

    # Encode testing data using the same encoder
    test_sensor = encoder.transform(X_test[["sensor_type"]])

    # Get the generated column names
    column_names = encoder.get_feature_names_out(["sensor_type"])

    # Convert encoded data into DataFrames
    train_encoded = pd.DataFrame(
        train_sensor.toarray(),
        columns=column_names
    )

    test_encoded = pd.DataFrame(
        test_sensor.toarray(),
        columns=column_names
    )

    # Add reading_value to both datasets
    train_encoded["reading_value"] = X_train["reading_value"].values
    test_encoded["reading_value"] = X_test["reading_value"].values

    # Save encoded datasets
    train_encoded.to_csv(
        DATA_FOLDER / "X_train_encoded.csv",
        index=False
    )

    test_encoded.to_csv(
        DATA_FOLDER / "X_test_encoded.csv",
        index=False
    )

    # Display results
    print("\nEncoded training data:")
    print(train_encoded.head())

    print("\nTraining data shape:", train_encoded.shape)
    print("Testing data shape:", test_encoded.shape)

    print("\nGenerated columns:")
    print(list(train_encoded.columns))

    print("\nOne-Hot Encoding completed successfully!")


if __name__ == "__main__":
    encode_data()
