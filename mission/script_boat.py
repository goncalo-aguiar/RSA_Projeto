import random
import sys
import paho.mqtt.client as mqtt
import threading
import json
import time



global broker_ip
global boat_id
 
global status


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
    client.subscribe("nodes/#")
    

def calculateDistance(loc1, loc2):
    xLoc1 = loc1[0]
    xLoc2 = loc2[0]
    yLoc1 = loc1[1]
    yLoc2 = loc2[1]
    return ((xLoc2 - xLoc1)**2 + (yLoc2 - yLoc1)**2)**0.5

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))
    global intention 
    global boias_limpas
    
    if data["type"] == "boat":
        
        if data["id"] != boat_id:
            print(f"Message from {msg.topic}: {data}")
            if data["intention"] != [] and intention != [] :

                
                other_boat_intention =  data["intention"][1]
                if (other_boat_intention == intention[1]) and other_boat_intention not in boias_limpas.values():
                    other_boat_location = data["location"]
                    distOtherBoat = calculateDistance(other_boat_location, other_boat_intention)
                    distThisBoat = calculateDistance(current_location, other_boat_intention)

                    print("DISTANCE OUTRO BARCO " + str(other_boat_location) + " " + str(other_boat_intention) + " "  + str(distOtherBoat) )
                    print("DISTANCE ESTE BARCO " +  str(current_location) + " " +  str(intention[1]) + " " + str(distThisBoat))
                    if  distOtherBoat <= distThisBoat:
                        print("LIMPEI")
                        boias_limpas[data["intention"][0]] = data["intention"][1]
                        intention = []
                        
                        
                    else:
                        intention = data["intention"] 
        
    elif data["type"] == "boia":
            print(f"Message from {msg.topic}: {data}")
            if data["status"] == "dirty" and intention == [] and data["location"] not in boias_limpas.values() :
                    intention = [data["id"],data["location"]]

            if data["status"] == "clean":
                if data["location"][1] not in boias_limpas.values() :
                   boias_limpas[data["id"]] = data["location"]


def generate_random_coordinates():
    
    x = random.uniform(0, 15)
    
    y = random.uniform(0, 15)
    return [int(x),int(y)]


def goTo(coordinates):

    global current_location
        
    if current_location != coordinates:
        
        if current_location[0] < coordinates[0]:
            new_x = current_location[0] + 1
        elif current_location[0] > coordinates[0]:
            new_x = current_location[0] - 1
        else:
            new_x = current_location[0]

        
        if current_location[1] < coordinates[1]:
            new_y = current_location[1] + 1
        elif current_location[1] > coordinates[1]:
            new_y = current_location[1] - 1
        else:
            new_y = current_location[1]

        current_location = [new_x, new_y]
        return False
    else:
        return True



def send_message(client, topic, message):
    client.publish(topic, json.dumps(message))



if len(sys.argv) < 3:
    print("Usage: python script.py <broker_ip> <boat_id>")
    sys.exit(1)


own_ip = sys.argv[1]
boat_id = sys.argv[2]

intention = []
current_location = generate_random_coordinates()
boias_limpas = {}

status = "procurando"



broker_ip = "192.168.1.2"

client = mqtt.Client(client_id=boat_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)


threading.Thread(target=client.loop_start).start()

while True:
    send_message(client, f"nodes/{boat_id}", {"type":"boat","id": boat_id,"intention":intention,"location":current_location,"status":status,"learning":boias_limpas})

    if intention != []:
        
        goTo(intention[1])
        status = "recolhendo"
    else:
        status = "procurando"
    


    time.sleep(5)


    