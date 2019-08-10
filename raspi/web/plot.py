#!/usr/bin/env python3
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->
# Required Args:        
#
# Optional Args:        
#
# Imports
# ------------------------------------------------------------------------ 79->
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Range1d
from bokeh.models import LinearColorMapper, BasicTicker, ColorBar
from bokeh.plotting import figure, reset_output
from bokeh.themes import Theme
from multiprocessing import Queue
from bokeh.palettes import Viridis
from bokeh.palettes import Category10
import numpy as np
import time

# Globals
# ------------------------------------------------------------------------ 79->
LOGFILE = 'log/plot.log'
PLOT_QUEUE = Queue()

PLOTS = {}
SOURCES = {}
STATE = {}
COLORMAP = {
    0: 'red', 
    1: 'green', 
    2: 'blue',
    3: 'orange',
    4: 'purple',
    5: 'navy'
}

DEFAULT = ColumnDataSource(data={'x': [0], 'y': [0], 'color': ['#ffffff']})

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def setState(sources):
    if sources['name'] not in STATE.keys():
        STATE[sources['name']] = {}
        for i in range(len(sources['draws'])):
            STATE[sources['name']][i] = ColumnDataSource()

def getState(sources, i):
    if sources['name'] in STATE.keys():
        log('GETSTATE: {0} - {1}'.format(
                sources['name'],
                STATE[sources['name']]
            )
        )
        return STATE[sources['name']][i]

def isState(sources):
    if sources['name'] in STATE.keys():
        return True
    return False

def log(msg):
    with open(LOGFILE, 'a') as f:
        f.write(str(msg) + '\n')

def convertcolor(x):
    if x < 256:
        a = x / 256
    else:
        a = 256 / x
    b = a * 180 + 70
    return int(b)

def getColors(draw):
    if draw['series'] is None:
        return ['#000000' for x in range(len(draw['x']))]
    return [Viridis[256][convertcolor(x)] for x in draw['series']]

def draw(sources):
    c = 0
    plot = PLOTS[sources['name']]
    color_mapper = LinearColorMapper(
        palette=Category10[6], 
        low=0,
        high=6
    )
    plot = PLOTS[sources['name']]
    color_bar = ColorBar(
        color_mapper=color_mapper, 
        height=60, 
        ticker=BasicTicker(),
        label_standoff=5, 
        border_line_color=None, 
        location=(-10,147)
    )
    plot.add_layout(color_bar)
    for draw in sources['draws']:
        draw = sort_bad(draw)
        try:
            plot.xaxis.axis_label = sources['xAxis']
            plot.yaxis.axis_label = sources['yAxis']
            color = getColors(draw)
            cds = getState(sources, c)
            cds.data = {'x': draw['x'], 'y': draw['y'], 'color': color}
            if draw['type'] == 'circle':
                getattr(plot, draw['type'])(x='x', y='y', source=cds, size=2, color='color')
            elif draw['type'] == 'line':
                getattr(plot, draw['type'])(x='x', y='y', source=cds, line_width=2, line_color=Category10[6][c])
            elif draw['type'] == 'vbar':
                getattr(plot, draw['type'])(x='x', top='y', source=cds, bottom=0, width=1, fill_color='color')
        except Exception as e:
            log('draw: {0}'.format(e))
        c += 1

def sort_bad(q_data):
    dtype = [('x', '<i8'), ('y', '<f8')]
    shape = (len(q_data['x']))
    a = np.zeros(
        shape,
        dtype=dtype
        )
    a['x'] = q_data['x']
    a['y'] = q_data['y']
    a.sort(
        axis=0,
        kind='quicksort',
        order='x'
        )
    q_data['x'] = a['x'].tolist()
    q_data['y'] = a['y'].tolist()
    return q_data

def addFigure(sources, doc):
    PLOTS[sources['name']] = figure(
        title=sources['name'],
        plot_width=1200,
        plot_height=300,
        x_axis_type=sources['scale'],
        y_axis_type=sources['scale'],
        x_minor_ticks=10,
        y_minor_ticks=10,
        #x_range=Range1d(0, 1000000),
        #y_range=Range1d(0, 10000)
    )
    doc.add_root(column(PLOTS[sources['name']]))

def modify_doc(doc):

    def update():
        try:
            if not PLOT_QUEUE.empty():
                q_data = PLOT_QUEUE.get()
                if isinstance(q_data, dict):
                    if not isState(q_data):
                        setState(q_data)
                        addFigure(q_data, doc)
                    draw(q_data)
        except Exception as e:
            log('callback: {0}'.format(e))
        reset_output()

    try:
        doc.add_periodic_callback(update, 20)
    except Exception as e:
        log('tools: {0}'.format(e))