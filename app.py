from flask import Flask, request, jsonify
import pandas as pd
import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

best_model = joblib.load(r'C:\Users\noath\Documents\myapi\Test2\logistic_regression_model.pkl')
scaler = joblib.load(r'C:\Users\noath\Documents\myapi\Test2\scaler.pkl')
top_feature_names = joblib.load(r'C:\Users\noath\Documents\myapi\Test2\top_feature_names.pkl')

@app.route('/')
def home():
    return "Hello, Flask API!"

@app.route('/health', methods=['GET'])
def health_check():
    custom_input = {
        'PL': 5.0,
        'M11': 3.0,
        'Age': 1.4,
        'BD2': 0.2,
        'PR': 2.5,
        'TS': 1.5,
        'PRG': 0.5
    }

    custom_input_df = pd.DataFrame([custom_input])

    custom_input_top = custom_input_df[top_feature_names]

    custom_input_top_scaled = scaler.transform(custom_input_top)

    predictions = best_model.predict(custom_input_top_scaled)

    print(f'Predicted class: {predictions[0]}')

    if predictions[0] == "Negative" or predictions[0] == "Positive" : return "System Ok" 
    else : return "System not OK"

@app.route('/predict/patient', methods=['POST'])
def predict():

    data = request.json

    custom_input = {
        'PL': list(data.values())[1],
        'M11': list(data.values())[2],
        'Age': list(data.values())[3],
        'BD2': list(data.values())[4],
        'PR': list(data.values())[5],
        'TS': list(data.values())[6],
        'PRG': list(data.values())[0]
    }

    custom_input_df = pd.DataFrame([custom_input])

    custom_input_top = custom_input_df[top_feature_names]

    custom_input_top_scaled = scaler.transform(custom_input_top)

    predictions = best_model.predict(custom_input_top_scaled)

    print(f'Predicted class: {predictions[0]}')

    return predictions[0]
    
if __name__ == '__main__':
    app.run(debug=True)
