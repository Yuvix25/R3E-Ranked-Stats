from threading import Thread
import os
import io
import json
import pytz
from datetime import datetime
from flask import Response, Flask, render_template

import numpy as np
import pandas as pd
from pandas_highcharts.core import serialize
# from pandas_highcharts.display import display_charts
import matplotlib.pyplot as plt

# import pandas as pd
# from pandas_highcharts.display import display_charts

# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt


app = Flask(__name__)
cet = pytz.timezone('CET')

def convert_timezone(t): # convert GMT to CET
    return int(t) + 3600 * 2

def create_chart():
    if not os.path.isfile('data.json'):
        data = {}
    else:
        data = json.load(open('data.json'))
    

    print(datetime.now().timestamp())
    
    # s = [[timestamp_to_str(k), v] for k, v in data.items()]
    s = list(map(lambda x: [convert_timezone(x[0]), x[1]], data.items()))
    df = pd.DataFrame(s, columns=['dt', 'cnt'])
    df.dt = df.dt.astype('datetime64[s]')
    df = df.set_index('dt')
    chart = json.loads(serialize(df, render_to='my-chart', output_type='json', title='Player Count'))
    chart['series'][0]['name'] = 'Player Count'
    chart['xAxis']['title']['text'] = 'Time (CET)'
    return json.dumps(chart)


@app.route('/')
def index(chartID = 'data-chart', chart_type = 'line', chart_height = 350):
    return render_template('index.html', chart=create_chart())

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()