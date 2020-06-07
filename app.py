import eventlet
# Eventlet isn't compatible with some python modules (e.g. time) so monkeypatch to resolve 
# bugs that result from such conflicts
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from Engine import Engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def get_id_from_sid(sid):
    for c in clients:
        if clients[c]["sid"] == sid:
            return c
    raise ValueError("Invalid sid request")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print(clients)
    print(started)

    clients[len(clients)] = {"sid": request.sid, "response": "No response"}
    print("Client connected")
    print(clients)

@socketio.on('disconnect')
def on_disconnect():
    del clients[get_id_from_sid(request.sid)]
    print("Client disconnected")
    print(clients)

@socketio.on('start game')
def on_start():
    global started
#     global clients
    print(clients)
    if not started:  # Don't allow multiple starts
        print("Starting")
        started = True
        engine = Engine(emit_to_client, lambda msg: send(msg, broadcast=True), retrieve_response, n_players=len(clients))
        winner = engine.run_game()

def emit_to_client(msg, client_id, name=None):
    # Clear response before whispering, to ensure we don't keep a stale one
    clients[client_id]["response"] = "No response"
    if name is None:
        socketio.send(msg, room=clients[client_id]["sid"])
    else:
        emit(name, msg, room=clients[client_id]["sid"])

def retrieve_response(client_id):
    """Get the current stored response corresponding to the requested client."""
    return clients[client_id]["response"]

@socketio.on('action')
def store_action(message):
    print("Got an action: " + message)
    clients[get_id_from_sid(request.sid)]["response"] = message

if __name__ == '__main__':
    started = False
    clients = {} 
    socketio.run(app, host='0.0.0.0')
