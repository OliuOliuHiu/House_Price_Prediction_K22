# 🏠 House Price Prediction Application

A full-stack machine learning web application that predicts real estate prices using Random Forest regression algorithm. Built with Flask backend and modern responsive frontend.

---

## 🌐 Live Demo

**🔗 Web Application:** [http://3.24.151.146:5000/](http://3.24.151.146:5000/)

The application is currently deployed and accessible online. Visit the link above to try the house price prediction without any local installation.

---

## 📊 Overview

This project implements an end-to-end machine learning solution for house price prediction using the King County House Sales dataset. The application features a clean web interface where users can input property characteristics and receive instant price predictions.

**Key Metrics:**
- **Dataset:** 10,094 house records from King County, WA
- **Model Accuracy:** R² = 0.5703 (57.03% variance explained)
- **Algorithm:** Random Forest with 100 decision trees
- **Features:** 6 property characteristics
- **Tech Stack:** Python 3.13 + Flask + scikit-learn
- **Deployment:** AWS EC2 (ap-southeast-2)


## 🛠️ Technology Stack

**Backend:**
- Python 3.13.3
- Flask 3.1.2 - Web framework
- scikit-learn 1.8.0 - Machine learning
- NumPy 2.4.0 - Numerical computing
- Pandas 2.3.3 - Data manipulation

**Frontend:**
- HTML5 - Structure
- CSS3 - Responsive grid layout with animations
- Vanilla JavaScript - Async API calls with Fetch API

**Data Science:**
- Jupyter Notebook - Model development and training
- Matplotlib 3.10.8 - Visualization
- Seaborn 0.13.2 - Statistical plots
- StandardScaler - Feature normalization

**Database:**
- SQLite - Prediction history storage

---

## 📁 Project Structure

```
House_Price_Prediction_K22/
│
├── app/
│   ├── app.py              # Flask application server
│   ├── database.py         # Database operations and schema
│   ├── templates/
│   │   └── index.html      # Frontend interface
│   └── static/
│       └── style.css       # Styling and responsive design
│
├── model/
│   ├── model.pkl           # Trained Random Forest model
│   ├── scaler.pkl          # StandardScaler for normalization
│   └── process_assess_train_model.ipynb  # Training notebook
│
├── data/
│   └── kc_house_data.csv   # King County house sales dataset
│
├── db/                     # Auto-generated database directory
│   └── predictions.db      # SQLite database (created on first run)
│
├── requirements.txt        # Python dependencies
├── .gitignore             # Git exclusion rules
└── README.md              # This file
```

---

## 📋 Prerequisites

- Python 3.13.3 (Required)
- pip package manager
- Git
- 8GB+ RAM recommended (for model loading)
- Internet connection (for first-time package installation)

---

## 🔧 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/OliuOliuHiu/House_Price_Prediction_K22.git
cd House_Price_Prediction_K22
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter any issues:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python --version
# Should output: Python 3.13.3
```

---

## 🚀 Usage

### Quick Start (Online)

The easiest way to use the application is through the live deployment:

**🌍 Visit:** [http://3.24.151.146:5000/](http://3.24.151.146:5000/)

No installation required - just open the link in your browser and start making predictions!

### Running Locally

**Start the Flask server:**

```bash
python app/app.py
```

**Expected output:**

```
Model and scaler loaded successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**Access the application:**

- **Local:** `http://localhost:5000`
- **Online:** `http://3.24.151.146:5000`

### Making Predictions

1. Fill in the house details in the web form:
   - Bedrooms (1-5)
   - Bathrooms (1-5)
   - Living Area in square feet (500-15,000)
   - Lot Size in square feet (500-100,000)
   - Number of Floors (1-4)
   - Year Built (1900-2025)

2. Click "Predict Price"

3. View the predicted price displayed in USD

## 📈 Dataset Information

**Source:** King County House Sales Dataset

**Records:** 10,094 house sales

**Features Used:**
1. `bedrooms` - Number of bedrooms (0-11)
2. `bathrooms` - Number of bathrooms (0-8)
3. `sqft_living` - Living area in square feet (380-12,050)
4. `sqft_lot` - Lot size in square feet (572-1,651,359)
5. `floors` - Number of floors (1-3.5)
6. `yr_built` - Year the house was built (1900-2015)

**Target Variable:**
- `price` - House sale price in USD ($75,000 - $7,700,000)

**Data Quality:**
- No missing values
- 85 duplicate records (removed during preprocessing)
- Outliers filtered: bedrooms ≤ 10, sqft_living ≤ 10,000, price ≤ $5,000,000

## 💾 Database Schema

The application stores all predictions in a SQLite database

## 🔨 Development

### Model Retraining

For developers who want to retrain the model:

1. Open and run the Jupyter notebook: `model/process_assess_train_model.ipynb`
2. The notebook will automatically save new `model.pkl` and `scaler.pkl` files
3. Restart the Flask server to load the updated model

See the notebook for detailed training steps and parameter tuning options.


## 📞 Contact

**🌐 Live Application:** [http://3.24.151.146:5000/](http://3.24.151.146:5000/)

**📦 Repository:** [House_Price_Prediction_K22](https://github.com/OliuOliuHiu/House_Price_Prediction_K22)

Happy predicting! 🏠 💰 🚀
