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
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
from common.print_helpers import Colours
from common.print_helpers import printc
import time
import zmq
import hashlib
import collections

# Globals
# ------------------------------------------------------------------------ 79->
VOLUME = 70
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->
class TaskClient(object):
    """
    NAME:
    DESCRIPTION:
    """
    def __init__(self, name):
        super(TaskClient, self).__init__()
        self.task_socket = zmq.Context().socket(zmq.REQ)
        self.task_socket.connect('tcp://{}:{}'.format(ROUTER, ROUTER_FRONTEND))
        self.queue = collections.deque()
        self.results_queue = collections.deque()
        self.volume = VOLUME
        self.name = name
        self.meta = MetaFrame(0)
        self.data = DataFrame(0)

    def generate_packing_id(self):
        self.pack = time.time()

    def digest(self, message):
        if isinstance(message, str):
            return hashlib.md5(''.join(message).encode()).hexdigest().encode()
        elif isinstance(message, bytes):
            return hashlib.md5(''.join(message)).hexdigest().encode()

    def build_task_frame(self, func, args=[], nargs=[], kwargs={}):
        Task = TaskFrame(self.pack)
        Task.digest()
        Task.set_task(func.encode())
        Task.set_args(args)
        Task.set_nargs(nargs)
        Task.set_kwargs(kwargs)
        Task.set_pack(self.digest(str(time.time() - self.pack)))
        self.queue.append(Task.serialize())

    def build_meta_frame(self, id):
        Meta = MetaFrame(self.pack)
        Meta.digest()
        Meta.set_pack(str(self.pack).encode())
        Meta.set_id(id)
        Meta.set_version(b'0.1')
        Meta.set_type(b'REQ')
        Meta.set_role(self.name.encode())
        self.meta = Meta

    def task_queue(self, serial=None):
        message_hash = self.digest(str(self.queue))
        self.meta.set_length(len(self.queue))
        if serial == None:
            self.meta.set_serial(message_hash)
        else:
            self.meta.set_serial(serial)
        envelope = [self.meta.serialize()] 
        envelope.extend(self.queue)
        #print("Client Sending...")
        self.task_socket.send_multipart(envelope)
        del envelope
        response = self.task_socket.recv_multipart()
        #print("Client Received")
        self.results_queue.extend(response)
        del response
        #print('[CLIENT] recv: {0}'.format(self.results_queue[-1]))

    def setup_container(self, id):
        self.generate_packing_id()
        self.build_meta_frame(id)

    def insert(self, func, args=[], nargs=[], kwargs={}):
        self.build_task_frame(func, args, nargs, kwargs)

    def send(self, serial=None):
        self.task_queue(serial)
        self.queue.clear()
        self.meta = MetaFrame(0)

    def last(self):
        return self.results_queue[-1]

    def get(self):
        return self.results_queue

    def flush(self):
        self.results_queue.clear()

class DataClient(object):
    """
    NAME:
    DESCRIPTION:
    """
    def __init__(self, name):
        super(DataClient, self).__init__()
        print('create context')
        self.data_socket = zmq.Context().socket(zmq.SUB)
        print('connect: 127.0.0.1, 10003')
        self.data_socket.connect('tcp://{0}:{1}'.format('127.0.0.1', 10003))
        self.data_socket.setsockopt(zmq.SUBSCRIBE, 'sample')
        self.results_queue = []

    def receive(self):
        print('receive attempt')
        topic, message = self.data_socket.recv_multipart()
        print('split frame')
        self.results_queue.append(message)
        print('[CLIENT] recv: {0}'.format(self.results_queue[-1]))

# Functions
# ------------------------------------------------------------------------ 79->
def distribute(func=None, name='ANON', kwargs={}, nargs=[], args=[], buffer=[], serial=None):
    """
    NAME:           distribute
    DESCRIPTION:    send data to another task.
    REQUIRES:       name        - Tag for job owner
                    func        - The next function in the chain.
                    kwargs      - Keyword arguments for the next function, 
                                  and/or functions further down the pipeline 
                                  chain.
                    args        - Text arguments
                    nargs       - Numeric arguments
                    serial      - Cached serial for routing parent
                    buffer      - list of functions [optional]
    REQUIRED KWARGS:
                    pipeline    - A list of sequential functions in the 
                                  pipeline
    """
    TC = TaskClient(name)
    TC.setup_container(str(len(buffer)).encode())
    if func == None and buffer:
        while buffer:
            TC.insert(buffer.pop(), kwargs=kwargs, nargs=nargs, args=args)
    else:
        TC.insert(func, kwargs=kwargs, nargs=nargs, args=args)
    TC.send()
    response = list(TC.get())
    TC.flush()
    meta = MetaFrame(0)
    meta.load(meta.deserialize(response[0]))
    if serial != None:
        meta.set_serial(serial)
    data = DataFrame(0)
    data.load(data.deserialize(response[1]))
    printc('Distribute: {0}'.format(name), COLOURS.BLUE)
    return [meta.serialize(), data.serialize()]
    
# Main
# ------------------------------------------------------------------------ 79->