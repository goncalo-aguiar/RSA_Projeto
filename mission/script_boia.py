import math
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

def calculateDistance(loc1, loc2):
    xLoc1 = loc1[0]
    xLoc2 = loc2[0]
    yLoc1 = loc1[1]
    yLoc2 = loc2[1]
    return ((xLoc2 - xLoc1)**2 + (yLoc2 - yLoc1)**2)**0.5

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))

    global time_being_cleaned
    global initial_location
    global status
    global trash_location
    
    
    if data["type"] == "boat":
        distOtherMessage = calculateDistance(initial_location,data['location'])
        if distOtherMessage <=5:
            #print(f"Message from {msg.topic}: {data}")
        
            if data["location"] == trash_location:
                time_being_cleaned = time_being_cleaned+1
            
            if time_being_cleaned >= 5:
                status= "clean"
                time_being_cleaned = 0
                trash_location = []

            for key, value in data["learning"].items():
                if key not in boias_limpas and value != data["intention"] :
                    boias_limpas[key] = value

    elif data["type"] == "boia":
        if data["id"] != boia_id:
            distOtherMessage = calculateDistance(initial_location,data['location'])
            if distOtherMessage <=5:
                print(f"Message from {msg.topic}: {data}")
                for key, value in data["learning"].items():
                    if key not in boias_limpas and data["status"] == "clean" :
                        boias_limpas[key] = value
                    


               
               
                
               
                
                

                



def send_message(client, topic, message):
    client.publish(topic, json.dumps(message))

def generate_random_coordinates():
    
    x = random.uniform(0, 100)
    
    y = random.uniform(0, 49)
    return [int(x),int(y)]


def generate_random_coordinates_trash(initial_location, radius):
    angle = random.uniform(0, 2 * math.pi)
    max_distance = min(radius, min(abs(initial_location[0] - 0), abs(initial_location[0] - 100)), 
                               min(abs(initial_location[1] - 0), abs(initial_location[1] - 49)))
    distance = random.uniform(0, max_distance)
    
    # Generate random coordinates around the center
    x_offset = distance * math.cos(angle)
    y_offset = distance * math.sin(angle)
    
    # Calculate the new coordinates
    x_new = initial_location[0] + x_offset
    y_new = initial_location[1] + y_offset
    
    return [int(x_new), int(y_new)]


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
#broker_ip = "localhost"
client.connect(broker_ip, 1883, 60)

time_being_cleaned = 0
status = "dirty"

boias_limpas = {}

initial_location = generate_random_coordinates()

trash_location = generate_random_coordinates_trash(initial_location,2)


threading.Thread(target=client.loop_start).start()

while True:
    send_message(client, f"nodes/{boia_id}", {"type":"boia","id": boia_id,"location":initial_location,"status":status,"trash_location":trash_location,"learning":boias_limpas})
    time.sleep(1)

