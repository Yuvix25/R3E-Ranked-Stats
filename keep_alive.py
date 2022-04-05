from threading import Thread
import json
import pytz
from flask import Flask, render_template

import pandas as pd
from pandas_highcharts.core import serialize

from utils import *

app = Flask(__name__)
cet = pytz.timezone('CET')

def convert_timezone(t): # convert GMT to CET
    return int(t) + 3600 * 2

def create_chart():
    data = read_chart_data()


    s = list(map(lambda x: [convert_timezone(x[0]), *x[1]], data.items()))
    cols = ['dt', 'total', 'rook', 'am', 'pro', 'eu', 'us', 'oc', 'rook-eu', 'rook-us', 'rook-oc', 'am-eu', 'am-us', 'am-oc', 'pro-eu', 'pro-us', 'pro-oc']
    df = pd.DataFrame(s, columns=cols)
    df.dt = df.dt.astype('datetime64[s]')
    df = df.set_index('dt')
    chart = json.loads(serialize(df, render_to='my-chart', output_type='json', title='Player Count'))
    if len(chart['series']) > 0:
        # chart['series'][0]['name'] = 'Player Count'
        chart['series'].sort(key=lambda x: cols.index(x['name']))
        for i in range(len(chart['series'])):
            chart['series'][i]['name'] = chart['series'][i]['name'].replace('-', ' ').replace('eu', 'Europe').replace('us', 'America').replace('oc', 'Oceania').replace('rook', 'Rookie').replace('am', 'Amateur').replace('pro', 'Pro').replace('total', 'Total')
        chart['xAxis']['title']['text'] = 'Time (CET)'
    return json.dumps(chart)

    
    # s = list(map(lambda x: [convert_timezone(x[0]), x[1]], data.items()))
    # df = pd.DataFrame(s, columns=['dt', 'cnt'])
    # df.dt = df.dt.astype('datetime64[s]')
    # df = df.set_index('dt')
    # chart = json.loads(serialize(df, render_to='my-chart', output_type='json', title='Player Count'))
    # if len(chart['series']) > 0:
    #     chart['series'][0]['name'] = 'Player Count'
    #     chart['xAxis']['title']['text'] = 'Time (CET)'
    # return json.dumps(chart)


@app.route('/')
def index():
    return render_template('index.html', chart=create_chart())

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()