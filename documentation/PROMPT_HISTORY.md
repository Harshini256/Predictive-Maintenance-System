# AI Assistance and Prompt History

## 1. Purpose

AI assistance was used as a development support tool while building the Predictive Maintenance System.

It helped explain concepts, suggest implementation approaches, troubleshoot errors, and review parts of the code. The project was executed and tested by the developer.

## 2. Areas Where AI Assistance Was Used

| Development area | Summary of assistance |
|---|---|
| Project setup | Guidance on organizing Python files and folders |
| Configuration | Explanation of environment variables and database connection settings |
| Data generation | Help understanding master data and sensor reading generation |
| Data validation | Explanation of validation checks and interpreting their results |
| Data preprocessing | Guidance on preparing features and target labels |
| Machine learning | Explanation of train-test splitting, one-hot encoding, and Random Forest |
| Model evaluation | Help interpreting accuracy, classification reports, confusion matrices, and feature importance |
| MySQL integration | Guidance on importing data and storing predictions |
| Streamlit dashboard | Help understanding dashboard components and troubleshooting |
| Documentation | Assistance preparing project documentation and setup instructions |

## 3. Representative Prompt Summaries

The following examples summarize the kinds of prompts used during development:

1. Explain how to organize the Predictive Maintenance System project into folders and Python files.
2. Explain the purpose of each Python script and how the scripts work together.
3. Help configure a Python application to connect to MySQL using environment variables.
4. Explain how to generate machine sensor readings and validate the generated CSV data.
5. Explain data preparation, train-test splitting, and one-hot encoding step by step.
6. Explain how a Random Forest Classifier trains and predicts Normal and Abnormal sensor readings.
7. Help troubleshoot the integration between Python prediction scripts and MySQL tables.
8. Explain how to display prediction counts, abnormal readings, and sensor trends in Streamlit.
9. Help prepare documentation describing project decisions, test results, and limitations.

These are representative summaries rather than a complete verbatim conversation transcript.

## 4. How AI Assistance Was Used

AI assistance was used for:

- Understanding unfamiliar Python and machine learning concepts.
- Getting explanations of code and database operations.
- Identifying possible errors and troubleshooting them.
- Reviewing implementation approaches.
- Improving project documentation.

AI-generated suggestions were treated as guidance, not automatically accepted as correct.

## 5. Developer's Work and Verification

The developer performed the project setup and execution, including:

- Creating and organizing the project files and folders.
- Running the Python data generation scripts.
- Running the sensor data validation script.
- Executing preprocessing, encoding, and model training scripts.
- Creating and working with the MySQL database.
- Importing master data and telemetry records.
- Running prediction storage scripts.
- Launching and checking the Streamlit dashboard.
- Reviewing command outputs, SQL query results, and model evaluation metrics.

The developer reviewed the implementation and tested the main workflow locally.

## 6. Evidence of Verification

The following results were observed during development:

- 10,000 generated sensor readings passed the implemented validation checks.
- The model training script evaluated 2,000 test records.
- The reported model accuracy was 99.9% on the synthetic test dataset.
- MySQL contained 10,000 telemetry records and 10,000 predictions.
- The database verification query found zero telemetry records without predictions.
- The Streamlit dashboard launched successfully.

## 7. Responsible Use and Limitations

AI assistance does not replace understanding, code review, or testing.

The developer remains responsible for the submitted implementation and should be able to explain the code, design decisions, database structure, and model results.

The model's high accuracy is limited by the synthetic threshold-based dataset. It should not be presented as proven accuracy on real industrial machine failures.

## 8. Transparency Statement

AI tools were used to support learning, debugging, implementation guidance, and documentation. The developer executed the project locally, reviewed the outputs, and verified the main workflow. AI assistance and developer verification are described separately to make the development process transparent.