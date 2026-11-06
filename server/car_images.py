
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OPTIMIZED_DIR = PROJECT_ROOT / "assets" / "cars" / "optimized"

DEFAULT_CAR_IMAGE = PROJECT_ROOT / "client" / "CAR.jpg"

CAR_IMAGE_MAP = {
    "Maruti": {
        "Swift": "maruti_swift.webp",
        "Baleno": "maruti_baleno.webp",
        "Alto": "maruti_alto.webp",
        "Wagon R": "maruti_wagon_r.webp",
    },
    "Hyundai": {
        "Creta": "hyundai_creta.webp",
        "i20": "hyundai_i20.webp",
        "Verna": "hyundai_verna.webp",
    },
    "Tata": {
        "Nexon": "tata_nexon.webp",
        "Tiago": "tata_tiago.webp",
    },
    "Honda": {
        "City": "honda_city.webp",
        "Amaze": "honda_amaze.webp",
    },
    "Mahindra": {
        "Scorpio": "mahindra_scorpio.webp",
        "XUV500": "mahindra_xuv500.webp",
    },
    "Ford": {
        "EcoSport": "ford_ecosport.webp",
    },
    "Volkswagen": {
        "Polo": "volkswagen_polo.webp",
    },
}


def get_car_image_path(brand: str, model: str) -> str:
    """Return the matching car image or the generic fallback image."""

    image_filename = CAR_IMAGE_MAP.get(brand, {}).get(model)

    if image_filename:
        image_path = OPTIMIZED_DIR / image_filename

        if image_path.is_file():
            return str(image_path)

    return str(DEFAULT_CAR_IMAGE)
