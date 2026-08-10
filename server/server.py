from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('car_price_prediction_model.pkl')


# Define a route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)

    # Convert the data into a DataFrame
    input_data = pd.DataFrame([data])

    # Make predictions using the loaded model
    prediction = model.predict(input_data)

    # Return the prediction as a JSON response
    return jsonify({'predicted_price': prediction[0]})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
