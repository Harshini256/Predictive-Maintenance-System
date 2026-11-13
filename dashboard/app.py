

import streamlit as st
import pandas as pd
import joblib
import mysql.connector
import sys
from decimal import Decimal
from pathlib import Path

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add the main project folder to Python's search path
sys.path.insert(0, str(PROJECT_ROOT))

# Import database settings
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Model location
MODEL_FILE = PROJECT_ROOT / "models" / "random_forest_model.pkl"



# Page configuration
st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="⚙️",
    layout="wide"
)


# Database connection
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# Execute SELECT queries and return results as a DataFrame

def fetch_data(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        records = cursor.fetchall()

        df = pd.DataFrame(records)

        # Convert MySQL Decimal values into Python float values
        for column in df.columns:
            df[column] = df[column].apply(
                lambda value: float(value)
                if isinstance(value, Decimal)
                else value
            )

        return df

    finally:
        cursor.close()
        connection.close()



# Load machine learning model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


# Dashboard title
st.title("⚙️ Predictive Maintenance System")

st.write(
    "Monitor machine sensor readings and identify abnormal conditions "
    "using Machine Learning."
)


# Load model
model = load_model()


# Dashboard overview
st.header("Dashboard Overview")

try:
    plant_count = fetch_data("SELECT COUNT(*) AS total FROM Plant").iloc[0]["total"]
    line_count = fetch_data("SELECT COUNT(*) AS total FROM ProductionLine").iloc[0]["total"]
    machine_count = fetch_data("SELECT COUNT(*) AS total FROM Machine").iloc[0]["total"]
    sensor_count = fetch_data("SELECT COUNT(*) AS total FROM Sensor").iloc[0]["total"]

    reading_count = fetch_data(
        "SELECT COUNT(*) AS total FROM TelemetryEvent"
    ).iloc[0]["total"]

    prediction_count = fetch_data(
        "SELECT COUNT(*) AS total FROM Prediction"
    ).iloc[0]["total"]

    prediction_summary = fetch_data("""
        SELECT predicted_label, COUNT(*) AS total
        FROM Prediction
        GROUP BY predicted_label
    """)

except Exception as error:
    st.error("Unable to connect to MySQL or read dashboard data.")
    st.code(str(error))
    st.stop()


# Get normal and abnormal counts
normal_count = 0
abnormal_count = 0

for _, row in prediction_summary.iterrows():
    if row["predicted_label"] == "NORMAL":
        normal_count = int(row["total"])
    elif row["predicted_label"] == "ABNORMAL":
        abnormal_count = int(row["total"])


# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Plants", plant_count)
col2.metric("Production Lines", line_count)
col3.metric("Machines", machine_count)
col4.metric("Sensors", sensor_count)

col5, col6, col7, col8 = st.columns(4)

col5.metric("Sensor Readings", reading_count)
col6.metric("Predictions", prediction_count)
col7.metric("Normal Predictions", normal_count)
col8.metric("Abnormal Predictions", abnormal_count)


st.divider()


# Prediction analysis
st.header("Prediction Analysis")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Normal vs Abnormal Predictions")

    prediction_chart = pd.DataFrame({
        "Prediction": ["Normal", "Abnormal"],
        "Count": [normal_count, abnormal_count]
    })

    st.bar_chart(
        prediction_chart.set_index("Prediction")
    )


with right_col:
    st.subheader("Abnormal Predictions by Sensor Type")

    abnormal_by_sensor = fetch_data("""
        SELECT
            s.sensor_type,
            COUNT(*) AS total
        FROM Prediction p
        JOIN Sensor s
            ON p.sensor_id = s.sensor_id
        WHERE p.predicted_label = 'ABNORMAL'
        GROUP BY s.sensor_type
        ORDER BY total DESC
    """)

    if not abnormal_by_sensor.empty:
        st.bar_chart(
            abnormal_by_sensor.set_index("sensor_type")
        )
    else:
        st.info("No abnormal predictions available.")


st.divider()


# Latest abnormal readings
st.header("Latest Abnormal Readings")

latest_abnormal = fetch_data("""
    SELECT
        p.prediction_id,
        p.telemetry_id,
        p.sensor_id,
        s.sensor_type,
        p.reading_value,
        p.abnormal_probability,
        p.predicted_at
    FROM Prediction p
    JOIN Sensor s
        ON p.sensor_id = s.sensor_id
    WHERE p.predicted_label = 'ABNORMAL'
    ORDER BY p.predicted_at DESC
    LIMIT 20
""")

if not latest_abnormal.empty:
    st.dataframe(latest_abnormal, width="stretch")
else:
    st.info("No abnormal readings found.")


st.divider()


# Interactive sensor monitoring
st.header("Interactive Sensor Monitoring")

sensor_list = fetch_data("""
    SELECT sensor_id, sensor_type
    FROM Sensor
    ORDER BY sensor_id
""")

if not sensor_list.empty:

    selected_sensor = st.selectbox(
        "Select a Sensor",
        sensor_list["sensor_id"].tolist()
    )

    sensor_readings = fetch_data("""
        SELECT
            t.telemetry_id,
            t.recorded_at,
            t.sensor_id,
            s.sensor_type,
            t.reading_value,
            p.predicted_label,
            p.abnormal_probability
        FROM TelemetryEvent t
        JOIN Sensor s
            ON t.sensor_id = s.sensor_id
        LEFT JOIN Prediction p
            ON t.telemetry_id = p.telemetry_id
        WHERE t.sensor_id = %s
        ORDER BY t.recorded_at DESC
        LIMIT 20
    """, (selected_sensor,))

    st.subheader("Recent Readings")

    if not sensor_readings.empty:

        st.dataframe(sensor_readings, width="stretch")

        chart_data = sensor_readings.sort_values("recorded_at")

        st.subheader("Sensor Reading Trend")

        st.line_chart(
            chart_data.set_index("recorded_at")["reading_value"]
        )

    else:
        st.info("No readings available for this sensor.")

else:
    st.info("No sensors available in the database.")


st.divider()


# Manual machine learning prediction
st.header("Predict New Sensor Reading")

st.write(
    "Enter sensor information to predict whether the reading is normal or abnormal."
)

sensor_type = st.selectbox(
    "Select Sensor Type",
    ["Temperature", "Vibration", "Pressure", "Humidity", "Current"],
    key="manual_sensor_type"
)

reading_value = st.number_input(
    "Enter Sensor Reading Value",
    value=55.0,
    step=1.0
)


if st.button("Predict Condition"):

    new_data = pd.DataFrame({
        "sensor_type": [sensor_type],
        "reading_value": [reading_value]
    })

    encoded_data = pd.get_dummies(
        new_data,
        columns=["sensor_type"]
    )

    encoded_data = encoded_data.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    prediction = model.predict(encoded_data)[0]

    abnormal_index = list(model.classes_).index(1)

    probability = model.predict_proba(encoded_data)[0][abnormal_index]

    st.subheader("Prediction Result")

    if prediction == 0:
        st.success("NORMAL - No abnormal reading detected.")
    else:
        st.error("ABNORMAL - Abnormal sensor reading detected!")

    st.metric(
        "Abnormal Prediction Probability",
        f"{probability * 100:.2f}%"
    )

    st.caption(
        "This probability comes from a model trained using synthetic "
        "sensor data. It is not a validated real-world failure probability."
    )


st.divider()

st.caption(
    "Predictive Maintenance System | Machine Learning Project"
)
