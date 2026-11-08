import unittest

import pandas as pd

from server.prediction import (
    FEATURE_COLUMNS,
    InputValidationError,
    InvalidPredictionError,
    MissingFieldsError,
    predict_price,
    prepare_input,
)


class FakeModel:
    """Return a fixed prediction without loading the real model."""

    def predict(self, features):
        return [176738.78174603195]


class InvalidModel:
    """Return an invalid prediction for testing."""

    def predict(self, features):
        return [float("nan")]


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.model = FakeModel()

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

    def test_valid_input_creates_dataframe(self):
        result = prepare_input(self.valid_payload())

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), FEATURE_COLUMNS)
        self.assertEqual(len(result), 1)

    def test_categorical_values_are_trimmed(self):
        payload = self.valid_payload()
        payload["brand"] = "  Maruti  "

        result = prepare_input(payload)

        self.assertEqual(result.iloc[0]["brand"], "Maruti")

    def test_integer_fields_are_converted(self):
        payload = self.valid_payload()
        payload["vehicle_age"] = "9"

        result = prepare_input(payload)

        self.assertEqual(result.iloc[0]["vehicle_age"], 9)
        self.assertTrue(pd.api.types.is_integer_dtype(result["vehicle_age"]))

    def test_missing_field_raises_error(self):
        payload = self.valid_payload()
        payload.pop("brand")

        with self.assertRaises(MissingFieldsError):
            prepare_input(payload)

    def test_empty_categorical_value_raises_error(self):
        payload = self.valid_payload()
        payload["brand"] = "   "

        with self.assertRaises(InputValidationError) as context:
            prepare_input(payload)

        self.assertIn("brand", context.exception.details)

    def test_non_string_categorical_value_raises_error(self):
        payload = self.valid_payload()
        payload["brand"] = 123

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_invalid_numeric_value_raises_error(self):
        payload = self.valid_payload()
        payload["km_driven"] = "not-a-number"

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_non_finite_numeric_value_raises_error(self):
        payload = self.valid_payload()
        payload["mileage"] = "nan"

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_negative_numeric_value_raises_error(self):
        payload = self.valid_payload()
        payload["km_driven"] = -100

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_zero_positive_field_raises_error(self):
        payload = self.valid_payload()
        payload["mileage"] = 0

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_one_seat_raises_error(self):
        payload = self.valid_payload()
        payload["seats"] = 1

        with self.assertRaises(InputValidationError) as context:
            prepare_input(payload)

        self.assertEqual(
            context.exception.details["seats"],
            "Enter at least 2 seats.",
        )

    def test_fractional_integer_field_raises_error(self):
        payload = self.valid_payload()
        payload["vehicle_age"] = 9.5

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_boolean_numeric_value_raises_error(self):
        payload = self.valid_payload()
        payload["km_driven"] = True

        with self.assertRaises(InputValidationError):
            prepare_input(payload)

    def test_valid_prediction(self):
        result = predict_price(self.valid_payload(), self.model)

        self.assertEqual(result, 176738.78174603195)

    def test_invalid_model_prediction_raises_error(self):
        with self.assertRaises(InvalidPredictionError):
            predict_price(self.valid_payload(), InvalidModel())


if __name__ == "__main__":
    unittest.main()
