import os
import time
import json
import requests
from keep_alive import keep_alive

url = 'https://game.raceroom.com/multiplayer-rating/servers/'

def get_servers():
    return requests.get(url).json()['result']

def save_data(player_count):
    if not os.path.isfile('data.json'):
        data = {}
    
    data = json.load(open('data.json'))
    data[str(round(time.time()))] = player_count
    json.dump(data, open('data.json', 'w'))



keep_alive()
while True:
    servers = get_servers()
    player_count = 0
    for server in servers:
        player_count += server['Server']['PlayersOnServer']
    print(f'{player_count} players online')
    save_data(player_count)

    time.sleep(5 * 60)