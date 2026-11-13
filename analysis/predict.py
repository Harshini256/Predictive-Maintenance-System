
import pandas as pd
import joblib

from pathlib import Path

# Find project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Saved model location
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.pkl"


def predict_reading():

    print("PREDICTIVE MAINTENANCE SYSTEM")
    print("-----------------------------")

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Get sensor details from user
    sensor_type = input(
        "Enter sensor type (Temperature, Vibration, Pressure, Humidity, Current): "
    ).strip().capitalize()

    if sensor_type not in [
        "Temperature", "Vibration", "Pressure", "Humidity", "Current"
    ]:
        print("Invalid sensor type!")
        return

    try:
        reading_value = float(input("Enter sensor reading value: "))
    except ValueError:
        print("Please enter a valid number!")
        return

    # Create input DataFrame
    new_data = pd.DataFrame({
        "sensor_type": [sensor_type],
        "reading_value": [reading_value]
    })

    # Convert sensor type into numerical columns
    encoded_data = pd.get_dummies(new_data, columns=["sensor_type"])

    # Match the exact training column order
    encoded_data = encoded_data.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    # Make prediction
    prediction = model.predict(encoded_data)[0]

    # Display result
    print("\nPREDICTION RESULT")

    if prediction == 0:
        print("Condition: NORMAL")
        print("No abnormal reading detected.")
    else:
        print("Condition: ABNORMAL")
        print("Abnormal sensor reading detected!")

    # Display abnormal prediction probability
    abnormal_index = list(model.classes_).index(1)
    probability = model.predict_proba(encoded_data)[0][abnormal_index]

    print(
        "Abnormal prediction probability:",
        round(probability * 100, 2), "%"
    )


if __name__ == "__main__":
    predict_reading()
