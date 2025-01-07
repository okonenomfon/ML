from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('best_model.pkl', 'rb') as file:
    model = pickle.load(file)


@app.route('/')
def home():
    """
    Render the homepage with the input form.
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle the prediction request. Validates the inputs, prepares data, 
    and generates the prediction.
    """
    try:
        # Get data from the form
        floor_size_sq_ft = request.form.get('floor_size_sq_ft')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        address = request.form.get('address')  # New field

        # Input validation
        if not floor_size_sq_ft or not latitude or not longitude or not address:
            return jsonify({'error': 'Missing data: All fields are required (floor size, latitude, longitude, address).'}), 400

        # Convert to numeric types
        try:
            floor_size_sq_ft = float(floor_size_sq_ft)
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return jsonify({'error': 'Invalid input: floor size, latitude, and longitude must be numeric.'}), 400

        # Prepare data for prediction
        input_data = pd.DataFrame([[floor_size_sq_ft, latitude, longitude, address]],
                                  columns=['floor_size_sq_ft', 'latitude', 'longitude', 'address'])

        # Make prediction
        prediction = model.predict(input_data).round(2)[0]

        # Return result
        return render_template('result.html', prediction=prediction)

    except Exception as e:
        # Catch and display any other errors
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

