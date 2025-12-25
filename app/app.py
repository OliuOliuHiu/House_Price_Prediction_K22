from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import json
from database import get_connection, init_db

app = Flask(__name__)
init_db()

# Load the trained model and scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'scaler.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print("Model and scaler loaded successfully!")
except FileNotFoundError:
    print("Warning: Model files not found. Please train the model first.")
    model = None
    scaler = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 500
        
        # Get input features from form
        bedrooms = float(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        sqft_living = float(request.form['sqft_living'])
        sqft_lot = float(request.form['sqft_lot'])
        floors = float(request.form['floors'])
        yr_built = float(request.form['yr_built'])
        
        # Create feature array
        features = np.array([[bedrooms, bathrooms, sqft_living, 
                            sqft_lot, floors, yr_built]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]

                # Lưu vào DB
        input_data = {
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft_living': sqft_living,
            'sqft_lot': sqft_lot,
            'floors': floors,
            'yr_built': yr_built
        }
        save_record(input_data, prediction)
        
        return jsonify({
            'success': True,
            'predicted_price': round(prediction, 2)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def save_record(input_data, predicted_price):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        input_json = json.dumps(input_data)
        cursor.execute('''
            INSERT INTO predictions (input_data, predicted_price)
            VALUES (?, ?)
        ''', (input_json, float(predicted_price)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] Error saving to DB: {e}")


# if __name__ == '__main__':
#     app.run(debug=True)
