from kafka import KafkaConsumer
import os
import tensorflow as tf
import numpy as np
import json
import pandas as pd
import requests
import joblib

# Kafka settings
kafka_host = os.environ.get("KAFKA_HOST", "kafka:9092")  # Use the environment variable or default to kafka:9092
topic_name = "lap_times"  # Replace with your topic name

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=kafka_host,
    auto_offset_reset='earliest',  # Start from the earliest message
    enable_auto_commit=True,  # Automatically commit offsets
    group_id='my-group',  # Consumer group ID
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Decode messages as strings
)

model = tf.keras.models.load_model('models/lap-time-model.keras')
led = joblib.load('models/led.pkl')
let = joblib.load('models/let.pkl')
print("Starting the consumer. Listening for messages...")

def denormalise(prediction):
    with open('models/normalised_max_min.json') as json_file:
        normalised_max_min = json.load(json_file)
    return prediction*(normalised_max_min['LapTime']['max']-normalised_max_min['LapTime']['min']) + normalised_max_min['LapTime']['min']

def predict(row):
    input_data = pd.DataFrame([row])
    input_data['Driver_encoded'] = led.transform(input_data['Driver'])
    input_data['Team_encoded'] = let.transform(input_data['Team'])
    X_driver = input_data['Driver_encoded'].values.astype(np.int32)
    X_team = input_data['Team_encoded'].values.astype(np.int32)
    X_numerical = input_data.drop(columns=["Driver", "Team", "Driver_encoded", "Team_encoded"]).values.astype(np.float32)
    prediction = model.predict([X_driver, X_team, X_numerical])
    return denormalise(prediction[0][0])

def normalise(data):
    with open('models/normalised_max_min.json') as json_file:
        normalised_max_min = json.load(json_file)
    for key, value in data.items():
        if key in normalised_max_min:
            data[key] = (value - normalised_max_min[key]['min']) / (normalised_max_min[key]['max'] - normalised_max_min[key]['min'])
    return data


while True:
    for message in consumer:
        lap_data = message.value
        print(f"Received message")
        print(message)
        lap_data = normalise(lap_data)
        
        print(model)
        prediction = predict(pd.DataFrame(lap_data, index=[0]).iloc[0])
        print(prediction)
        payload = {"prediction": f"{prediction}", "lap_data": lap_data}
        print(payload)
        
        try:
            response = requests.post(f"http://api:3000/receive_prediction", json=payload)  # Send prediction to the Flask app
            if response.status_code == 200:
                print("Prediction sent to Flask app successfully.")
            else:
                print(f"Failed to send prediction to Flask app: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending prediction to Flask app: {e}")

        print(f"Predicted lap time: {prediction}")  # Adjust based on your model's output
