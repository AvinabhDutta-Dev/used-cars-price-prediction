
from flask import Flask, jsonify, request
from flask_cors import CORS

from server.prediction import (
    InputValidationError,
    InvalidPredictionError,
    MissingFieldsError,
    load_model,
    predict_price,
)

app = Flask(__name__)
CORS(app)

# Load the trained model using the reusable prediction module.
model = load_model()


@app.get("/health")
def health():
    """Simple endpoint to check whether the API started successfully."""
    return jsonify({"status": "ok", "model_loaded": True})


@app.post("/predict")
def predict():
    if not request.is_json:
        return jsonify(
            {"error": "Send the request as JSON with Content-Type: application/json."}
        ), 415

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "The request body must be a JSON object."}), 400

    try:
        predicted_price = predict_price(payload, model)

    except MissingFieldsError as error:
        return jsonify(
            {
                "error": "Required fields are missing.",
                "details": {
                    field: "This field is required." for field in error.fields
                },
            }
        ), 400

    except InputValidationError as error:
        return jsonify(
            {
                "error": "Some input values are invalid.",
                "details": error.details,
            }
        ), 422

    except InvalidPredictionError as error:
        return jsonify({"error": str(error)}), 500

    return jsonify({"predicted_price": predicted_price})


if __name__ == "__main__":
    # Debug mode is disabled by default.
    app.run(host="127.0.0.1", port=5000, debug=False)
