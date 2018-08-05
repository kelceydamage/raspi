from __future__ import division
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                    )
                )
            )
        )
    )
import numpy as np
from monitoring.drivers.haruspex import HaruspexDriver
from monitoring.drivers.haruspex import GET
from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM
#from bokeh.io import show
from threading import Thread
import time

from bokeh.plotting import curdoc, figure

from monitoring.drivers.surface3d import Surface3d

driver = HaruspexDriver()

def unpack(response):
    x = []
    y = []
    for r in response['results']:
        for v in r['values']:
            x.append(float(v[0])*1000)
            y.append(float(v[1]))
    return x, y

def get_stream(start, depth, query):
    query['start'] = str(start - depth)
    query['end'] = str(start)
    driver.update_query(query)
    return driver.request(GET)

driver.configure(
    host=b'apps1.sre',
    port=19099,
    endpoint=b'/prometheus/api/v1/',
    cert=b'var/security/cert.cer',
    key=b'var/security/key.pem'
)

driver.connect()

query = {
    'metric': 'system:load_5',
    "_type": "query_range",
    "start": "1538847228",
    "end": "1531867428",
    "filter": {},
    "stepping": "1s",
    "function": "",
    "window": "",
    "simple": False
}

driver.update_query(query)

Y_LABEL = 'node_memory_Active_bytes'
X_LABEL = 'node_memory_Cached_bytes'
Z_LABEL = 'node_memory_Dirty_bytes'

Q_DEPTH = 200
BUFF_DEPTH = 100

# do some blocking computation
query['metric'] = X_LABEL
query['function'] = 'rate'
query['window'] = '2s'
query['filter'] = {
    'instance': 'apps2.internal:19100',
    #'device':'sda'
    }
r1 = get_stream(int(time.time()), Q_DEPTH, query)
x1, y1 = unpack(r1)

query['metric'] = Y_LABEL
query['function'] = 'rate'
query['window'] = '2s'
query['filter'] = {
    'instance': 'apps2.internal:19100',
    #'device':'sda'
    }
r2 = get_stream(int(time.time()), Q_DEPTH, query)
x2, y2 = unpack(r2)

query['metric'] = Z_LABEL
query['function'] = 'rate'
query['window'] = '2s'
query['filter'] = {
    'instance': 'apps2.internal:19100',
    #'device':'sda'
    }
r3 = get_stream(int(time.time()), Q_DEPTH, query)
x3, y3 = unpack(r3)

doc = curdoc()

xx, yy = np.meshgrid(y1, y2)
print(xx)
xx = xx.ravel()
print(xx)
yy = yy.ravel()
#zz = y3 * len(y3)

value = np.sin(xx/50) * np.cos(yy/50) * 50 + 50
zz = value

source = ColumnDataSource(data=dict(x=xx, y=yy, z=zz))

surface = Surface3d(x='x', y="y", z="z", data_source=source, width=600, height=600)

doc.add_root(surface)