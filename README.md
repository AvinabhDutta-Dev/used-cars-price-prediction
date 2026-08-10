# Used Car Price Prediction 🚗

A machine learning web app that predicts the selling price of a used car based on features like brand, vehicle age, mileage, fuel type, transmission, engine capacity, and more — trained on the CarDekho dataset.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Model Training | Python, Scikit-learn, Pandas |
| Backend API | Flask, Flask-CORS |
| Model Serialization | Joblib (.pkl) |
| Frontend | HTML, CSS, JavaScript |

---

## 📁 Project Structure

```
used-cars-price-prediction/
├── model/          # Training notebook + trained model
├── server/         # Flask API
├── client/         # Web frontend
└── data/           # Raw and cleaned datasets
```

---

## 📊 Data Pipeline

1. Raw dataset (`cardekho_dataset.csv`) sourced from the CarDekho used-car listings dataset.
2. Cleaned and preprocessed into `cleaned_cardekho_dataset.csv` — handling missing values and feature formatting.
3. Features used: brand, vehicle age, km driven, seller type, fuel type, transmission type, mileage, engine, max power, seats.
4. Model trained in `model/car_price_prediction_training.ipynb` and serialized as `car_price_prediction_model.pkl`.

---

## ⚙️ Setup

```bash
git clone https://github.com/AvinabhDutta-Dev/used-cars-price-prediction.git
cd used-cars-price-prediction
pip install flask flask-cors joblib pandas scikit-learn
```

---

## ▶️ Running

### 1. Start the Flask server
```bash
cd server
python server.py
```
Server runs on `http://127.0.0.1:5000`

### 2. Open the frontend
Open `client/UCPPM.html` directly in your browser (no build step needed).

---

## 📦 Requirements

`flask`, `flask-cors`, `joblib`, `pandas`, `scikit-learn`

---

## 📝 Notes

- The trained model (`car_price_prediction_model.pkl`, ~75MB) is included directly in the repo — under GitHub's 100MB file limit, no Git LFS needed.
- Dataset sourced from the publicly available CarDekho used-car dataset.
- This is a simple demo-style app — the frontend calls the Flask API directly at `localhost:5000`, so both must be running together locally.