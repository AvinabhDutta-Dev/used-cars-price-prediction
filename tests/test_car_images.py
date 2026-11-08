import unittest
from unittest.mock import patch

from server.car_images import (
    DEFAULT_CAR_IMAGE,
    OPTIMIZED_DIR,
    get_car_image_path,
)


class CarImageTests(unittest.TestCase):
    def test_existing_model_image_is_returned(self):
        expected_path = OPTIMIZED_DIR / "maruti_swift.webp"

        with patch("server.car_images.Path.is_file", return_value=True):
            result = get_car_image_path("Maruti", "Swift")

        self.assertEqual(result, str(expected_path))

    def test_missing_model_image_returns_default(self):
        with patch("server.car_images.Path.is_file", return_value=False):
            result = get_car_image_path("Maruti", "Swift")

        self.assertEqual(result, str(DEFAULT_CAR_IMAGE))

    def test_unknown_brand_returns_default(self):
        result = get_car_image_path("Unknown Brand", "Unknown Model")

        self.assertEqual(result, str(DEFAULT_CAR_IMAGE))

    def test_unknown_model_returns_default(self):
        result = get_car_image_path("Maruti", "Unknown Model")

        self.assertEqual(result, str(DEFAULT_CAR_IMAGE))

    def test_empty_brand_returns_default(self):
        result = get_car_image_path("", "Swift")

        self.assertEqual(result, str(DEFAULT_CAR_IMAGE))

    def test_empty_model_returns_default(self):
        result = get_car_image_path("Maruti", "")

        self.assertEqual(result, str(DEFAULT_CAR_IMAGE))


if __name__ == "__main__":
    unittest.main()
