from flask import Flask, jsonify , request
import paho.mqtt.client as mqtt
import json
from time import sleep
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

boats = {}
buoys = {}  # Dictionary to store boat positions
trash_location = {}


visited_locations_set = list()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("nodes/#")

def on_message(client, userdata, msg):
    #print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    # Assuming message payload is JSON containing id and position
    data = json.loads(msg.payload)
    
    
    if data['type'] == "boia":
        buoys[data['id']] = [data['type'],data['location']]
        trash_location[data['id']] = [data['type'],data['trash_location']]
    else:
        boats[data['id']] = [data['type'],data['location'],data['intention']]

        if data['id'] == '4':
            for x in data["visited_locations"]:
                if x not in visited_locations_set:
                    visited_locations_set.append(x)
        
        
    
    

        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)  # Connect to the MQTT broker
client.loop_start()  # Start the loop to process callbacks

@app.route('/api/boats', methods=['GET'])
def get_boats():
    return jsonify(boats)


@app.route('/api/buoys', methods=['GET'])
def get_buoys():
    return jsonify(buoys)

@app.route('/api/trash', methods=['GET'])
def get_trash():
    return jsonify(trash_location)


@app.route('/api/visited', methods=['GET'])
def get_visited():
    print(visited_locations_set)

    return jsonify(visited_locations_set)





if __name__ == '__main__':
    app.run(debug=True, port=8080)
