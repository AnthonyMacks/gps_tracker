from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import signal
import sys
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Use environment variables for production security
users = {
    os.environ.get("AUTH_USERNAME"): generate_password_hash(os.environ.get("AUTH_PASSWORD"))
}

@auth.verify_password
def verify_password(username,password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, you are logged in!."

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# 📜 Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 🧠 State management
buffer = []
flush_buffer = True
last_gps_packet = None

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/gps", methods=["POST"])
def gps():
    global last_gps_packet
    data = request.get_json()

    if not data or "latitude" not in data or "longitude" not in data or "device_id" not in data:
        logging.warning("⚠️ Invalid GPS payload: %s", data)
        return jsonify({"error": "Invalid GPS data"}), 400

    last_gps_packet = data
    logging.info("📡 Received GPS via Fly relay: %s", data)

    if flush_buffer:
        socketio.emit("gps_update", data)
    else:
        buffer.append(data)
        logging.info("⏸️ Buffering GPS packet (shutdown in progress)")

    return jsonify({"status": "received"}), 200

@app.route("/last", methods=["GET"])
def last():
    if last_gps_packet:
        return jsonify(last_gps_packet)
    return jsonify({"status": "no data received"}), 200

# 🧹 Graceful shutdown
def handle_sigterm(*args):
    global flush_buffer
    flush_buffer = False
    logging.info("🛑 SIGTERM received: flushing buffered GPS data")

    for entry in buffer:
        socketio.emit("gps_update", entry)

    logging.info(f"✅ Flushed {len(buffer)} buffered entries before exit")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

# 🚀 Launch with correct Render port
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))  # Render binds to $PORT
    socketio.run(app, host="0.0.0.0", port=PORT)



