from flask import Flask, render_template, request
from flask_socketio import SocketIO
import logging
import signal
import sys

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow broadcast to dashboard
logging.basicConfig(level=logging.INFO)

# 🧠 In-memory buffer for GPS data during shutdown
buffer = []
flush_buffer = True
last_gps_packet = None  # 🔍 Store most recent GPS ping for diagnostics

@app.route('/')
def index():
    return render_template('map.html')  # Could be gps-map.html if renamed

@app.route('/gps', methods=['POST'])
def gps():
    global last_gps_packet
    data = request.get_json()
    last_gps_packet = data  # 📌 Update latest packet

    logging.info("📡 Received GPS via Fly relay: %s", data)

    if flush_buffer:
        socketio.emit('gps_update', data)
    else:
        buffer.append(data)
        logging.info("⏸️ Buffering GPS packet (shutdown in progress)")

    return {'status': 'received'}

@app.route('/last', methods=['GET'])
def last():
    if last_gps_packet:
        return last_gps_packet
    return {'status': 'no data received'}

# 🧹 Graceful shutdown: flush GPS buffer
def handle_sigterm(*args):
    global flush_buffer
    flush_buffer = False
    logging.info("🛑 SIGTERM received: flushing buffered GPS data")

    for entry in buffer:
        socketio.emit('gps_update', entry)

    logging.info(f"✅ Flushed {len(buffer)} buffered entries before exit")
    sys.exit(0)

# Register SIGTERM handler
signal.signal(signal.SIGTERM, handle_sigterm)

# 🚀 Launch the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
