from flask import Flask, render_template, request
from flask_socketio import SocketIO
import logging
import signal
import sys

app = Flask(__name__)
socketio = SocketIO(app)
logging.basicConfig(level=logging.INFO)

# 🧠 In-memory buffer for GPS data during shutdown
buffer = []
flush_buffer = True

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    logging.info("📡 Received GPS: %s", data)

    if flush_buffer:
        socketio.emit('gps_update', data)
    else:
        buffer.append(data)
        logging.info("⏸️ Buffering GPS packet (shutdown in progress)")

    return {'status': 'received'}

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
