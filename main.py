import time
import json
import requests
from keep_alive import keep_alive
from utils import *

url = 'https://game.raceroom.com/multiplayer-rating/servers/'

def get_servers():
    return requests.get(url).json()['result']

def save_data(servers):
    data = read_data()
    timestamp = str(round(time.time()))
    data[timestamp] = []

    player_count = 0
    for server in servers:
        server_data = pack_server_data(server)
        player_count += server_data[0]
        if server_data[0] > 0:
            data[timestamp].append(server_data)

    json.dump(data, open('data.json', 'w'))
    return player_count


keep_alive()
while True:
    servers = get_servers()
    player_count = save_data(servers)
    print(f'{player_count} players online')
    # save_data(player_count)

    time.sleep(5 * 60)