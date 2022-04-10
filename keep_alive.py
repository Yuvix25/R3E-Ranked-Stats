from threading import Thread
import json
from flask import Flask, render_template

import pandas as pd
from pandas_highcharts.core import serialize

from utils import *

app = Flask(__name__)

def convert_timezone(t): # convert GMT to CET
    return int(t) + 3600 * 2

def create_chart():
    data = read_chart_data()

    smoothened = smoothen([x[0] for x in data.values()])
    s = [[convert_timezone(x[0]), x[1][0], smoothened[i], *x[1][1:]] for i, x in enumerate(data.items())]
    cols = ['dt', 'total', 'Smooth-total', 'rook', 'am', 'pro', 'eu', 'us', 'oc', 'rook-eu', 'rook-us', 'rook-oc', 'am-eu', 'am-us', 'am-oc', 'pro-eu', 'pro-us', 'pro-oc']
    df = pd.DataFrame(s, columns=cols)
    df.dt = df.dt.astype('datetime64[s]')
    df = df.set_index('dt')
    chart = json.loads(serialize(df, render_to='my-chart', output_type='json', title='Player Count'))
    if len(chart['series']) > 0:
        # chart['series'][0]['name'] = 'Player Count'
        chart['series'].sort(key=lambda x: cols.index(x['name']))
        for i in range(len(chart['series'])):
            chart['series'][i]['name'] = chart['series'][i]['name'].replace('-', ' ').replace('eu', 'Europe').replace('us', 'America').replace('oc', 'Oceania').replace('rook', 'Rookie').replace('am', 'Amateur').replace('pro', 'Pro').replace('total', 'Total')
            if chart['series'][i]['name'] == 'Smooth Total':
                chart['series'][i]['showInLegend'] = False
                # chart['series'][i]['zIndex'] = -1
                chart['series'][i]['color'] = '#878787'
        chart['xAxis']['title']['text'] = 'Time (CET)'
    return json.dumps(chart)


@app.route('/')
def index():
    return render_template('index.html', chart=create_chart())

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()