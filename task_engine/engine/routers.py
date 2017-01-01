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
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
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
    def __init__(self, pid):
        super(Router, self).__init__()
        context = zmq.Context()
        self.frontend = context.socket(zmq.ROUTER)
        self.backend = context.socket(zmq.DEALER)
        self.poller = zmq.Poller()
        self.pid = pid

    def register_peers(self, peers):
        """
NAME:           register_peers
DESCRIPTION:    Set a property with all local upstream workers
        """
        self.peers = peers

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
NAME:           run_broker
DESCRIPTION:    Main routing component [loop]
        """
        while True:
            print('loop')
            socks = dict(self.poller.poll())
            if socks.get(self.frontend) == zmq.POLLIN:
                message = self.frontend.recv_multipart()
                print('[ROUTER-9000(FRONTEND)] Forwarding: {}'.format(message))
                self.backend.send_multipart(message)

            if socks.get(self.backend) == zmq.POLLIN:
                message = self.backend.recv_multipart()
                print('[ROUTER-9001(BACKEND)] Forwarding: {}'.format(message))
                self.frontend.send_multipart(message)

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