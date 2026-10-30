
const form = document.getElementById("prediction-form");
const result = document.getElementById("result");
const submitButton = form.querySelector('button[type="submit"]');

function showResult(message, type = "") {
    result.textContent = message;
    result.style.color =
        type === "error" ? "#b91c1c" :
        type === "success" ? "#166534" : "";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const carData = {
        brand: document.getElementById("brand").value.trim(),
        vehicle_age: Number(document.getElementById("vehicle_age").value),
        km_driven: Number(document.getElementById("km_driven").value),
        seller_type: document.getElementById("seller_type").value,
        fuel_type: document.getElementById("fuel_type").value,
        transmission_type: document.getElementById("transmission_type").value,
        mileage: Number(document.getElementById("mileage").value),
        engine: Number(document.getElementById("engine").value),
        max_power: Number(document.getElementById("max_power").value),
        seats: Number(document.getElementById("seats").value)
    };

    submitButton.disabled = true;
    showResult("Predicting price...");

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(carData)
        });

        let data = {};
        try {
            data = await response.json();
        } catch {
            // Handle responses that are not valid JSON.
        }

        if (!response.ok) {
            const details = data.details
                ? Object.entries(data.details)
                    .map(([field, message]) => `${field}: ${message}`)
                    .join(" ")
                : "";

            throw new Error(
                [data.error || `Request failed (${response.status}).`, details]
                    .filter(Boolean)
                    .join(" ")
            );
        }

        const price = Number(data.predicted_price);

        if (!Number.isFinite(price)) {
            throw new Error("The server returned an invalid price.");
        }

        showResult(
            `Predicted Price: ₹${price.toLocaleString("en-IN", {
                maximumFractionDigits: 2
            })}`,
            "success"
        );
    } catch (error) {
        showResult(
            `Prediction failed: ${error.message}. Check that the Flask server is running.`,
            "error"
        );
    } finally {
        submitButton.disabled = false;
    }
});
