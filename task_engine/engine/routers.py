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
CHUNKING = False

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
        self.poller = zmq.Poller()
        self.pid = pid  
        self.envelope = Envelope()
        self.buffer = []

    def run_broker(self):
        #print('START BROKER')
        """
NAME:           run_broker
DESCRIPTION:    Main routing component [loop]
        """
        while True:
            try:
                self.publisher.send_multipart([b'0', b'keepalive'], flags=zmq.NOBLOCK)
            except Exception as e:
                print(str(e))
            socks = dict(self.poller.poll())
            if socks.get(self.frontend) == zmq.POLLIN:
                try:
                    self.envelope.empty()
                    self.envelope.load(self.frontend.recv_multipart())
                except Exception as e:
                    printc('[ROUTER] (run_broker): {0}'.format(str(e)), COLOURS.RED)
                try:
                    self.envelope.validate()
                except Exception as e:
                    printc('[ROUTER] (run_broker): {0}'.format(str(e)), COLOURS.RED)
                else:
                    printc('LIFESPAN: {0}'.format(self.envelope.lifespan), COLOURS.LIGHTBLUE)
                    if self.envelope.lifespan != 0:
                        self.backend.send_multipart(self.envelope.seal())
                        self.publisher.send_multipart([b'0', b'processing'], flags=zmq.NOBLOCK)
                    else:
                        printc('[ROUTER] (run_broker): envelope lifespan depleted', COLOURS.RED)
                        self.publisher.send_multipart(self.envelope.seal())

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
            self.poller.register(self.frontend, zmq.POLLIN)
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