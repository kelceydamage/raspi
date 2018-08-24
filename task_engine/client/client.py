#!/usr/bin/env python3
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->

# Imports
# ------------------------------------------------------------------------ 79->
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
from task_engine.conf.configuration import RESPONSE_TIME
from task_engine.conf.configuration import ROUTER
from task_engine.conf.configuration import ROUTER_FRONTEND
from task_engine.conf.configuration import ROUTER_PUBLISHER
from task_engine.conf.configuration import CACHE_SERVER
from task_engine.conf.configuration import CACHE_PORT
from common.datatypes import Envelope
from common.datatypes import Tools
from common.print_helpers import Colours
from common.print_helpers import printc
import zmq

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->
class TaskClient(object):
    """
    NAME:
    DESCRIPTION:
    """
    def __init__(self):
        super(TaskClient, self).__init__()
        self.push_addr = 'tcp://{}:{}'.format(ROUTER, ROUTER_FRONTEND)
        self.sub_addr = 'tcp://{}:{}'.format('127.0.0.1', 19300)
        self.push_socket = zmq.Context().socket(zmq.PUSH) #REQ
        self.sub_socket = zmq.Context().socket(zmq.SUB)
        self.push_socket.connect(self.push_addr)
        self.sub_socket.connect(self.sub_addr)
        self.sub_socket.set(zmq.SUBSCRIBE, b'0')
        self.poller = zmq.Poller()
        self.poller.register(self.sub_socket, zmq.POLLIN|zmq.POLLOUT)
        self.envelope = Envelope()

    def register(self):
        self.sub_socket.set(zmq.SUBSCRIBE, self.envelope.get_header())
        self.push_socket.send_multipart(self.envelope.seal())
        self.envelope.empty()

    def cleanup(self):
        self.push_socket.disconnect(self.push_addr)
        self.sub_socket.disconnect(self.sub_addr)
    
    def poll(self):
        msg = None
        while True:
            socks = dict(self.poller.poll(timeout=RESPONSE_TIME))
            if socks.get(self.sub_socket) == zmq.POLLIN:
                msg = self.sub_socket.recv_multipart(flags=0)
                if msg[0] == b'0':
                    continue
                else:
                    break
        return msg

    def distribute(self, envelope):
        self.envelope = envelope
        self.register()
        printc('[CLIENT] Sending', COLOURS.PURPLE)
        self.envelope.load(self.poll())
        self.cleanup()
        return self.envelope

class CacheClient(object):
    def __init__(self):
        try:
            self.req_addr = 'tcp://{}:{}'.format(CACHE_SERVER, CACHE_PORT)
            self.req_socket = zmq.Context().socket(zmq.REQ)
            self.req_socket.connect(self.req_addr)
        except Exception as e:
            printc('[CACHE_CLIENT]: (__init__) {0}'.format(str(e)), COLOURS.RED)

    def send(self, message):
        msg = [Tools.serialize(x) for x in message]
        try:
            self.req_socket.send_multipart(msg)
        except Exception as e:
            printc('[CACHE_CLIENT]: (send) {0}'.format(str(e)), COLOURS.RED)
        while True:
            try:
                r = self.req_socket.recv_multipart()
            except Exception as e:
                print(str(e))
            break
        return Tools.deserialize(r[0])

# Functions
# ------------------------------------------------------------------------ 79->
    
# Main
# ------------------------------------------------------------------------ 79->