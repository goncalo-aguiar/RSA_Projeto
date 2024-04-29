import sys
import paho.mqtt.client as mqtt
import threading
import json
import time

import random




def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all subtopics under nodes
    client.subscribe("nodes/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))

    global time_being_cleaned
    global initial_location
    global status
    
    if data["type"] == "boat":
        print(f"Message from {msg.topic}: {data}")
        print(time_being_cleaned)
        if data["location"] == initial_location:
            time_being_cleaned = time_being_cleaned+1
        
        if time_being_cleaned >= 3:
            status= "clean"
            time_being_cleaned = 0
        print(initial_location)
        print(data["location"])


    elif data["type"] == "boia":
        if data["id"] != boia_id:
            print(f"Message from {msg.topic}: {data}")



def send_message(client, topic, message):
    client.publish(topic, json.dumps(message))

def generate_random_coordinates():
    
    x = random.uniform(0, 7)
    
    y = random.uniform(0, 7)
    return [int(x),int(y)]


if len(sys.argv) < 3:
    print("Usage: python script.py <broker_ip> <boia_id>")
    sys.exit(1)


global boia_id 
own_ip = sys.argv[1]
boia_id = sys.argv[2]
client = mqtt.Client(client_id=boia_id)
client.on_connect = on_connect
client.on_message = on_message


broker_ip = "192.168.1.2"
client.connect(broker_ip, 1883, 60)

time_being_cleaned = 0
status = "dirty"


initial_location = generate_random_coordinates()


threading.Thread(target=client.loop_start).start()

while True:
    send_message(client, f"nodes/{boia_id}", {"type":"boia","id": boia_id,"location":initial_location,"status":status})
    time.sleep(5)

