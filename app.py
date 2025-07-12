from flask import Flask, render_template, request
from flask_socketio import SocketIO
import logging

app = Flask(__name__)
socketio = SocketIO(app)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    logging.info("📡 Received GPS: %s", data)
    socketio.emit('gps_update', data)
    return {'status': 'received'}
