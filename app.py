from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model and feature names
with open('house_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('feature_names.pkl', 'rb') as file:
    feature_names = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        input_data = {
            'Rooms': int(request.form.get('rooms')),
            'Bathroom': float(request.form.get('bathroom')),
            'Landsize': float(request.form.get('landsize')),
            'BuildingArea': float(request.form.get('buildingarea')),
            'YearBuilt': float(request.form.get('yearbuilt')),
            'Lattitude': float(request.form.get('lattitude')),
            'Longtitude': float(request.form.get('longtitude')),
            'Propertycount': float(request.form.get('propertycount')),
            'Distance': float(request.form.get('distance')),
            'Car': float(request.form.get('car')),
            'Year': int(request.form.get('year')),
            'Month': int(request.form.get('month')),
            'suburb_freq': float(request.form.get('suburb_freq')),
            'SellerG_freq': float(request.form.get('sellerg_freq')),
            'CouncilArea_freq': float(request.form.get('councilarea_freq')),
            'Type_h': int(request.form.get('type_h', 0)),
            'Type_t': int(request.form.get('type_t', 0)),
            'Method_PI': int(request.form.get('method_pi', 0)),
            'Method_SP': int(request.form.get('method_sp', 0)),
            'Method_VB': int(request.form.get('method_vb', 0)),
            'Regionname_Eastern Metropolitan': int(request.form.get('region_eastern', 0)),
            'Regionname_Eastern Victoria': int(request.form.get('region_eastern_vic', 0)),
            'Regionname_Northern Metropolitan': int(request.form.get('region_northern', 0)),
            'Regionname_Northern Victoria': int(request.form.get('region_northern_vic', 0)),
            'Regionname_Southeastern Metropolitan': int(request.form.get('region_southeastern', 0)),
            'Regionname_Southern Metropolitan': int(request.form.get('region_southern', 0)),
            'Regionname_Western Metropolitan': int(request.form.get('region_western', 0)),
            'Regionname_Western Victoria': int(request.form.get('region_western_vic', 0))
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure all required columns are present
        for col in feature_names:
            if col not in input_df.columns:
                input_df[col] = 0
        
        # Reorder columns to match training data
        input_df = input_df[feature_names]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'success': True,
            'prediction': f'${prediction:,.2f}',
            'message': 'Prediction successful!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)