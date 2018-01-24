#!/usr/bin/env python
from bokeh.server.server import Server

server = Server(
    'server',  # list of Bokeh applications
    io_loop=None,        # Tornado IOLoop
    port=5006,      # port, num_procs, etc.
    num_procs=2
)

# start timers and services and immediately return
server.start()