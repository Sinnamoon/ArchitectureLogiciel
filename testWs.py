import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def carPosition(data):  # Add 'data' as an argument
    print('Car position received:', data)  # Print the received data
    return "OK"


sio.connect('ws://10.31.33.62:3001', headers={'App-id': '60e3f3d8b5e9c6a5d8f4b0c5'})
sio.wait()
print(sio.emit(carPosition))
