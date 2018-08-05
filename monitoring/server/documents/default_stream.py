
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
from monitoring.drivers.haruspex import HaruspexDriver
from monitoring.drivers.haruspex import GET
from common.custom_math import CustomMath
from bokeh.models import Range1d, LabelSet, Label
from scipy.stats import chisquare, chi2

#from monitoring.server.documents.jackpot import jp
from common.math.statistics import normalize_2d_by_pct

from functools import partial
import random
from threading import Thread
import sys
import numpy
import math

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure


from tornado import gen
import json
import time

import numpy as np

# queryContext Python to C object
'''
q.metric = _obj[b'metric']
q._type = _obj[b'_type']
q.start = _obj[b'start']
q.end = _obj[b'end']
q.stepping = _obj[b'stepping']
q.function = _obj[b'function']
q.window = _obj[b'window']
q.simple = _obj[b'simple']
q.filter = _obj[b'filter']
'''

WINDOW = 30000
BUFF_DEPTH = 40
Q_DEPTH = BUFF_DEPTH * WINDOW + 1

driver = HaruspexDriver()

driver.configure(
    host=b'apps1.sre',
    port=19099,
    endpoint=b'/prometheus/api/v1/',
    cert=b'var/security/cert.cer',
    key=b'var/security/key.pem'
)

driver.connect()

# This is important! Save curdoc() to make sure all threads
# see then same document.
doc = curdoc()
current_milli_time = lambda: int(round(time.time() * 1000))

def running_mean(y, w, n):
    m = []
    for i in range(0, n):
        l = len(y[:i])
        if l < w:
            w1 = l + 1
        else:
            w1 = w
        m.append(CustomMath().simple_moving_average(y[:i], w1))
    return m

@gen.coroutine
def update(x, y, n, s):
    if len(s.data['x']) < 10:
        s.stream(dict(x=x[-n:], y=y[-n:]), rollover=n)
    elif not s.data['y'][-1] == y[-1]:
        s.stream(dict(x=x[-1:], y=y[-1:]), rollover=n)
    #else:
    #    s.stream(dict(x=x[-1:], y=y[-1:]), rollover=n)

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

def polyfit(x, y, degree):
    l = len(x)
    xpmin = min(x)
    xpmax = max(x)
    xp = np.linspace(xpmin, xpmax, l)
    pf = np.polyfit(xp, y, degree)
    return np.poly1d(pf), xp

def regression(x, y, degree, r_source, p_source, l_source, c_source):
    p1, xp = polyfit(x, y, degree)
    c1, xp = polyfit(x, y, 2)
    l1, xp = polyfit(x, y, 1)
    doc.add_next_tick_callback(partial(update, x=x, y=y, n=BUFF_DEPTH, s=r_source))
    doc.add_next_tick_callback(partial(update, x=xp, y=p1(xp), n=BUFF_DEPTH, s=p_source))
    doc.add_next_tick_callback(partial(update, x=xp, y=l1(xp), n=BUFF_DEPTH, s=l_source))
    doc.add_next_tick_callback(partial(update, x=xp, y=c1(xp), n=BUFF_DEPTH, s=c_source))

def probabiities(o, e, pdf_source, ppf_source, isf_source, chi_source):
    df = len(o) - 1
    cc = chisquare(o, f_exp=e)
    sf = chi2.sf(cc.statistic, df)
    pdf = chi2.pdf(cc.statistic, df)
    ppf = round(chi2.ppf(0.05, df), 4)
    isf = round(chi2.isf(0.05, df), 4) #inverse of cdf, or lookup value for chi^2 and p=0.05 based on df [significance level]
    x_prob = np.linspace(0, df*2, df+1)
    doc.add_next_tick_callback(partial(update, x=x_prob, y=chi2.pdf(x_prob, df), n=BUFF_DEPTH, s=pdf_source))
    doc.add_next_tick_callback(partial(update, x=[ppf, ppf], y=[0, 0.05], n=BUFF_DEPTH, s=ppf_source))
    doc.add_next_tick_callback(partial(update, x=[isf, isf], y=[0, 0.05], n=BUFF_DEPTH, s=isf_source))
    doc.add_next_tick_callback(partial(update, x=[round(cc.statistic, 4), round(cc.statistic, 4)], y=[0, 0.05], n=BUFF_DEPTH, s=chi_source))
    print('Distance: ', isf - cc.statistic)
    print('Target: {0} -> {1}'.format(isf, cc.statistic))

def blocking_task(x_label, y_label):
    y = 4
    cap = 80
    while True:
        s = time.time()
        

        # do some blocking computation
        query['metric'] = x_label
        #query['function'] = 'rate'
        #query['window'] = '2s'
        query['filter'] = {
            'instance': 'apps1.sre:19100',
            #'device':'sda'
            #'mountpoint': "/opt"
            }
        r1 = get_stream(int(time.time()), Q_DEPTH, query)
        x1, y1 = unpack(r1)
        #print(driver.uri)

        query['metric'] = y_label
        #query['function'] = 'rate'
        #query['window'] = '2s'
        query['filter'] = {
            'instance': 'apps1.sre:19100',
            #'device':'sda',
            #'mountpoint': "/opt"
            }
        r2 = get_stream(int(time.time()), Q_DEPTH, query)
        x2, y2 = unpack(r2)
        #print(driver.uri)

        y1n, y2n = normalize_2d_by_pct(y1, y2)

        regression(x1, y1n, 13, r_source1a, p_source1a, l_source1a, c_source1a)
        regression(x2, y2n, 13, r_source1b, p_source1b, l_source1b, c_source1b)
        regression(y2n, y1n, 13, r_source2a, p_source2a, l_source2a, c_source2a)

        probabiities(y2n, y1n, pdf_source, ppf_source, isf_source, chi_source)
        # but update the document from callback

        end = time.time() - s
        print('loop-time: ', end)
        if end <= 1:
            time.sleep(1 - end)
        else:
            print('Error loop state too-long: {0}'.format(end))
        break
        

query = {
    'metric': 'system:load_5',
    "_type": "query_range",
    "start": "1538847228",
    "end": "1531867428",
    "filter": {},
    "stepping": "{0}s".format(WINDOW),
    "function": "",
    "window": "",
    "simple": False
}

driver.update_query(query)

# this must only be modified from a Bokeh session callback
r_source1a = ColumnDataSource(data=dict(x=[0], y=[0]))
r_source1b = ColumnDataSource(data=dict(x=[0], y=[0]))
p_source1a = ColumnDataSource(data=dict(x=[0], y=[0]))
p_source1b = ColumnDataSource(data=dict(x=[0], y=[0]))
l_source1a = ColumnDataSource(data=dict(x=[0], y=[0]))
l_source1b = ColumnDataSource(data=dict(x=[0], y=[0]))
c_source1a = ColumnDataSource(data=dict(x=[0], y=[0]))
c_source1b = ColumnDataSource(data=dict(x=[0], y=[0]))

r_source2a = ColumnDataSource(data=dict(x=[0], y=[0]))
p_source2a = ColumnDataSource(data=dict(x=[0], y=[0]))
l_source2a = ColumnDataSource(data=dict(x=[0], y=[0]))
c_source2a = ColumnDataSource(data=dict(x=[0], y=[0]))

pdf_source = ColumnDataSource(data=dict(x=[0], y=[0]))
ppf_source = ColumnDataSource(data=dict(x=[0], y=[0]))
isf_source = ColumnDataSource(data=dict(x=[0], y=[0]))
chi_source = ColumnDataSource(data=dict(x=[0], y=[0]))
# y_range=
#p = figure(width=800, height=600, x_axis_type="datetime")

Y_LABEL = 'node_load1'
X_LABEL = 'node_load15'


p = figure(width=1000, height=400, y_range=Range1d(0, 100), x_axis_type="datetime", y_axis_label="value", x_axis_label="datetime", title="Normalized Streams With Regression")
p.line(x='x', y='y', source=r_source1a, line_width=1, line_color='dodgerblue')
p.line(x='x', y='y', source=r_source1b, line_width=1, line_color='green')
#p.vbar(source=r_source1a,x='x',top='y',bottom=0,width=10,color='dodgerblue')
#p.vbar(source=r_source1b,x='x',top='y',bottom=0,width=10,color='green')
p.line(x='x', y='y', source=l_source1a, legend='Linear Regression', line_width=3, line_color='orange')
p.line(x='x', y='y', source=l_source1b, legend='Linear Regression', line_width=3, line_color='orange')
p.line(x='x', y='y', source=p_source1a, legend='Poly Fit x^13', line_width=2, line_color='red', line_dash='dashed')
p.line(x='x', y='y', source=p_source1b, legend='Poly Fit x^13', line_width=2, line_color='red', line_dash='dashed')
p.line(x='x', y='y', source=c_source1a, legend='Curve Fit', line_width=2, line_color='grey', line_dash='dotted')
p.line(x='x', y='y', source=c_source1b, legend='Curve Fit', line_width=2, line_color='grey', line_dash='dotted')

p_2 = figure(width=1000, height=400, y_range=Range1d(0, 100), x_axis_type="linear", y_axis_label=Y_LABEL, x_axis_label=X_LABEL, title="Correlation Of 2 Variables")
p_2.circle(x='x', y='y', source=r_source2a, fill_color='dodgerblue', line_color='dodgerblue', size=8)
p_2.line(x='x', y='y', source=l_source2a, legend='Linear Regression', line_width=2, line_color='orange')
p_2.line(x='x', y='y', source=p_source2a, legend='Poly Fit x^13', line_width=2, line_color='red', line_dash='dashed')
p_2.line(x='x', y='y', source=c_source2a, legend='Curve Fit', line_width=2, line_color='grey', line_dash='dotted')

p_3 = figure(width=1000, height=400, x_axis_type="log", y_axis_label='frequency', x_axis_label='value', title="Probability")
p_3.circle(x='x', y='y', source=pdf_source, fill_color='firebrick', line_color='firebrick', size=3, legend='Probability Density Function')
p_3.line(x='x', y='y', source=pdf_source, line_color='firebrick', legend='ppf')
l_1 = LabelSet(x='x', y='y', text='x', level='glyph',
        x_offset=10, y_offset=100, source=ppf_source, render_mode='canvas')
p_3.line(x='x', y='y', source=ppf_source, line_color='blue', legend='ppf')
l_2 = LabelSet(x='x', y='y', text='x', level='glyph',
        x_offset=10, y_offset=100, source=isf_source, render_mode='canvas')
p_3.line(x='x', y='y', source=isf_source, line_color='forestgreen', legend='Inverse Survival Function')
l_3 = LabelSet(x='x', y='y', text='x', level='glyph',
        x_offset=-100, y_offset=80, source=chi_source, render_mode='canvas')
p_3.line(x='x', y='y', source=chi_source, line_color='black', line_width=10, legend='chi^2')
p_3.add_layout(l_1)
p_3.add_layout(l_2)
p_3.add_layout(l_3)
doc.add_root(p)
doc.add_root(p_2)
doc.add_root(p_3)

thread = Thread(target=blocking_task, args=(X_LABEL, Y_LABEL))
thread.start()