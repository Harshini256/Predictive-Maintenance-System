
import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Find project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Dataset folder
DATA_FOLDER = PROJECT_ROOT / "data" / "processed"

# Model folder
MODEL_FOLDER = PROJECT_ROOT / "models"


def train_model():

    print("Starting Machine Learning Model Training...")

    # Create models folder if it does not exist
    MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

    # Read training and testing features
    X_train = pd.read_csv(DATA_FOLDER / "X_train_encoded.csv")
    X_test = pd.read_csv(DATA_FOLDER / "X_test_encoded.csv")

    # Read training and testing target values
    y_train = pd.read_csv(DATA_FOLDER / "y_train.csv").squeeze()
    y_test = pd.read_csv(DATA_FOLDER / "y_test.csv").squeeze()

    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))

    # Create Random Forest model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    # Train the model
    print("\nTraining the model...")
    model.fit(X_train, y_train)

    print("Model training completed!")

    # Predict results using testing data
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

    # Display classification report
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            labels=[0, 1],
            target_names=["Normal", "Abnormal"],
            zero_division=0
        )
    )

    # Display confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

    # Display feature importance
    print("\nFeature Importance:")
    importance = pd.Series(
        model.feature_importances_,
        index=X_train.columns
    )

    print(importance.sort_values(ascending=False))

    # Save trained model
    model_path = MODEL_FOLDER / "random_forest_model.pkl"

    joblib.dump(model, model_path)

    print("\nTrained model saved:", model_path)

    print("\nModel training and evaluation completed successfully!")


if __name__ == "__main__":
    train_model()
