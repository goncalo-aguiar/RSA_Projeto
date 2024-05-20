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
    global visited_locations
    
    if data["type"] == "boat":
        if data["id"] != boat_id:
            #print(f"Message from {msg.topic}: {data}")
            distOtherMessage = calculateDistance(current_location, data['location'])
            if distOtherMessage <= 5:
                for x in data["visited_locations"]:
                    if x not in visited_locations:
                        visited_locations.append(x)  

                if data["intention"] != [] and intention != []:
                    other_boat_intention = data["intention"][1]
                    if (other_boat_intention == intention[1]) and other_boat_intention not in boias_limpas.values():
                        other_boat_location = data["location"]
                        distOtherBoat = calculateDistance(other_boat_location, data["intention"][2])
                        distThisBoat = calculateDistance(current_location, data["intention"][2])
                        if distOtherBoat <= distThisBoat:
                            boias_limpas[data["intention"][0]] = data["intention"][1]
                            intention = []
                        else:
                            intention = data["intention"]

    elif data["type"] == "boia":
        distOtherMessage = calculateDistance(current_location, data['location'])
        if distOtherMessage <= 3:
            print(f"Message from {msg.topic}: {data}", distOtherMessage)
            if data["status"] == "dirty" and intention == [] and data["location"] not in boias_limpas.values():
                
                intention = [data["id"], data["location"], data["trash_location"]]
                print("intention",data["id"])
            if data["status"] == "clean" and data["location"] not in boias_limpas.values() :
                boias_limpas[data["id"]] = data["location"]
                intention = []
            

def generate_random_coordinates_Search(current_location):
    radius = 1
    max_radius = max(29, 14)  # Ensures the radius does not go beyond the grid limits
    while radius <= max_radius:
        surrounding_coords = [
            (current_location[0] + dx, current_location[1] + dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
            if (dx != 0 or dy != 0) and (0 <= current_location[0] + dx <= 29) and (0 <= current_location[1] + dy <= 14)
        ]

        unvisited_coords = [loc for loc in surrounding_coords if loc not in visited_locations]
        
        if unvisited_coords:
            return random.choice(unvisited_coords)
        radius += 1  # Increase the radius if all surrounding coordinates have been visited
        
    # If all coordinates are visited, return a completely random coordinate

    
    return generate_random_coordinates()

def generate_random_coordinates():
    x = random.uniform(0, 29)
    y = random.uniform(0, 14)
    new_location = (int(x), int(y))
    return new_location

def get_surrounding_coordinates(center):
    x, y = center
    surrounding_coords = [
        (x-1, y-1), (x, y-1), (x+1, y-1),  # Top-left, Top, Top-right
        (x-1, y),             (x+1, y),    # Left,      , Right
        (x-1, y+1), (x, y+1), (x+1, y+1)   # Bottom-left, Bottom, Bottom-right
    ]
    return surrounding_coords

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
        current_location = (new_x, new_y)  # Update current location as a tuple
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

new_location = []
intention = []
current_location = generate_random_coordinates()
boias_limpas = {}
status = "procurando"
visited_locations = list()
broker_ip = "192.168.1.2"
broker_ip = "localhost"

client = mqtt.Client(client_id=boat_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)

threading.Thread(target=client.loop_start).start()

while True:
    send_message(client, f"nodes/{boat_id}", {
        "type": "boat",
        "id": boat_id,
        "intention": intention,
        "location": current_location,
        "status": status,
        "learning": boias_limpas,
        "visited_locations":visited_locations
    })

    if intention != []:
        goTo(intention[2])
        status = "recolhendo"
    else:
        if new_location == current_location or new_location == []:
            new_location = generate_random_coordinates_Search(current_location)
        goTo(new_location)
        status = "procurando"

    surrounding = get_surrounding_coordinates(current_location)
    if current_location not in visited_locations:
        visited_locations.append(current_location)
    for x in surrounding:
        if x not in visited_locations:
            visited_locations.append(x)
    
    time.sleep(2)

    