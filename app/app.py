from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler
import json
import pandas as pd
import joblib
import numpy as np
import requests
import fastf1

data = pd.read_pickle('data/cleaned_laps_df.pkl')
scaler = joblib.load('data/scaler.pkl')
X = data.drop(columns=['LapTimeSeconds'])

app = Flask(__name__)

@app.route('/send_prediction', methods=['POST'])
def send_prediction():
    data = request.get_json()
    lap_df = pd.DataFrame(pd.DataFrame([X.iloc[data.get('index')]]))
    print(lap_df)
    normalized_lap_values = scaler.transform(lap_df)
    normalized_lap_data = dict(zip(X.columns, normalized_lap_values[0]))
    payload = {"lap_data": normalized_lap_data}
    
    try:
        response = requests.post(f"http://producer:3001/receive_lap_data", json=payload)  # Send prediction to the Flask app
        if response.status_code == 200:
            print("Prediction sent to producer successfully.")
            return jsonify({"status": "success", "message": "index received"}), 200

        else:
            print(f"Failed to send prediction to producer app: {response.status_code} - {response.text}")
            return jsonify({"error": "Invalid data"}), 400
    except requests.exceptions.RequestException as e:
        print(f"Error sending prediction to producer app: {e}")
        return jsonify({"error": "Invalid data"}), 400
    


@app.route('/receive_prediction', methods=['POST'])
def receive_prediction():
    print('hi')
    # Get the JSON data from the request
    data = request.get_json()
    
    # Extract the predicted lap time and lap data
    predicted_lap_time = data.get('predicted_lap_time')
    lap_data = data.get('lap_data')

    # Log the received prediction
    print(f"Received prediction: {predicted_lap_time}")
    print(f"Lap data: {lap_data}")

    f = open("output.txt", "a")
    f.write(f"Received prediction: {predicted_lap_time}")
    f.close()

    # Here you could save the prediction to a database or perform additional processing

    # Return a success response
    return jsonify({"status": "success", "message": "Prediction received."}), 200

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=3000)  # Ensure it runs on all interfaces
