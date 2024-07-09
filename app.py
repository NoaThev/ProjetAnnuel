from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Chemin vers le fichier Excel
FILE_PATH = 'C:\\Users\\noath\\Documents\\myapi\\data.xlsx'

@app.route('/')
def home():
    return "Hello, Flask API!"

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Vérifier si le fichier Excel est accessible
        if os.path.exists(FILE_PATH):
            pd.read_excel(FILE_PATH)
        return 'OK', 200
    except Exception as e:
        return 'Error: ' + str(e), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Vérifier si le fichier Excel existe
        if not os.path.exists(FILE_PATH):
            return jsonify({"message": "Le fichier de données n'existe pas."}), 404

        # Lire le fichier Excel
        df = pd.read_excel(FILE_PATH)

        # Convertir les données en dictionnaire
        data = df.to_dict(orient='records')

        response = {
            "message": "Voici quelques données",
            "data": data
        }
        return jsonify(response)
    except PermissionError:
        return jsonify({"message": "Permission denied. Cannot read the file."}), 403
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/data', methods=['POST'])
def post_data():
    try:
        # Récupérer les données envoyées dans la requête POST
        new_data = request.json

        # Convertir les nouvelles données en DataFrame
        new_df = pd.DataFrame([new_data])

        # Vérifier si le fichier Excel existe déjà
        if os.path.exists(FILE_PATH):
            # Lire le fichier Excel existant
            df = pd.read_excel(FILE_PATH)
            # Ajouter les nouvelles données
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            # Si le fichier n'existe pas, utiliser simplement les nouvelles données
            df = new_df

        # Sauvegarder les données dans le fichier Excel
        df.to_excel(FILE_PATH, index=False)

        response = {
            "message": "Données ajoutées avec succès",
            "data_received": new_data
        }
        return jsonify(response)
    except PermissionError:
        return jsonify({"message": "Permission denied. Cannot write to the file."}), 403
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/predict/patient', methods=['POST'])
def predict_patient():
    try:
        # Récupérer les données envoyées dans la requête POST
        patient_data = request.json

        # Définir les colonnes attendues
        expected_columns = ['ID', 'PRG', 'PL', 'PR', 'SK', 'TS', 'M11', 'BD2', 'Age', 'Insurance']

        # Vérifier que toutes les colonnes sont présentes
        for col in expected_columns:
            if col not in patient_data:
                return jsonify({"message": f"Missing data for {col}"}), 422

        # Exemple de logique simple pour prédire le statut du patient
        # Remplacer cette logique par un modèle de machine learning selon les besoins
        if patient_data['PRG'] > 5 or patient_data['PL'] > 150:
            status = 'Positive'
        else:
            status = 'Negative'

        response = {
            "message": "Prediction successful",
            "status": status
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
