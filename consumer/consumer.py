from kafka import KafkaConsumer
import os
import tensorflow as tf
import numpy as np
import json
import pandas as pd
import requests

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

model = tf.keras.models.load_model('models/lap_time_prediction_model.keras')

print("Starting the consumer. Listening for messages...")

while True:
        for message in consumer:
            lap_data = message.value
            print(f"Received message")
            print(message)
            

            input_data = np.array(list(lap_data.values())).reshape(1, -1)
            

            prediction = model.predict(input_data)
            payload = {"prediction": f"{prediction[0][0].tolist()}", "lap_data": lap_data}
            
            try:
                response = requests.post(f"http://app:3000/receive_prediction", json=payload)  # Send prediction to the Flask app
                if response.status_code == 200:
                    print("Prediction sent to Flask app successfully.")
                else:
                    print(f"Failed to send prediction to Flask app: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending prediction to Flask app: {e}")

            print(f"Predicted lap time: {prediction[0][0]}")  # Adjust based on your model's output
