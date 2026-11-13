
import pandas as pd
import joblib
import mysql.connector

from pathlib import Path

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


# Find project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Model location
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.pkl"


def get_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    return connection


def fetch_unpredicted_readings():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            t.telemetry_id,
            t.sensor_id,
            s.sensor_type,
            t.reading_value
        FROM TelemetryEvent t
        JOIN Sensor s
            ON t.sensor_id = s.sensor_id
        LEFT JOIN Prediction p
            ON t.telemetry_id = p.telemetry_id
        WHERE p.telemetry_id IS NULL
    """

    cursor.execute(query)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    df = pd.DataFrame(records)

    if not df.empty:
        # Convert uppercase sensor types to training format
        df["sensor_type"] = df["sensor_type"].str.capitalize()

    print("Total unpredicted readings:", len(df))

    return df


def generate_predictions(df):

    if df.empty:
        print("No new readings available for prediction.")
        return pd.DataFrame()

    # Load the trained Random Forest model
    model = joblib.load(MODEL_PATH)

    # Prepare input data
    new_data = df[["sensor_type", "reading_value"]].copy()

    # Apply the same encoding used during training
    encoded_data = pd.get_dummies(
        new_data,
        columns=["sensor_type"]
    )

    # Match the exact training columns
    encoded_data = encoded_data.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    # Predict NORMAL or ABNORMAL
    predictions = model.predict(encoded_data)

    # Calculate abnormal probabilities
    abnormal_index = list(model.classes_).index(1)

    probabilities = model.predict_proba(encoded_data)[
        :, abnormal_index
    ]

    # Prepare prediction results
    results = df[
        ["telemetry_id", "sensor_id", "reading_value"]
    ].copy()

    results["predicted_label"] = [
        "ABNORMAL" if prediction == 1 else "NORMAL"
        for prediction in predictions
    ]

    results["abnormal_probability"] = (
        probabilities * 100
    ).round(2)

    print("Predictions generated successfully!")
    print(results["predicted_label"].value_counts())

    return results


def save_predictions(results):

    if results.empty:
        print("No predictions to save.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Prediction
        (telemetry_id, sensor_id, reading_value,
         predicted_label, abnormal_probability)
        VALUES (%s, %s, %s, %s, %s)
    """

    records = [
        (
            row.telemetry_id,
            row.sensor_id,
            row.reading_value,
            row.predicted_label,
            row.abnormal_probability
        )
        for row in results.itertuples(index=False)
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Predictions saved successfully!")
    print("Total predictions saved:", cursor.rowcount)

    cursor.close()
    connection.close()


def main():

    print("PREDICTIVE MAINTENANCE SYSTEM")
    print("-----------------------------")

    # Step 1: Fetch readings from MySQL
    df = fetch_unpredicted_readings()

    # Step 2: Generate ML predictions
    results = generate_predictions(df)

    # Step 3: Save predictions into MySQL
    save_predictions(results)

    print("\nPrediction process completed!")


if __name__ == "__main__":
    main()

