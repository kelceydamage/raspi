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
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
from common.print_helpers import padding
from common.print_helpers import Colours
from common.print_helpers import printc
import sys
import os
import zmq
import time
import json
import math

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION                 = b'0.1'
PAD                     = 0
COLOURS                 = Colours()

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
        self.meta.set_id('ROUTER-{0}'.format(self.pid).encode())
        self.meta.set_type(b'FWD')
        self.meta.set_pack(self.meta.hash)
        self.meta.set_role(b'chunker')
        self.meta.set_version(VERSION)       
        self.buffer = []

    def deserialize(self, frame, _type=''):
        if _type == 'dict':
            return eval(frame.decode(), {"__builtins__":None}, {})
        else:
            meta = MetaFrame(0)
            meta.gen_message(eval(frame.decode(), {"__builtins__":None}, {}))
            return meta

    def serialize(self, frame):
        return str(frame).encode()

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
        printc('{0}Listener online'.format(padding('[ROUTER-{0}(FRONTEND)] '.format(port), PAD)), COLOURS.GREEN)

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
        printc('{0}Listener online'.format(padding('[ROUTER-{0}(BACKEND)] '.format(port), PAD)), COLOURS.GREEN)

    def ship(self, header, envelope, n):
        self.meta.set_length(len(envelope))
        self.meta.set_part(n)
        meta = self.meta.serialize()
        message = header + [meta] + envelope
        self.backend.send_multipart(message)

    def chunk(self, message):
        """
NAME:           chunk
DESCRIPTION:    chunk messages to better load balance
REQUIRES:       message
        """
        meta = self.deserialize(message[2])
        count = math.ceil(float(len(message[3:])) / CHUNKING_SIZE)
        if count < 1:
            count = 1
        self.state[meta.get_serial()] = count
        self.meta.set_serial(meta.get_serial())
        self.meta.set_pack(meta.get_pack())
        header = message[0:2]
        envelope = []
        n = 1
        z = 0
        for i in range(len(message) - 3):
            z += 1
            envelope.append(message[i + 3])
            if z % CHUNKING_SIZE == 0:
                self.ship(header, envelope, n)
                envelope = []
                n += 1
        if len(envelope) > 0:
            self.ship(header, envelope, n)

    def assemble(self, message):
        try:
            meta = self.deserialize(message[2])
            self.state[meta.get_serial()] -= 1
            self.log('Forwarding', 'BACKEND', 'Assembling: {0}, Part: {1}'.format(
                meta.get_serial(),
                self.state[meta.get_serial()]
                ))
            header = message[:2]
            source = self.deserialize(message[3], 'dict')
            l = source['size']
            package = source['data']
            try:
                assert len(package) == l
            except AssertionError as e:
                self.log('Forwarding', 'BACKEND', 'Error: {0}'.format(
                    'Package contents ({0}) less then noted in manifest ({0})'.format(len(package), l)
                ))
            self.buffer = self.buffer + package
            if self.state[meta.get_serial()] == 0:
                meta.set_role(b'assembler')
                meta.set_size(len(self.buffer))
                data = DataFrame(0)
                data.set_data(self.buffer)
                data.set_size(len(self.buffer))
                data.set_pack(meta.get_pack())
                message = header + [self.serialize(meta.get_message())] + [data.serialize()]
                self.frontend.send_multipart(message)
                self.buffer = []
                del self.state[meta.get_serial()]
                #self.log('Forwarding', 'BACKEND', 'Shipped: {0}'.format(
                #    meta.get_serial()
                #))
        except Exception as e:
            print('R-0', str(e))

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
                #self.log('Forwarding', 'BACKEND', message[2])
                if CHUNKING == True:
                    self.assemble(message)
                else:
                    self.frontend.send_multipart(message)
        
    def start(self):
        """
NAME:
DESCRIPTION:
        """
        printc('{0}Routing started'.format(padding('[ROUTER-MASTER] ', PAD)), COLOURS.GREEN)
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