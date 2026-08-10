function predictPrice() {
    // Get the form data
    const brand = document.getElementById('brand').value;
    const vehicle_age = document.getElementById('vehicle_age').value;
    const km_driven = document.getElementById('km_driven').value;
    const seller_type = document.getElementById('seller_type').value;
    const fuel_type = document.getElementById('fuel_type').value;
    const transmission_type = document.getElementById('transmission_type').value;
    const mileage = document.getElementById('mileage').value;
    const engine = document.getElementById('engine').value;
    const max_power = document.getElementById('max_power').value;
    const seats = document.getElementById('seats').value;

    // Create a JSON object to send to the server
    const carData = {
        brand: brand,
        vehicle_age: parseInt(vehicle_age),
        km_driven: parseInt(km_driven),
        seller_type: seller_type,
        fuel_type: fuel_type,
        transmission_type: transmission_type,
        mileage: parseFloat(mileage),
        engine: parseInt(engine),
        max_power: parseFloat(max_power),
        seats: parseInt(seats)
    };

    // Send the data to the Flask server using fetch
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(carData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the result in the #result div
        document.getElementById('result').innerText = `Predicted Price: ₹${data.predicted_price.toFixed(2)}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
