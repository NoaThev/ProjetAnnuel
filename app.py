from flask import Flask, request, jsonify
import pandas as pd
import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

rf_model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
top_feature_names = joblib.load('top_feature_names.pkl')

@app.route('/')
def home():
    return "Hello, Flask API!"

@app.route('/health', methods=['GET'])
def health_check():
    try:
        return 'System OK', 200
    except Exception as e:
        return 'Error: ' + str(e), 500

@app.route('/predict/patient', methods=['POST'])
def predict_patient():
    try:
        # Obtenir les données de la requête POSTx
        patient_data = request.json

        # Vérifier que toutes les colonnes nécessaires sont présentes
        missing_columns = [col for col in top_feature_names if col not in patient_data]
        if missing_columns:
            return jsonify({"message": f"Missing data for columns: {', '.join(missing_columns)}"}), 422

        # Convertir les données en DataFrame
        patient_df = pd.DataFrame([patient_data])

        # Sélectionner les caractéristiques nécessaires
        x_new = patient_df[top_feature_names]

        # Appliquer la normalisation/scaling
        x_new_scaled = scaler.transform(x_new)

        # Faire les prédictions
        predictions = rf_model.predict(x_new_scaled)

        # Convertir les prédictions en une liste pour la réponse JSON
        predictions = predictions.tolist()

        response = {
            "message": "Prediction successful",
            "predictions": predictions
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
