from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('map.html')

import logging
logging.basicConfig(level=logging.INFO)

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    logging.info("📡 Received GPS: %s", data)
    socketio.emit('gps_update', data)
    return {'status': 'received'}
