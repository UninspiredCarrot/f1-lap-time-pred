from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

output_line = 0

@app.route('/receive_lap_data', methods=['POST'])
def send_prediction():
    data = request.get_json()
    print(data)

    try:
        response = requests.post(f"http://producer:3001/receive_lap_data", json=data)  # Send prediction to the Flask app
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
    data = request.get_json()

    predicted_lap_time = data.get('prediction')
    lap_data = data.get('lap_data')

    with open("output.txt", "a") as f:
        f.write(f"Received prediction: {predicted_lap_time}\n")

    return jsonify({"status": "success", "message": "Prediction received."}), 200

@app.route('/prediction', methods=['GET'])
def get_latest_prediction():
    global output_line  # Declare output_line as global so it can be modified

    try:
        with open("output.txt", "r") as f:
            lines = f.readlines()

        if not lines:
            return jsonify({"error": "No predictions found"}), 404

        if len(lines) <= output_line:
            return jsonify({"error": "No more predictions available"}), 404

        last_prediction = lines[output_line].strip()
        output_line += 1

        return jsonify({"status": "success", "prediction": last_prediction}), 200

    except FileNotFoundError:
        return jsonify({"error": "No predictions found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)  # Ensure it runs on all interfaces
