from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
import json
from database import get_connection, init_db

app = Flask(__name__)
init_db()

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload Excel or CSV file'}), 400
        
        # Read the file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Check if required columns exist
        required_columns = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'yr_built']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }), 400
        
        # Convert DataFrame to JSON
        data = df[required_columns].to_dict('records')
        
        return jsonify({
            'success': True,
            'data': data,
            'columns': required_columns,
            'row_count': len(data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    try:
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 500
        
        data = request.get_json()
        rows = data.get('data', [])
        
        if not rows:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features
        features_list = []
        for row in rows:
            features = [
                float(row['bedrooms']),
                float(row['bathrooms']),
                float(row['sqft_living']),
                float(row['sqft_lot']),
                float(row['floors']),
                float(row['yr_built'])
            ]
            features_list.append(features)
        
        # Convert to numpy array
        X = np.array(features_list)
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make predictions
        predictions = model.predict(X_scaled)
        
        # Round predictions
        predictions = [round(pred, 2) for pred in predictions]
        
        return jsonify({
            'success': True,
            'predictions': predictions
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

if __name__ == '__main__':
    app.run(debug=True)
