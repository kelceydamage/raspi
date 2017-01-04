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
from conf.configuration import ENABLE_STDOUT
from conf.configuration import CHUNKING
from conf.configuration import CHUNKING_SIZE
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
import sys
import os
import zmq
import time
import json
import math

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION = 0.1

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
        self.state = {'init': self.pid}
        self.meta = MetaFrame(0)
        self.data = DataFrame(0)
        self.meta.digest()
        self.meta.message['id'] = 'ROUTER-{0}'.format(self.pid)
        self.meta.message['type'] = 'FWD'
        self.meta.message['pack'] = self.meta.hash
        self.meta.message['role'] = 'chunker'
        self.meta.message['version'] = VERSION
        self.buffer = []

    def deserialize(self, frame):
        return json.loads(frame)

    def serialize(self, frame):
        return json.dumps(frame)

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

    def chunk(self, message):
        """
NAME:           chunk
DESCRIPTION:    chunk messages to better load balance
REQUIRES:       message
        """

        def ship(header, envelope, n):
            self.meta.message['length'] = len(envelope)
            self.meta.message['part'] = n
            meta = self.meta.serialize()
            message = header + [meta] + envelope
            self.backend.send_multipart(message)

        meta = self.deserialize(message[2])
        count = math.ceil(float(len(message[3:])) / CHUNKING_SIZE)
        if count < 1:
            count = 1
        self.state[meta['serial']] = count + 1
        self.meta.message['serial'] = meta['serial']
        self.meta.message['pack'] = meta['pack']
        header = message[0:2]
        envelope = []
        n = 1
        for i in range(len(message) - 3):
            envelope.append(message[i + 3])
            if i % CHUNKING_SIZE == 0:
                ship(header, envelope, n)
                envelope = []
                n += 1
        if len(envelope) > 0:
            ship(header, envelope, n)

    def assemble(self, message):
        meta = self.deserialize(message[2])
        self.state[meta['serial']] -= 1
        self.log('Forwarding', 'BACKEND', 'Assembling: {0}, Part: {1}'.format(
            meta['serial'],
            self.state[meta['serial']]
            ))
        header = message[:2]
        package = message[3:]
        self.buffer = self.buffer + package
        if self.state[meta['serial']] == 0:
            meta['role'] = 'assembler'
            meta['size'] = len(self.buffer)
            message = header + [self.serialize(meta)] + self.buffer
            self.frontend.send_multipart(message)
            self.buffer = []
            del self.state[meta['serial']]
            self.log('Forwarding', 'BACKEND', 'Shipped: {0}'.format(
                meta['serial']
            ))

    def run_broker(self):
        """
NAME:           run_broker
DESCRIPTION:    Main routing component [loop]
        """
        while True:
            socks = dict(self.poller.poll())
            if socks.get(self.frontend) == zmq.POLLIN:
                message = self.frontend.recv_multipart()
                if CHUNKING == True:
                    self.log(
                        'Chunking: {0}/{1}'.format(len(message[3:]), CHUNKING_SIZE), 
                        'FRONTEND', 
                        message[2]
                        )
                    self.chunk(message)
                else:
                    self.log('Forwarding', 'FRONTEND', message[2])
                    self.backend.send_multipart(message)

            if socks.get(self.backend) == zmq.POLLIN:
                message = self.backend.recv_multipart()
                self.log('Forwarding', 'BACKEND', message[2])
                if CHUNKING == True:
                    self.assemble(message)
                else:
                    self.frontend.send_multipart(message)
        
    def start(self):
        """
NAME:
DESCRIPTION:
        """
        print('[ROUTER-MASTER] Routing started')
        self.run_broker()

    def log(self, action, service, message):
        if ENABLE_STDOUT == True:
            print('[ROUTER-{0}({1})] {3}: {2}'.format(
                self.pid, 
                service, 
                message,
                action
                )) 

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    R = Router()
    R.setup_frontend('127.0.0.1', 9000)
    R.setup_backend('127.0.0.1', 9001)
    R.start()