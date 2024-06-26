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
    global flag

    if data["type"] == "boat":
        if data["id"] != boat_id:
            distOtherMessage = calculateDistance(current_location, data['location'])
            if distOtherMessage <= 6 and flag != "acabou" and flag != "goingTo00":
                for x in data["visited_locations"]:
                    if x not in visited_locations:
                        visited_locations.append(x)
                
                if data["intention"] != [] and intention != []:
                    other_boat_intention = data["intention"]
                    if (other_boat_intention == intention) and other_boat_intention not in boias_limpas.values():
                        other_boat_location = data["location"]
                        distOtherBoat = calculateDistance(other_boat_location, data["intention"][2])
                        distThisBoat = calculateDistance(current_location, data["intention"][2])
                        if distOtherBoat <= distThisBoat:
                            boias_limpas[data["intention"][0]] = data["intention"][1]
                            intention = []
                        else:
                            intention = data["intention"]
                else:
                    for key, value in data["learning"].items():
                        if key not in boias_limpas and value != data["intention"] :
                            boias_limpas[key] = value
                            

    elif data["type"] == "boia":
        distOtherMessage = calculateDistance(current_location, data['location'])
        if distOtherMessage <= 5:
            #print(f"Message from {msg.topic}: {data}", distOtherMessage)
            if data["status"] == "dirty" and intention == [] :
                intention = [data["id"], data["location"], data["trash_location"]]
                #print("intention", data["id"])
            if data["status"] == "clean"   :
                boias_limpas[data["id"]] = data["location"]
                #print(intention)
                #print(data["id"], data["location"], data["trash_location"])
                if intention != []:
                    if intention[0] == data["id"]:
                        intention = []

                for key, value in data["learning"].items():
                    if key not in boias_limpas  :
                        boias_limpas[key] = value
                
                    
            
            

def generate_random_coordinates_Search(current_location,threshold):
    radius = 1
    max_radius = max(100, 49)  # Ensures the radius does not go beyond the grid limits
    
    
    while radius <= max_radius:
        surrounding_coords = [
            [current_location[0] + dx, current_location[1] + dy]
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
            if (dx != 0 or dy != 0) and (0 <= current_location[0] + dx <= 100) and (0 <= current_location[1] + dy <= 49)
        ]

        unvisited_coords = [loc for loc in surrounding_coords if loc not in visited_locations]
        
        valid_coords = [loc for loc in unvisited_coords if has_sufficient_unvisited_neighbors(loc, threshold)]
        
        if valid_coords:
            return random.choice(valid_coords)
        radius += 1
    
    return []

def generate_random_coordinates():
    x = random.uniform(0, 100)
    y = random.uniform(0, 49)
    return [int(x), int(y)]

def get_surrounding_coordinates(center):
    x, y = center
    surrounding_coords = []
    radius = 3
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            surrounding_coords.append([x+i, y+j])
    return surrounding_coords

def is_on_path_to_origin(current_location, buoy_location, tolerance):
   
    if buoy_location == [0, 0]:
        return False
    
    
    dx1, dy1 = buoy_location[0] - current_location[0], buoy_location[1] - current_location[1]
    dx2, dy2 = 0 - buoy_location[0], 0 - buoy_location[1]
    cross_product = abs(dx1 * dy2 - dy1 * dx2)
    
    # Calculate distances
    distance_current_to_buoy = calculateDistance(current_location, buoy_location)
    distance_buoy_to_origin = calculateDistance(buoy_location, [0, 0])
    
    # Check if the buoy is on the approximate straight path to [0,0]
    return cross_product < tolerance and distance_current_to_buoy + distance_buoy_to_origin >= calculateDistance(current_location, [0, 0]) - tolerance
def has_sufficient_unvisited_neighbors(location, threshold):
    surrounding = get_surrounding_coordinates(location)
    unvisited_count = 0
    for coord in surrounding:
        if coord not in visited_locations and is_within_valid_range(coord):
            unvisited_count += 1
    return unvisited_count >= threshold

def is_within_valid_range(coordinate):
    x, y = coordinate
    return 0 <= x <= 100 and 0 <= y <= 49
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
        current_location = [new_x, new_y]  # Update current location as a tuple
        return False
    else:
        return True

def send_message(client, topic, message):
    client.publish(topic, json.dumps(message))

if len(sys.argv) < 3:
    print("Usage: python script.py <broker_ip> <boat_id> <loc_inicial_x> <loc_inicial_y> <num_boias>")
    sys.exit(1)

own_ip = sys.argv[1]
boat_id = sys.argv[2]

current_location = [int(sys.argv[3]),int(sys.argv[4])]

new_location = []
intention = []

boias_limpas = {}
status = "procurando"
visited_locations = list()
broker_ip = "192.168.1.2"
#broker_ip = "localhost"

num_boias = int(sys.argv[5])

client = mqtt.Client(client_id=boat_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)

flag = ""
last_intention = []
threading.Thread(target=client.loop_start).start()

while True:

    send_message(client, f"nodes/{boat_id}", {
        "type": "boat",
        "id": boat_id,
        "intention": intention,
        "location": current_location,
        "status": status,
        "learning": boias_limpas,
        "visited_locations": visited_locations
    })

    

    if intention != []:
        goTo(intention[2])
        status = "recolhendo"
        last_intention = intention
    else:
        if new_location == current_location or new_location == []:
            # print(len(boias_limpas),num_boias)
            if flag != "acabou" and flag != "goingTo00":
                if len(boias_limpas) == num_boias or len(visited_locations) >= 5050 :
                    near_buoys = {}

                    for key, value in boias_limpas.items():
                       
                        distance = calculateDistance(current_location, value)
                        if distance < 25  :
                            
                            near_buoys[key] = value

                    if near_buoys:
                        
                        random_key = random.choice(list(near_buoys.keys()))

                        
                        random_value = near_buoys[random_key]

                        
                        id = random_key
                        new_location = random_value

                        print("goingto ",random_key)
                        flag = "acabou"
                    else:
                        flag = "goingTo00"
                    
                else:
                    new_location = generate_random_coordinates_Search(current_location,15)
                    
                    while(new_location == []):
                        if(num_boias == len(boias_limpas) ):
                            break
                        new_location = generate_random_coordinates_Search(current_location,5)
                        
                    
            else:
                if flag == "goingTo00":
                    new_location = [0,0]
                    if current_location == new_location:
                        
                        sys.exit(0)
                elif flag == "acabou":
                    
                    if current_location == new_location:
                        flag = "goingTo00"
                    




        goTo(new_location)
        
        status = "procurando"

    surrounding = get_surrounding_coordinates(current_location)
    if current_location not in visited_locations and is_within_valid_range(current_location):
        visited_locations.append(current_location)
    for x in surrounding:
        if x not in visited_locations and is_within_valid_range(x):
            visited_locations.append(x)
    
    
    
    time.sleep(0.6)
