from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/gps', methods=['POST'])
def receive_gps():
    try:
        data = request.get_json(force=True)

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        timestamp = data.get("timestamp")
        speed = data.get("speed")
        satellites = data.get("satellites")

        print("📡 Received GPS Data:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Timestamp: {timestamp}")
        print(f"Speed (km/h): {speed}")
        print(f"Satellites: {satellites}")
        print("-" * 40)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ Error parsing GPS data:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)