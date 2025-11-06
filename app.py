# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'change-me'
socketio = SocketIO(app, cors_allowed_origins="*")  # dev only

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def on_join(data):
    room = data.get("room")
    join_room(room)
    emit("peer-joined", {"sid": request.sid}, to=room, include_self=False)

@socketio.on("leave")
def on_leave(data):
    room = data.get("room")
    leave_room(room)
    emit("peer-left", {"sid": request.sid}, to=room, include_self=False)

@socketio.on("signal")
def on_signal(data):
    # data: {room, to (optional), type, payload}
    room = data.get("room")
    to_sid = data.get("to")
    if to_sid:
        emit("signal", {"from": request.sid, **data}, to=to_sid)
    else:
        emit("signal", {"from": request.sid, **data}, to=room, include_self=False)

if __name__ == "__main__":
    # For local dev; in prod use gunicorn/eventlet and HTTPS
    socketio.run(app, host="0.0.0.0", port=8080)