from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/gps', methods=['POST'])
def receive_gps():
    try:
        # Print raw JSON payload as received
        raw_payload = request.data.decode('utf-8')
        print("🔹 Raw payload received:", raw_payload)

        # Parse payload
        data = request.get_json(force=True)

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        timestamp = data.get("timestamp")
        speed = data.get("speed")
        satellites = data.get("satellites")

        # Print parsed fields
        print("📡 Parsed GPS Data:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Timestamp: {timestamp}")
        print(f"Speed (km/h): {speed}")
        print(f"Satellites: {satellites}")
        print("-" * 40)

        # Broadcast to connected browser clients
        socketio.emit('gps_update', data)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ Error parsing GPS data:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    print("🚀 Flask server with Socket.IO is running...")
    socketio.run(app, host='0.0.0.0', port=5000)