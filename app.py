
from pathlib import Path

import gradio as gr
import pandas as pd
from gradio.themes import Soft

from server.car_images import get_car_image_path
from server.prediction import (
    InputValidationError,
    InvalidPredictionError,
    MissingFieldsError,
    load_model,
    predict_price,
)

# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT / "data" / "cleaned_cardekho_dataset.csv"
)

# Load the trained model once when the application starts.
model = load_model()

# Load available brands and car models from the dataset.
df = pd.read_csv(DATASET_PATH)

BRAND_MODEL_MAP: dict[str, list[str]] = {
    str(brand): sorted(
        group["model"].dropna().astype(str).unique().tolist()
    )
    for brand, group in df.groupby("brand")
}

BRANDS = sorted(BRAND_MODEL_MAP)

DEFAULT_BRAND = "Maruti"

DEFAULT_MODEL = (
    "Swift"
    if "Swift" in BRAND_MODEL_MAP[DEFAULT_BRAND]
    else BRAND_MODEL_MAP[DEFAULT_BRAND][0]
)


# --------------------------------------------------
# 2. DYNAMIC CAR IMAGE FUNCTIONS
# --------------------------------------------------


def update_brand(brand):
    """Update the model dropdown when a brand is selected."""

    available_models = BRAND_MODEL_MAP.get(brand, [])

    return (
        gr.Dropdown(
            choices=available_models,
            value=None,
            info="Example: Swift",
        ),
        None,
    )



def update_car_image(brand, selected_model):
    """Display the image corresponding to the selected car."""

    return get_car_image_path(brand, selected_model)


# --------------------------------------------------
# 3. PRICE PREDICTION FUNCTION
# --------------------------------------------------


def format_indian_number(amount):
    """Format a number using Indian digit grouping."""

    number = str(round(amount))

    if len(number) <= 3:
        return number

    last_three = number[-3:]
    remaining = number[:-3]

    groups = []

    while remaining:
        groups.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    return ",".join(groups + [last_three])


def format_indian_price(amount):
    """Format a predicted price in INR with lakh/crore equivalents."""

    formatted_amount = format_indian_number(amount)

    if amount >= 10_000_000:
        equivalent = f"₹{amount / 10_000_000:.2f} crore"
    elif amount >= 100_000:
        equivalent = f"₹{amount / 100_000:.2f} lakh"
    else:
        equivalent = None

    result = f"## ₹{formatted_amount}"

    if equivalent:
        result += f"\n\n**Approximately {equivalent}**"

    return result


def predict_car_price(
    brand,
    vehicle_age,
    km_driven,
    seller_type,
    fuel_type,
    transmission_type,
    mileage,
    engine,
    max_power,
    seats,
):
    """Validate the inputs and predict the selling price."""


    payload = {
        "brand": brand,
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "seller_type": seller_type,
        "fuel_type": fuel_type,
        "transmission_type": transmission_type,
        "mileage": mileage,
        "engine": engine,
        "max_power": max_power,
        "seats": seats,
    }

    # Exclude empty fields so the shared validator
    # can identify them as missing information.
    payload = {
        field: value
        for field, value in payload.items()
        if value is not None
        and not (isinstance(value, str) and not value.strip())
    }

    try:
        predicted_price = predict_price(payload, model)

        return (
            "### Estimated Selling Price\n"
            f"{format_indian_price(predicted_price)}\n\n"
            "This is an estimated price based on the trained "
            "machine learning model."
        )

    except MissingFieldsError as error:
        return (
            "### Missing Information\n"
            f"Please provide all required fields: {error.fields}"
        )

    except InputValidationError as error:
        return (
            "### Invalid Input\n"
            f"{error.details}"
        )

    except InvalidPredictionError:
        return (
            "### Prediction Error\n"
            "The model returned an invalid prediction. "
            "Please try again."
        )

    except Exception:
        return (
            "### Unexpected Error\n"
            "Something went wrong while predicting the price. "
            "Please check your inputs and try again."
        )


# --------------------------------------------------
# 4. GRADIO INTERFACE
# --------------------------------------------------

with gr.Blocks(
    title="Used Cars Price Prediction",
) as demo:

    gr.Markdown(
        """
        # 🚗 Used Cars Price Prediction

        Estimate the resale value of a used car using
        machine learning.

        Select your car details, enter its specifications,
        and get an estimated selling price.
        """
    )

    with gr.Row():

        # LEFT COLUMN: INPUT FORM
        with gr.Column(scale=6):

            gr.Markdown("### Car Information")

            brand_dropdown = gr.Dropdown(
                choices=BRANDS,
                value=None,
                label="Car Brand",
                info="Example: Maruti",
                interactive=True,
            )

            model_dropdown = gr.Dropdown(
                choices=[],
                value=None,
                label="Car Model",
                info="Example: Swift",
                interactive=True,
            )

            gr.Markdown("### Vehicle Specifications")

            with gr.Row():
                vehicle_age = gr.Textbox(
                    label="Vehicle Age (Years)",
                    value="",
                    placeholder="e.g. 5",
                )

                km_driven = gr.Textbox(
                    label="Kilometres Driven (km)",
                    value="",
                    placeholder="e.g. 50000",
                )

            with gr.Row():
                mileage = gr.Textbox(
                    label="Mileage (km/L)",
                    value="",
                    placeholder="e.g. 20.5",
                )

                engine = gr.Textbox(
                    label="Engine Capacity (cc)",
                    value="",
                    placeholder="e.g. 1199",
                )

            with gr.Row():
                max_power = gr.Textbox(
                    label="Maximum Power (bhp)",
                    value="",
                    placeholder="e.g. 82",
                )

                seats = gr.Textbox(
                    label="Number of Seats",
                    value="",
                    placeholder="e.g. 5",
                )


            gr.Markdown("### Additional Details")

            seller_type = gr.Dropdown(
                choices=[
                    "Dealer",
                    "Individual",
                    "Trustmark Dealer",
                ],
                value=None,
                label="Seller Type",
                info="Example: Individual",
)

            fuel_type = gr.Dropdown(
                choices=[
                    "Petrol",
                    "Diesel",
                    "CNG",
                    "LPG",
                ],
                value=None,
                label="Fuel Type",
                info="Example: Petrol",
            )

            transmission_type = gr.Dropdown(
                choices=[
                    "Manual",
                    "Automatic",
                ],
                value=None,
                label="Transmission Type",
                info="Example: Manual",
            )

            predict_button = gr.Button(
                "Predict Selling Price",
                variant="primary",
                size="lg",
            )

        # RIGHT COLUMN: CAR IMAGE AND RESULT
        with gr.Column(scale=5):

            gr.Markdown("### Selected Vehicle")

            car_image = gr.Image(
                value=None,
                label="Car Preview",
                type="filepath",
                interactive=False,
                height=300,
            )

            gr.Markdown(
                "### Prediction Result"
            )

            prediction_output = gr.Markdown(
                "Your estimated selling price will appear here."
            )

            gr.Markdown(
                """
                **Note:** The displayed car photograph is for
                visual reference. It does not influence the
                machine learning prediction.
                """
            )

    # --------------------------------------------------
    # 5. INTERFACE EVENT HANDLERS
    # --------------------------------------------------

    brand_dropdown.change(
        fn=update_brand,
        inputs=brand_dropdown,
        outputs=[
            model_dropdown,
            car_image,
        ],
    )

    model_dropdown.change(
        fn=update_car_image,
        inputs=[
            brand_dropdown,
            model_dropdown,
        ],
        outputs=car_image,
    )

    predict_button.click(
        fn=predict_car_price,
        inputs=[
            brand_dropdown,
            vehicle_age,
            km_driven,
            seller_type,
            fuel_type,
            transmission_type,
            mileage,
            engine,
            max_power,
            seats,
        ],
        outputs=prediction_output,
    )


# --------------------------------------------------
# 6. APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=Soft(),
    )
