import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
                )
            )
        )
    )

from common.custom_math import CustomMath

from functools import partial
import random
from threading import Thread
import time
import sys
import numpy
import math

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure


from tornado import gen

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))
source2 = ColumnDataSource(data=dict(x=[0], y=[0]))
source3 = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see then same document.
doc = curdoc()
current_milli_time = lambda: int(round(time.time() * 1000))

def running_mean(x, w):
    return CustomMath().simple_moving_average(x, w)

@gen.coroutine
def update(x, y, z, l):
    source.stream(dict(x=[x], y=[y]), rollover=100)
    source2.stream(dict(x=[x], y=[z]), rollover=100)
    source3.stream(dict(x=[x], y=[l]), rollover=100)

def data_gen(y):
    if y > 7:
        y = random.randrange(3, 9, 1)
    elif y < 3:
        y = random.randrange(1, 7, 1)
    else:
        y = random.randrange(1, 9, 1)
    x = current_milli_time()

    return x, y

def blocking_task():
    y = 4
    cap = 80
    while True:
        s = time.time()
        # do some blocking computation
        x, y = data_gen(y)
        if len(source.data['y']) <= cap:
            window = len(source.data['y'])
        z = running_mean(source.data['y'] + [y], window)
        l = running_mean(source.data['y'] + [y], int(math.ceil(float(window) / 5)))
        # but update the document from callback
        doc.add_next_tick_callback(partial(update, x=x, y=y, z=z, l=l))
        end = time.time() - s
        if end <= 0.01:
            time.sleep(0.01 - end)
        else:
            print('Error loop state too-long: {0}'.format(end))


p = figure(y_range=[2, 6.2], width=640, height=480, x_axis_type="datetime")
#l = p.line(x='x', y='y', source=source, legend='Temp', line_width=4)
l = p.line(x='x', y='y', source=source2, legend='Temp3', line_width=4, line_color='firebrick')
l = p.line(x='x', y='y', source=source3, legend='Temp3', line_width=4, line_color='green')
l2 = p.circle(
    x='x',
    y='y',
    source=source2,
    legend='Temp2', 
    fill_color='red',
    size=10
    )

doc.add_root(p)

thread = Thread(target=blocking_task)
thread.start()