#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Doc
#-------------------------------------------------------------------------------- <-80
"""
SUMMARY:        Broker-less distributed task workers.
"""

# Imports
#-------------------------------------------------------------------------------- <-80
'''
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource

def make_document(doc):
    fig = figure(title='Line plot!', sizing_mode='scale_width')
    fig.line(x=[1, 2, 3], y=[1, 4, 9])

    doc.title = "Hello, world!"
    doc.add_root(fig)

apps = {'/': Application(FunctionHandler(make_document))}

server = Server(apps, port=5006, num_procs=2)
print('Starting Server')
server.start()




'''
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from server.main import *

def make_document(doc):
    source = ColumnDataSource({'time': [time(), time() + 1],
                               'idle': [0, 0.1],
                               'saturated': [0, 0.1]})

    x_range = DataRange1d(follow='end', follow_interval=20000, range_padding=0)

    fig = figure(title="Idle and Saturated Workers Over Time",
                 x_axis_type='datetime', y_range=[-0.1, len(scheduler.workers) + 0.1],
                 height=150, tools='', x_range=x_range, **kwargs)
    fig.line(source=source, x='time', y='idle', color='red')
    fig.line(source=source, x='time', y='saturated', color='green')
    fig.yaxis.minor_tick_line_color = None

    fig.add_tools(
        ResetTool(reset_size=False),
        PanTool(dimensions="width"),
        WheelZoomTool(dimensions="width")
    )

    doc.add_root(fig)

    def update():
        result = {'time': [time() * 1000],
                  'idle': [len(scheduler.idle)],
                  'saturated': [len(scheduler.saturated)]}
        source.stream(result, 10000)

    doc.add_periodic_callback(update, 100)

applications = {'/': Application(FunctionHandler(make_document))}

server = Server(
    applications,  # list of Bokeh applications
    #io_loop=None,        # Tornado IOLoop
    #host='0.0.0.0',
    port=5006,      # port, num_procs, etc.
    num_procs=2
)

# start timers and services and immediately return
print("Runing on port: 5006")
server.start()
