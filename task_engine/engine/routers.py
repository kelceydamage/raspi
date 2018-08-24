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
            #os.path.dirname(
                os.path.abspath(__file__)
                )
            #)
        )
    )
from conf.configuration import ENABLE_STDOUT
from conf.configuration import CHUNKING
from conf.configuration import CHUNKING_SIZE
from common.datatypes import *
from common.print_helpers import padding
from common.print_helpers import Colours
from common.print_helpers import printc
import sys
import os
import zmq
import time
import math

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION                 = b'0.1'
PAD                     = 0
COLOURS                 = Colours()
CHUNKING = True
CHUNKING_SIZE = 2

# Classes
#-------------------------------------------------------------------------------- <-80
class Router(object):
    """
NAME:           Router
DESCRIPTION:    Routes messages to available workers.
    """
    def __init__(self, pid):
        #print('INIT')
        super(Router, self).__init__()
        context = zmq.Context()
        self.frontend = context.socket(zmq.PULL) # ROUTER
        self.backend = context.socket(zmq.PUSH) # DEALER
        self.publisher = context.socket(zmq.PUB)
        self.pid = pid  
        self.state = {}
        self.buffer = []
        self.queue = []

    def ship(self, header, meta, udf):
        envelope = Envelope()
        envelope.pack(header, meta.extract(), udf.extract(), self.buffer)
        print('r -->', envelope.length, envelope.size, envelope.lifespan)
        self.backend.send_multipart(envelope.seal())
        self.buffer = []

    def receive(self):
        envelope = Envelope()
        envelope.load(self.frontend.recv_multipart())
        return envelope

    def create_state(self, meta):
        if not isinstance(meta.stage, bytes):
            stage = meta.stage.encode()
        else:
            stage = meta.stage
        if stage not in self.state.keys():
            meta.stage = Tools.create_id()
            self.state[meta.stage] = 1
            if meta.length % CHUNKING_SIZE != 0:
                self.state[meta.stage] += 1
        else:
            self.state[stage] += 1
        return meta

    def retrieve_state(self, meta):
        stage = meta.stage.encode()
        if stage in self.state.keys():
            self.state[stage] -= 1
            if self.state[stage] == 0:
                self.state.pop(stage, None)
                return meta, True, 0
            return meta, True, self.state[stage]
        return meta, False, 0

    def assemble(self, envelope):
        header, meta, udf, data = envelope.unpack()
        meta, success, count = self.retrieve_state(meta)
        print('STATE', self.state)
        if success:
            self.queue.extend(data)
            if count == 0:
                envelope.pack(header, meta.extract(), udf.extract(), self.queue)
                self.publisher.send_multipart(envelope.seal())
                self.queue = []
                print('send to client multiple')
        else:
            self.publisher.send_multipart(envelope.seal())
            print('send to client single')

    def chunk(self, envelope):
        header, meta, udf, data = envelope.unpack()
        for i in range(len(data)):
            self.buffer.append(data.pop())
            if len(self.buffer) % CHUNKING_SIZE == 0:
                #print('start m')
                meta = self.create_state(meta)
                self.ship(header, meta, udf)
        if len(self.buffer) > 0:
            #print('ship s')
            self.ship(header, meta, udf)
        del envelope
        print('STATE', self.state)

    def start(self):
        while True:
            envelope = self.receive()
            #print('router <---')
            #print('lifespan', envelope.lifespan)
            #print('rr', envelope.length, envelope.size, envelope.lifespan)
            if envelope.lifespan > 0:
                if envelope.length <= 1 or envelope.length == CHUNKING_SIZE:
                    self.backend.send_multipart(envelope.seal())
                else:
                    self.chunk(envelope)
            else:
                #print('END')
                try:
                    self.assemble(envelope)
                except Exception as e:
                    print('ERROR', e)

    def setup_frontend(self, host, port, proto='tcp'):
        """
NAME:           setup_frontend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        try:
            self.frontend.bind('{2}://{0}:{1}'.format(
                host, 
                port,
                proto
                ))
            #self.poller.register(self.frontend, zmq.POLLIN|zmq.POLLOUT)
        except Exception as e:
            printc('[ROUTER] (setup_frontend): {0}'.format(str(e)), COLOURS.RED)
        printc('{0}Listener online'.format(padding('[ROUTER-{0}(FRONTEND)] '.format(port), PAD)), COLOURS.GREEN)

    def setup_backend(self, host, port, proto='tcp'):
        """
NAME:           setup_backend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        try:
            self.backend.bind('{2}://{0}:{1}'.format(
                host, 
                port,
                proto
                ))
            self.backend.hwm = 1000
        except Exception as e:
            printc('[ROUTER] (setup_backend): {0}'.format(str(e)), COLOURS.RED)
        printc('{0}Listener online'.format(padding('[ROUTER-{0}(BACKEND)] '.format(port), PAD)), COLOURS.GREEN)

    def setup_publisher(self, host, port, proto='tcp'):
        """
NAME:           setup_backend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        try:
            self.publisher.bind('{2}://{0}:{1}'.format(
                host, 
                port,
                proto
                ))
        except Exception as e:
            printc('[ROUTER] (setup_publisher): {0}'.format(str(e)), COLOURS.RED)
        printc('{0}publisher online'.format(padding('[ROUTER-{0}(PUBLISHER)] '.format(port), PAD)), COLOURS.GREEN)

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80