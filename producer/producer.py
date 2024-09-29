from kafka import KafkaProducer
import json
from flask import Flask, request, jsonify


# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Use Kafka service name in Docker Compose
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

app = Flask(__name__)

@app.route('/receive_lap_data', methods=['POST'])
def receive_lap_data():
    lap_data = (request.json).get('lap_data')
    if lap_data:
        # Optionally, you could validate the incoming data here
        producer.send('lap_times', value=lap_data)
        return jsonify({"message": "Data sent to Kafka", "data": lap_data}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=3001)  # Ensure it runs on all interfaces
