from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

with open('best_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return "Welcome to my Housing Price Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        floor_size_sq_ft = data.get('floor_size_sq_ft')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        address = data.get('address')

        if floor_size_sq_ft is None or latitude is None or longitude is None or address is None:
            return jsonify({'error': 'Missing data'}), 400

        features = np.array([[floor_size_sq_ft, latitude, longitude, address]])

        df = pd.DataFrame(data, index=[0])

        prediction = model.predict(df).round(2)[0]

        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
