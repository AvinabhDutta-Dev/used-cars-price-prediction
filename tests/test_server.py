import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


class FakeModel:
    """Return a fixed prediction without loading the real model."""

    def predict(self, features):
        return [176738.78174603195]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVER_FILE = PROJECT_ROOT / "server" / "server.py"

spec = importlib.util.spec_from_file_location(
    "car_price_server_under_test",
    SERVER_FILE,
)

if spec is None or spec.loader is None:
    raise ImportError(f"Could not load server module from {SERVER_FILE}")

server_module = importlib.util.module_from_spec(spec)

# Prevent the real model from being loaded during API tests.
with patch("joblib.load", return_value=FakeModel()):
    sys.modules[spec.name] = server_module
    spec.loader.exec_module(server_module)


class PredictionAPITests(unittest.TestCase):
    def setUp(self):
        self.client = server_module.app.test_client()

    def valid_payload(self):
        return {
            "brand": "Maruti",
            "vehicle_age": 9,
            "km_driven": 120000,
            "seller_type": "Individual",
            "fuel_type": "Petrol",
            "transmission_type": "Manual",
            "mileage": 19.7,
            "engine": 796,
            "max_power": 46.3,
            "seats": 5,
        }

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertTrue(response.get_json()["model_loaded"])

    def test_valid_prediction(self):
        response = self.client.post(
            "/predict",
            json=self.valid_payload(),
        )

        self.assertEqual(
            response.status_code,
            200,
            response.get_json(),
        )
        self.assertEqual(
            response.get_json()["predicted_price"],
            176738.78174603195,
        )

    def test_missing_field_returns_bad_request(self):
        payload = self.valid_payload()
        payload.pop("brand")

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_invalid_numeric_value_returns_bad_request(self):
        payload = self.valid_payload()
        payload["km_driven"] = "not-a-number"

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)
        self.assertIn("error", response.get_json())

    def test_non_json_request_returns_415(self):
        response = self.client.post(
            "/predict",
            data="not json",
            content_type="text/plain",
        )

        self.assertEqual(response.status_code, 415)

    def test_non_object_json_returns_400(self):
        response = self.client.post(
            "/predict",
            data="[]",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_categorical_value_returns_422(self):
        payload = self.valid_payload()
        payload["brand"] = "   "

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)
        self.assertIn("brand", response.get_json()["details"])

    def test_non_string_categorical_value_returns_422(self):
        payload = self.valid_payload()
        payload["brand"] = 123

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_non_finite_numeric_value_returns_422(self):
        payload = self.valid_payload()
        payload["mileage"] = "nan"

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_negative_numeric_value_returns_422(self):
        payload = self.valid_payload()
        payload["km_driven"] = -100

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_zero_positive_field_returns_422(self):
        payload = self.valid_payload()
        payload["mileage"] = 0

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_fractional_integer_field_returns_422(self):
        payload = self.valid_payload()
        payload["vehicle_age"] = 9.5

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_boolean_numeric_value_returns_422(self):
        payload = self.valid_payload()
        payload["km_driven"] = True

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 422)

    def test_invalid_model_prediction_returns_500(self):
        class InvalidModel:
            def predict(self, features):
                return [float("nan")]

        original_model = server_module.model

        try:
            server_module.model = InvalidModel()

            response = self.client.post(
                "/predict",
                json=self.valid_payload(),
            )
        finally:
            server_module.model = original_model

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
