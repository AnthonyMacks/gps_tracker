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
    socketio.emit('gps_update', data)
    return {'status': 'received'}
@socketio.on('gps_update')
def handle_gps(data):
    print("Received GPS via Socket:", data)

if __name__ == '__main__':
    socketio.run(app)
