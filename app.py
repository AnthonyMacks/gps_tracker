from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    print("📡 Received GPS:", data)
    socketio.emit('gps_update', data)
    return {'status': 'received'}

if __name__ == '__main__':
    socketio.run(app)