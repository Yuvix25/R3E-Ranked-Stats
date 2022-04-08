import os
import time
import json
import requests


LEVELS = {
    0  : 0, # Rookie
    75 : 1, # Amateur
    80 : 2, # Pro
}

R3E_DATA_URL = 'https://raw.githubusercontent.com/sector3studios/r3e-spectator-overlay/master/r3e-data.json'
R3E_DB = None

LID_BLACKLIST = set()


def update_r3e_db():
    global R3E_DB
    R3E_DB = requests.get(R3E_DATA_URL).json()

def get_track_data(tid):
    """
    lid - track layout Id.

    returns: track, track_layout dicts.
    """

    for track_id in R3E_DB["tracks"]:
        for layout in R3E_DB["tracks"][track_id]["layouts"]:
            if layout["Id"] == tid:
                track = R3E_DB["tracks"][track_id]

                return [track, layout]
    
    print(f"Track {tid} not found")
    return [None, None]


def get_car_data_by_livery(lid):
    """
    lid - livery Id.

    returns: car, car_class dicts.
    """

    def livery_find_loop():
        for car_id in R3E_DB["cars"]:
            for livery in R3E_DB["cars"][car_id]["liveries"]:
                if livery["Id"] == lid:
                    return [R3E_DB["cars"][car_id], car_id]
        return [None, None]
    

    car, _ = livery_find_loop()
    
    if car is None:
        print(f"Livery {lid} not found, skipping")
        LID_BLACKLIST.add(lid)
    
    car_class = R3E_DB["classes"][str(car["Class"])]

    return [car, car_class]


def get_class_list(server):
    classes = set()

    if 'Server' in server:
        server = server['Server']
    lids = server["Settings"]["LiveryId"]

    found_liveries = set()
    for lid in lids:
        if lid not in found_liveries and lid not in LID_BLACKLIST:
            car, car_class = get_car_data_by_livery(lid)
            if car is not None:
                classes.add(car_class["Name"])
                
                for car_id in car_class["Cars"]:
                    car_id = str(car_id["Id"])
                    liveries = R3E_DB["cars"][car_id]["liveries"]
                    
                    for livery in liveries:
                        found_liveries.add(livery["Id"])
    
    return list(classes)


def get_level(server):
    if 'Server' in server:
        server = server['Server']
    
    min_rep = server["Settings"]["MinReputation"]
    if min_rep in LEVELS:
        return LEVELS[min_rep]
    else:
        # get closest level
        keys = list(LEVELS.keys())
        keys.sort()
        for i in range(len(keys)):
            if keys[i] > min_rep:
                return LEVELS[keys[i - 1]]
        return LEVELS[keys[-1]]


def get_region(server):
    if 'Server' in server:
        server = server['Server']
    
    server_name = server["Settings"]["ServerName"]
    if 'europe' in server_name.lower():
        return 0
    elif 'america' in server_name.lower():
        return 1
    elif 'oceania' in server_name.lower():
        return 2
    return -1


def pack_server_data(server):
    if 'Server' in server:
        server = server['Server']
    
    update_r3e_db()

    track_data = get_track_data(server["Settings"]["TrackLayoutId"][0])

    return [
        server["PlayersOnServer"],
        get_level(server),
        get_region(server),
        get_class_list(server),
        [track_data[0]["Name"], track_data[1]["Name"]]
    ]
    
    return {
        'player_count' : server["PlayersOnServer"],
        'level' : get_level(server),
        'region' : get_region(server),
        'classes' : get_class_set(server),
        'track' : get_track_data(server["Settings"]["TrackLayoutId"][0])
    }



def read_data():
    if not os.path.isfile('data.json'):
        data = {}
    else:
        try:
            data = json.load(open('data.json'))
        except:
            time.sleep(0.5)
            data = json.load(open('data.json'))
            
    return data

def read_chart_data():
    data = read_data()

    minimized_data = {}
    for timestamp in data:
        total_players = 0
        
        player_counts = [0] * (3 + len(LEVELS) + 3 * len(LEVELS) + 1)

        for server in data[timestamp]:
            player_counts[server[1]*3 + server[2] + 3 + len(LEVELS) + 1] += server[0]
            player_counts[server[1] + 1] += server[0]
            player_counts[server[2] + 3 + 1] += server[0]
            total_players += server[0]
        
        player_counts[0] = total_players
        
        minimized_data[timestamp] = player_counts

    return minimized_data