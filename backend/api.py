from flask import Flask, jsonify , request
import paho.mqtt.client as mqtt
import json
from time import sleep
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

boats_buoys = {}  # Dictionary to store boat positions
trash_location = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("nodes/#")

def on_message(client, userdata, msg):
    #print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    # Assuming message payload is JSON containing id and position
    data = json.loads(msg.payload)
    
    boats_buoys[data['id']] = [data['type'],data['location']]
    if data['type'] == "boia":
        trash_location[data['id']] = [data['type'],data['trash_location']]

        print(trash_location)
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)  # Connect to the MQTT broker
client.loop_start()  # Start the loop to process callbacks

@app.route('/api/boats_buoys', methods=['GET'])
def get_boats():
    return jsonify(boats_buoys)

@app.route('/api/trash', methods=['GET'])
def get_buoys():
    return jsonify(trash_location)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
