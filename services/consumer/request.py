import requests
import time

# Define the payload with lap data
payload = {
    "lap_data": {
        'Driver': 'VER',
        'SpeedAfterSector1': 0.47755102040816333,
        'SpeedAfterSector2': 0.5536480686695279,
        'SpeedAtFinishLine': 0.56,
        'IsPersonalBest': 1,
        'FreshTyre': 0,
        'Team': 'Red Bull Racing',
        'Humidity': 0.0655737704918033,
        'Rainfall': 0,
        'Speed_min': 0.4366197183098592,
        'RPM_max': 0.45299145299145316,
        'RPM_std': 0.6071919934621487,
        'ContainsTrackStatus1': 1,
        'ContainsTrackStatus2': 1,
        'ContainsTrackStatus4': 0,
        'ContainsTrackStatus6': 0,
        'ContainsTrackStatus7': 0,
        'SpeedAfterSector1IsFast': 0,
        'SpeedAfterSector2IsFast': 0,
        'combo_speed_max_speed_std': 0.13098107071941528,
        'combo_stint_lap_number': 0.0,
        'Compound_HARD': False,
        'Compound_INTERMEDIATE': False,
        'Compound_MEDIUM': False,
        'Compound_SOFT': True,
        'DirectionOfWind_East': False,
        'DirectionOfWind_North': False,
        'DirectionOfWind_South': True,
        'DirectionOfWind_West': False,
        'Pressure_Category_Very Low': False,
        'Pressure_Category_Low': False,
        'Pressure_Category_Normal': True,
        'AirTemp_Category_Cold': False,
        'AirTemp_Category_Normal': False,
        'AirTemp_Category_Hot': True,
        'AirTemp_Category_Very Hot': False,
        'TrackTemp_Category_Cold': False,
        'TrackTemp_Category_Normal': True,
        'TrackTemp_Category_Hot': False,
        'TrackTemp_Category_Very Hot': False,
        'Driver_encoded': 20,
        'Team_encoded': 8
    }
}

# Send a POST request to send the lap data
response = requests.post("http://api:3000/receive_lap_data", json=payload)

if response.status_code == 200:
    print("Lap data sent successfully.")

# Loop to check for predictions
while True:
    try:
        # Send a GET request to fetch the latest prediction
        prediction_response = requests.get("http://api:3000/prediction")
        
        if prediction_response.status_code == 200:
            # Successfully received a prediction
            prediction_data = prediction_response.json()
            print(f"Received prediction: {prediction_data.get('prediction')}")
            break
        elif prediction_response.status_code == 404:
            # Prediction not yet available, wait for 2 seconds
            print("Prediction not found. Retrying in 2 seconds...")
            time.sleep(2)
        else:
            # Handle unexpected status codes
            print(f"Unexpected status code: {prediction_response.status_code}")
            break

    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions
        print(f"Request failed: {e}")
        break
