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
from common.datatypes import Envelope
from common.datatypes import Meta
from common.datatypes import Udf
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
        self.dealer = context.socket(zmq.DEALER)
        self.poller = zmq.Poller()
        self.pid = pid  
        self.envelope = Envelope()
        self.buffer = []
        self.state = {}

    def run_broker(self):
        #print('START BROKER')
        """
NAME:           run_broker
DESCRIPTION:    Main routing component [loop]
        """
        while True:
            socks = dict(self.poller.poll(100))
            if socks.get(self.frontend) == zmq.POLLOUT or socks.get(self.frontend) == zmq.POLLIN:
                try:
                    self.envelope.empty()
                    self.envelope.load(self.frontend.recv_multipart(flags=zmq.NOBLOCK))
                    self.envelope.validate()
                except Exception as e:
                    printc('[ROUTER] (run_broker): {0}'.format(str(e)), COLOURS.RED)
                printc('LIFESPAN: {0}'.format(self.envelope.lifespan), COLOURS.LIGHTBLUE)
                if self.envelope.lifespan != 0:
                    #meta = self.envelope.get_meta()
                    #print(meta.stage)
                    #if meta.stage == None:
                    if CHUNKING:
                        self.chunk()
                    #else:
                    #    self.backend.send_multipart(self.envelope.seal(), flags=zmq.NOBLOCK)
                    #    self.publisher.send_multipart([b'0', b'processing'], flags=zmq.NOBLOCK)
                else:
                    printc('[ROUTER] (run_broker): envelope lifespan depleted', COLOURS.RED)
                    self.assemble()

    def prepare(self, data, udf, meta):
        u = Udf()
        u.load(udf.extract_less())
        u.set_data(data)
        envelope = self.envelope
        print(u.pipeline)
        envelope.update_contents(meta, u)
        return envelope

    def assemble(self):
        print('assembling')
        try:
            udf = self.envelope.get_udf()
            meta = self.envelope.get_meta()
        except Exception as e:
            print(str(e))
        if meta.stage in self.state.keys():  
            print('HIT', self.state[meta.stage])
            self.state[meta.stage] -= udf.get_length()
            if self.state[meta.stage] > 0:
                print('sub-state')
                self.buffer.extend(udf.get_data())
                print(meta.stage, self.state[meta.stage])
            else:
                print(meta.stage, self.state[meta.stage])
                self.state.pop(meta.stage, None)
                envelope = self.prepare(self.buffer, udf, meta)
                print('returning')
                self.publisher.send_multipart(envelope.seal(), flags=zmq.NOBLOCK)
                print('shipped')
        else:
            print('stage', meta.stage)
            print(self.state)

    def chunk(self):
        print('chunking')
        buffer = []
        udf = self.envelope.get_udf()
        count = udf.get_length()
        meta = self.envelope.get_meta()
        if count > 0:
            print('send', meta.stage)
            if meta.stage not in self.state.keys():
                meta.stage = self.envelope.create_header().decode()
                self.state[meta.stage] = count
            n = 1
            z = 0
            for i in range(count):
                z += 1
                buffer.append(udf.data[i])
                if z % CHUNKING_SIZE == 0:
                    print('z mod c')
                    self.ship(meta, buffer, udf)
                    buffer = []
                    n += 1
            if len(buffer) > 0:
                print('s > 0')
                self.ship(meta, buffer, udf)
        else:
            print('s == 0')
            self.ship(meta, buffer, udf)
            self.envelope.empty()

    def ship(self, meta, buffer, udf):
        print('shipping')
        u = Udf()
        u.load(udf.extract_less())
        u.set_data(buffer)
        envelope = Envelope()
        envelope.load(self.envelope.seal())
        print(u.pipeline)
        envelope.update_contents(meta, u)
        try:
            self.backend.send_multipart(envelope.seal(), flags=zmq.NOBLOCK)
            #self.dealer.send_multipart(envelope.seal())
            #m = self.dealer.recv_multipart()
            #print(m)
        except Exception as e:
            print(str(e))
        #self.backend.send_multipart([b'test', b'msg'], flags=zmq.NOBLOCK)
        print(2)

    def chunker(self):
        udf = self.envelope.get_udf()
        payload_size = udf.get_length()
        meta = self.envelope.get_meta()
        if meta.stage in self.state.keys():
            print('found meta', meta.stage, self.state[meta.stage])
            #self.backend.send_multipart(self.envelope.seal(), flags=zmq.NOBLOCK)
            #PRECHUNK = True
        else:
            meta.stage = self.envelope.create_header().decode()
            self.state[meta.stage] = 0
        for n in self.state:
            print(n, self.state[n])
        if int(payload_size) <= 1 :
            self.backend.send_multipart(self.envelope.seal(), flags=zmq.NOBLOCK)
            self.publisher.send_multipart([b'0', b'processing'], flags=zmq.NOBLOCK)
        else:
            data = []
            if CHUNKING_SIZE == udf.get_length():
                print('sending-chunk *')
                self.state[meta.stage] += 1
                try:
                    envelope = self.prepare(data, udf, meta)
                except Exception as e:
                    print(str(e))
                try:
                    self.backend.send_multipart(envelope.seal(), flags=zmq.NOBLOCK)
                except Exception as e:
                    print(str(e))
            else:
                for i in range(payload_size):
                    data.append(udf.data[i])
                    if len(data) % CHUNKING_SIZE == 0:
                        print('sending-chunk')
                        self.state[meta.stage] += 1
                        try:
                            envelope = self.prepare(data, udf, meta)
                        except Exception as e:
                            print(str(e))
                        try:
                            self.backend.send_multipart(envelope.seal(), flags=zmq.NOBLOCK)
                        except Exception as e:
                            print(str(e))
                        #self.publisher.send_multipart([b'0', b'processing'], flags=zmq.NOBLOCK)
                        data = []
                if len(data) > 0:
                    self.state[meta.stage] += 1
                    envelope = self.prepare(data, udf, meta)
                    self.backend.send_multipart(envelope.seal(), flags=zmq.NOBLOCK)
                    self.publisher.send_multipart([b'0', b'processing'], flags=zmq.NOBLOCK)
            

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
            self.poller.register(self.frontend, zmq.POLLIN|zmq.POLLOUT)
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

    def setup_dealer(self, host, port, proto='tcp'):
        """
NAME:           setup_backend
DESCRIPTION:    Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        try:
            self.dealer.bind('{2}://{0}:{1}'.format(
                host, 
                port,
                proto
                ))
        except Exception as e:
            printc('[ROUTER] (setup_dealer): {0}'.format(str(e)), COLOURS.RED)
        printc('{0}dealer online'.format(padding('[ROUTER-{0}(DEALER)] '.format(port), PAD)), COLOURS.GREEN)

    def start(self):
        """
NAME:
DESCRIPTION:
        """
        printc('{0}Routing started'.format(padding('[ROUTER-MASTER] ', PAD)), COLOURS.GREEN)
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