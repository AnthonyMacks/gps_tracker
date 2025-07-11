import time
import requests

# Your Flask server endpoint
url = "http://127.0.0.1:5000/gps"

# Simulated GPS points (Sydney area)
gps_points = [
    {"latitude": "-33.865143", "longitude": "151.209900"},
    {"latitude": "-33.866000", "longitude": "151.210500"},
    {"latitude": "-33.866800", "longitude": "151.211200"},
    {"latitude": "-33.867500", "longitude": "151.212000"},
    {"latitude": "-33.868200", "longitude": "151.212800"},
    {"latitude": "-33.868900", "longitude": "151.213600"},
    {"latitude": "-33.869600", "longitude": "151.214400"},
    {"latitude": "-33.870300", "longitude": "151.215200"},
    {"latitude": "-33.871000", "longitude": "151.216000"},
    {"latitude": "-33.871700", "longitude": "151.216800"}
]

# Send each point with a timestamp
for i, point in enumerate(gps_points):
    payload = {
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "timestamp": time.strftime("%Y%m%d%H%M%S", time.localtime()),
        "speed": "0.00",
        "satellites": "7"
    }
    print(f"Sending point {i+1}: {payload}")
    try:
        response = requests.post(url, json=payload)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Error:", e)
    time.sleep(1)  # Wait 1 second between points