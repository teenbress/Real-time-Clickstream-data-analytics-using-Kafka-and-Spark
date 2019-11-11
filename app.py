import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
consumer = KafkaConsumer('result')


def background_thread():
    female = 0
    male = 0
    for msg in consumer:
        data_json = msg.value.decode('utf8')
        data_list = json.loads(data_json)
        for data in data_list:
            if '0' in data.keys():
                female = data['0']
            elif '1' in data.keys():
                male = data['1']
            else:
                continue
        result = str(female) + ',' + str(male)
        print(result)
        socketio.emit('test_message',{'data':result})


@socketio.on('test_connect')
def connect(message):
    print(message)
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    print('connected', 'data' 'Connected')
    socketio.emit('connected', {'data': 'Connected'})


@app.route("/")
def handle_mes():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app,debug=True)