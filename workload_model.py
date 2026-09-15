import os
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


MODEL_DATA = "workload_history.csv"


def load_training_data(filename=MODEL_DATA):
    """Load historical assignment data."""

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Training data file '{filename}' was not found."
        )

    return pd.read_csv(filename)


def train_workload_model(filename=MODEL_DATA):
    """
    Train a Random Forest model to predict assignment workload.

    Features:
    - difficulty
    - importance
    - assignment type
    - course

    Target:
    - actual hours spent
    """

    data = load_training_data(filename)

    required_columns = [
        "difficulty",
        "importance",
        "assignment_type",
        "course",
        "actual_hours"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"Missing required training column: {column}"
            )

    X = data[
        [
            "difficulty",
            "importance",
            "assignment_type",
            "course"
        ]
    ]

    y = data["actual_hours"]

    categorical_features = [
        "assignment_type",
        "course"
    ]

    numeric_features = [
        "difficulty",
        "importance"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
            )
        ]
    )

    model.fit(X, y)

    return model


def predict_workload(model, assignment):
    """Predict how many hours an assignment will take."""

    input_data = pd.DataFrame([
        {
            "difficulty": assignment["difficulty"],
            "importance": assignment.get("importance", 3),
            "assignment_type": assignment.get(
                "assignment_type",
                "Other"
            ),
            "course": assignment.get(
                "course",
                "Unknown"
            )
        }
    ])

    prediction = model.predict(input_data)[0]

    return round(max(prediction, 0.5), 1)
