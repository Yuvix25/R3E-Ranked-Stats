import io
import json
import pytz
from datetime import datetime
from flask import Response, Flask
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Thread

app = Flask(__name__)


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    data = json.load(open('data.json'))
    cet = pytz.timezone('CET')
    x = [str(datetime.fromtimestamp(int(k), tz=cet)) for k in data.keys()]
    y = list(data.values())

    axis.plot(x, y, '-o')
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


@app.route('/')
def index():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()