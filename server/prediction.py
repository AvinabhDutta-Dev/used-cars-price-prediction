import math
from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "model" / "car_price_prediction_model.pkl"

FEATURE_COLUMNS = [
    "brand",
    "vehicle_age",
    "km_driven",
    "seller_type",
    "fuel_type",
    "transmission_type",
    "mileage",
    "engine",
    "max_power",
    "seats",
]

CATEGORICAL_FIELDS = [
    "brand",
    "seller_type",
    "fuel_type",
    "transmission_type",
]

INTEGER_FIELDS = {"vehicle_age", "km_driven", "engine", "seats"}
POSITIVE_FIELDS = {"mileage", "engine", "max_power", "seats"}


class MissingFieldsError(ValueError):
    """Raised when required prediction fields are missing."""

    def __init__(self, fields):
        self.fields = fields
        super().__init__("Required fields are missing.")


class InputValidationError(ValueError):
    """Raised when one or more prediction inputs are invalid."""

    def __init__(self, details):
        self.details = details
        super().__init__("Some input values are invalid.")


class InvalidPredictionError(RuntimeError):
    """Raised when the model returns an invalid prediction."""


def load_model():
    """Load the trained scikit-learn model."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            "Make sure model/car_price_prediction_model.pkl exists."
        )

    return joblib.load(MODEL_PATH)


def prepare_input(payload):
    """Validate vehicle information and create the model input DataFrame."""
    missing = [
        field
        for field in FEATURE_COLUMNS
        if field not in payload or payload[field] is None
    ]

    if missing:
        raise MissingFieldsError(missing)

    cleaned = {}
    errors = {}

    # Validate categorical inputs.
    for field in CATEGORICAL_FIELDS:
        value = payload[field]

        if not isinstance(value, str) or not value.strip():
            errors[field] = "Enter a non-empty text value."
        else:
            cleaned[field] = value.strip()

    # Validate numeric inputs.
    for field in FEATURE_COLUMNS:
        if field in CATEGORICAL_FIELDS:
            continue

        value = payload[field]

        if isinstance(value, bool):
            errors[field] = "Enter a valid number."
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            errors[field] = "Enter a valid number."
            continue

        if not math.isfinite(number):
            errors[field] = "The number must be finite."
            continue

        if number < 0 or (field in POSITIVE_FIELDS and number == 0):
            errors[field] = "Enter a positive value, or zero where permitted."
            continue

        if field in INTEGER_FIELDS and not number.is_integer():
            errors[field] = "Enter a whole number."
            continue

        if field == "seats" and number < 2:
            errors[field] = "Enter at least 2 seats."
            continue

        cleaned[field] = int(number) if field in INTEGER_FIELDS else number

    if errors:
        raise InputValidationError(errors)

    return pd.DataFrame([cleaned], columns=FEATURE_COLUMNS)


def predict_price(payload, model):
    """Validate vehicle information and return the predicted price."""
    input_data = prepare_input(payload)

    predicted_price = float(model.predict(input_data)[0])

    if not math.isfinite(predicted_price):
        raise InvalidPredictionError("The model returned an invalid prediction.")

    return predicted_price
