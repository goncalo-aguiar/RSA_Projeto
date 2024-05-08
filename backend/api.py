from flask import Flask, jsonify , request
import paho.mqtt.client as mqtt
import json
from time import sleep
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

boats = {}  # Dictionary to store boat positions

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("nodes/#")

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    # Assuming message payload is JSON containing id and position
    data = json.loads(msg.payload)
    boats[data['id']] = data['location']

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.2", 1883, 60)  # Connect to the MQTT broker
client.loop_start()  # Start the loop to process callbacks

@app.route('/api/boats', methods=['GET'])
def get_boats():
    return jsonify(boats)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
