
import math
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Resolve paths from the project root, not the terminal's current directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "model" / "car_price_prediction_model.pkl"

if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"Trained model not found at {MODEL_PATH}. "
        "Make sure model/car_price_prediction_model.pkl exists."
    )

model = joblib.load(MODEL_PATH)

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


@app.get("/health")
def health():
    """Simple endpoint to check whether the API started successfully."""
    return jsonify({"status": "ok", "model_loaded": True})


@app.post("/predict")
def predict():
    if not request.is_json:
        return jsonify({
            "error": "Send the request as JSON with Content-Type: application/json."
        }), 415

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "The request body must be a JSON object."}), 400

    missing = [
        field for field in FEATURE_COLUMNS
        if field not in payload or payload[field] is None
    ]

    if missing:
        return jsonify({
            "error": "Required fields are missing.",
            "details": {field: "This field is required." for field in missing},
        }), 400

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
            errors[field] = "Enter a value greater than zero where required, otherwise zero or greater."
            continue

        if field in INTEGER_FIELDS and not number.is_integer():
            errors[field] = "Enter a whole number."
            continue

        cleaned[field] = int(number) if field in INTEGER_FIELDS else number

    if errors:
        return jsonify({
            "error": "Some input values are invalid.",
            "details": errors,
        }), 422

    input_data = pd.DataFrame([cleaned], columns=FEATURE_COLUMNS)
    predicted_price = float(model.predict(input_data)[0])

    if not math.isfinite(predicted_price):
        return jsonify({"error": "The model returned an invalid prediction."}), 500

    return jsonify({"predicted_price": predicted_price})


if __name__ == "__main__":
    # Debug mode is disabled by default.
    app.run(host="127.0.0.1", port=5000, debug=False)
