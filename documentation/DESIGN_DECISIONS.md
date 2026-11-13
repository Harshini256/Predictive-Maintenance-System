# Design Decisions – Predictive Maintenance System

## 1. Problem Statement

Industrial machines produce sensor readings such as temperature, vibration, pressure, humidity, and current. Unusual readings can indicate abnormal operating conditions.

The objective of this project is to build a system that processes sensor readings, classifies them as Normal or Abnormal, stores predictions in MySQL, and displays the results through an interactive dashboard.

## 2. Project Scope and Assumptions

- The project uses generated sample data for demonstration.
- Each machine has multiple sensors.
- Sensor readings are used as input features for classification.
- Abnormal labels are generated using predefined sensor thresholds.
- The model predicts the condition of a reading, not the exact time until a machine failure.
- The generated labels are not actual confirmed industrial failure records.

## 3. Architecture

The project follows this workflow:

1. Generate machine, plant, sensor, and other master data.
2. Generate sensor readings.
3. Validate the generated readings.
4. Prepare and split the dataset.
5. Encode categorical features.
6. Train and evaluate the Random Forest model.
7. Import master data and telemetry readings into MySQL.
8. Generate predictions and store them in MySQL.
9. Display database information and model predictions through Streamlit.

## 4. Technology Choices

### Python

Selected for data generation, preprocessing, validation, model training, and prediction because of its data science libraries.

### MySQL

Selected to store structured information about plants, production lines, machines, sensors, telemetry readings, and predictions.

### Streamlit

Selected to create an interactive dashboard using Python without requiring a separate frontend framework.

### Random Forest Classifier

Selected as the classification algorithm because it can learn relationships between sensor types, numerical readings, and the target classes. It also provides feature importance values.

### One-Hot Encoding

Sensor type is categorical. One-hot encoding converts it into numerical columns that can be used by the machine learning model.

## 5. Important Implementation Decisions

### Synthetic Data

Generated data was used because a real industrial sensor dataset was not available for this implementation.

A fixed random seed was used in the generation process to make sample data generation reproducible.

### Train-Test Split

The dataset was divided into 80% training data and 20% testing data. Stratification was used to preserve the class distribution.

The current split is row-based. Readings from the same sensor may appear in both sets, so the evaluation does not establish performance on completely unseen machines or sensors.

### Model Persistence

The trained model is saved as `models/random_forest_model.pkl` so that prediction scripts and the dashboard can load the trained model without training it every time.

### Database Integration

MySQL stores the telemetry records and their corresponding predictions. A unique constraint on `Prediction.telemetry_id` helps prevent duplicate predictions for the same telemetry record.

## 6. Model Evaluation

The current Random Forest model was evaluated using 2,000 test records.

| Metric | Result |
|---|---:|
| Training records | 8,000 |
| Testing records | 2,000 |
| Accuracy | 99.9% |
| True negatives | 1,904 |
| False positives | 0 |
| True positives | 94 |
| False negatives | 2 |

The model's feature importance output showed that `reading_value` was the most influential feature in the trained model.

These results must be interpreted in the context of the synthetic threshold-based labels. They do not demonstrate real-world predictive maintenance performance.

## 7. Testing and Verification

The following checks were performed:

- Sensor data validation checked record count, missing values, duplicate reading IDs, sensor types, conditions, and labels.
- The validation script reported 10,000 records and no detected validation issues.
- The model training script reported its evaluation metrics and confusion matrix.
- MySQL verification showed 10,000 telemetry records and 10,000 predictions.
- A query checking for telemetry records without predictions returned zero unpredicted records.
- The Streamlit dashboard was launched and confirmed to work.

## 8. Trade-offs

| Decision | Benefit | Trade-off |
|---|---|---|
| Synthetic data | Easy to generate and reproduce | Does not represent all real machine behavior |
| Random Forest | Suitable for tabular classification | Does not model time-series behavior directly |
| MySQL | Structured storage and relationships | Requires database setup and configuration |
| Streamlit | Fast Python dashboard development | Less frontend customization than a dedicated frontend framework |
| Row-based split | Simple evaluation workflow | Can cause sensor-level data leakage |

## 9. Limitations

- The dataset is synthetic.
- Labels are generated from predefined thresholds rather than verified machine failures.
- The model classifies individual readings and does not forecast failure time.
- Random row splitting may result in similar sensor readings appearing in both training and testing data.
- The displayed abnormal probability is a model score and is not a calibrated real-world failure probability.
- The current project has not been validated for use in actual industrial operations.

## 10. Future Improvements

- Use real industrial sensor and failure datasets.
- Evaluate generalization using machine-level or time-based train-test splits.
- Include historical trends and time-series features.
- Add failure forecasting and remaining useful life estimation.
- Calibrate model probabilities using appropriate validation data.
- Add more automated tests and database error handling.
- Deploy the dashboard in a controlled environment.

## 11. Conclusion

The project demonstrates an end-to-end educational workflow combining synthetic data generation, data validation, machine learning, MySQL storage, and an interactive dashboard. The current implementation is a prototype that can be extended using real industrial data and more advanced predictive models.