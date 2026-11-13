# Predictive Maintenance System

## Project Overview

The Predictive Maintenance System is a machine learning-based application that analyzes industrial sensor readings to identify abnormal machine operating conditions.

The system uses a Random Forest classification model to classify sensor readings as **Normal** or **Abnormal**. It integrates Python, MySQL, and Streamlit to provide data processing, prediction storage, and an interactive monitoring dashboard.

## Objectives

- Generate and manage industrial machine and sensor data.
- Analyze sensor readings to identify abnormal conditions.
- Train a machine learning model to classify sensor readings.
- Store machine information, telemetry data, and predictions in MySQL.
- Display monitoring statistics and predictions through a Streamlit dashboard.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas, NumPy | Data processing |
| Scikit-learn | Machine learning |
| Random Forest | Classification model |
| MySQL | Database management |
| Streamlit | Interactive dashboard |
| Matplotlib | Data visualization |
| Joblib | Model persistence |
| Python-dotenv | Environment configuration |

## Project Structure

```text
predictive_maintenance/
│
├── analysis/
│   ├── prepare_data.py
│   ├── split_data.py
│   ├── encode_data.py
│   ├── train_model.py
│   ├── predict.py
│   └── exploratory_data_analysis.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── ground_truth/
│
├── database/
│   ├── predictive_maintenance_schema.sql
│   ├── import_master_data.py
│   └── save_predictions.py
│
├── documentation/
│
├── generator/
│   ├── generate_master_data.py
│   └── generate_sensor_data.py
│
├── models/
│   └── random_forest_model.pkl
│
├── validation/
│   └── validate_sensor_data.py
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd predictive_maintenance
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

- Install and start MySQL Server.
- Open MySQL Workbench.
- Execute `database/predictive_maintenance_schema.sql`.
- Create a `.env` file in the project root.

Example `.env` configuration:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=1980
DB_NAME=predictive_maintenance_db
```

Replace the password with your own MySQL password. Never upload `.env` to GitHub.

## Running the Project

Run commands from the project root directory.

### Step 1: Generate master data

```bash
python generator/generate_master_data.py
```

### Step 2: Generate sensor readings

```bash
python generator/generate_sensor_data.py
```

### Step 3: Validate sensor data

```bash
python validation/validate_sensor_data.py
```

### Step 4: Prepare the dataset

```bash
python analysis/prepare_data.py
```

### Step 5: Split the dataset

```bash
python analysis/split_data.py
```

### Step 6: Encode categorical features

```bash
python analysis/encode_data.py
```

### Step 7: Train the model

```bash
python analysis/train_model.py
```

### Step 8: Import data into MySQL

```bash
python database/import_master_data.py
```

### Step 9: Save predictions in MySQL

```bash
python database/save_predictions.py
```

### Step 10: Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Open the local URL displayed in the terminal.

## Machine Learning Model

The project uses a Random Forest Classifier.

**Input features:**
- Sensor type
- Sensor reading value

**Output classes:**
- Normal
- Abnormal

The categorical sensor type is converted into numerical features using one-hot encoding.

### Model Evaluation

The current model evaluation produced:

| Metric | Result |
|---|---:|
| Training records | 8,000 |
| Testing records | 2,000 |
| Accuracy | 99.9% |
| Abnormal true positives | 94 |
| Abnormal false negatives | 2 |
| Normal true negatives | 1,904 |
| Normal false positives | 0 |

These results are from a synthetic dataset and should not be interpreted as proof of real-world failure prediction accuracy.

## Database

The MySQL database is named `predictive_maintenance_db`.

It contains 15 tables covering:

- Plants and production lines
- Machines and sensors
- Operating shifts, technicians, and parts
- Telemetry readings
- Failure events and maintenance work orders
- Work order history and data quality issues
- Machine status history
- Machine predictions

## Testing and Verification

The project includes sensor data validation and machine learning evaluation.

Current verification results:

- 10,000 sensor readings generated.
- No missing records detected during validation.
- No duplicate reading IDs detected.
- No invalid sensor types or condition labels detected.
- 10,000 telemetry records stored in MySQL.
- 10,000 corresponding predictions stored in MySQL.
- No unpredicted telemetry records in the verified database.

## Limitations and Future Improvements

- The current dataset is synthetic rather than collected from real industrial machines.
- Abnormal labels are generated using predefined sensor thresholds.
- Random train-test splitting can place readings from the same sensor in both datasets.
- The current model does not establish actual future failure probability.
- Future versions can incorporate real machine failure records, time-series forecasting, and machine-level evaluation.


## Author

Developed as a Python, Machine Learning, and MySQL project.
