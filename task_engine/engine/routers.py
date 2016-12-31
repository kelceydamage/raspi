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

"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import sys
import os
import zmq
import time
import json

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class Router(object):
    """
NAME:           Router
DESCRIPTION:    Routes messages to available workers.
    """
    def __init__(self):
        super(Router, self).__init__()
        context = zmq.Context()
        self.frontend = context.socket(zmq.ROUTER)
        self.backend = context.socket(zmq.DEALER)
        self.poller = zmq.Poller()

    def setup_frontend(self, host, port, proto='tcp'):
        """
NAME:           setup_frontend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        self.frontend.bind('{2}://{0}:{1}'.format(
            host, 
            port,
            proto
            ))
        self.poller.register(self.frontend, zmq.POLLIN)
        print('[ROUTER-{0}(FRONTEND)] Listener online'.format(port))

    def setup_backend(self, host, port, proto='tcp'):
        """
NAME:           setup_backend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        self.backend.bind('{2}://{0}:{1}'.format(
            host, 
            port,
            proto
            ))
        self.poller.register(self.backend, zmq.POLLIN)
        print('[ROUTER-{0}(BACKEND)] Listener online'.format(port))

    def run_broker(self):
        """
NAME:
DESCRIPTION:
        """
        while True:
            print('loop')
            socks = {}
            for sock in self.poller.poll():
                socks[sock[0]] = sock[1]
            
            if socks.get(self.frontend) == zmq.POLLIN:
                m = [x for x in self.frontend.recv_multipart()]
                print('received from frontend: {}'.format(m))
                meta = json.dumps({'responder': 222})
                self.frontend.send_multipart(m)
                
            """    
            if sock.get(backend) == zmq.POLLIN:
                for message in backend.recv_multipart():
                    yield message
                print('received from backend: {}'.format(message))
                for part in frontend.send_multipart(message):
                    yield part
            time.sleep(1)
            """

    def start(self):
        """
NAME:
DESCRIPTION:
        """
        print('[ROUTER-MASTER] Routing started')
        self.run_broker()

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    R = Router()
    R.setup_frontend('127.0.0.1', 9000)
    R.setup_backend('127.0.0.1', 9001)
    R.start()