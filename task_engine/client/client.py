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
from common.datatypes import prepare
import time
import zmq
import hashlib

# Globals
# ------------------------------------------------------------------------ 79->
VOLUME = 70

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
        self.queue = []
        self.results_queue = []
        self.volume = VOLUME
        self.name = name

    def generate_packing_id(self):
        self.pack = time.time()

    def digest(self, message):
        if isinstance(message, str):
            return hashlib.md5(''.join(message).encode()).hexdigest().encode()
        elif isinstance(message, bytes):
            return hashlib.md5(''.join(message)).hexdigest().encode()

    def build_task_frame(self, task, args=[], nargs=[], kwargs={}):
        Task = TaskFrame(self.pack)
        Task.digest()
        Task.set_task(task.encode())
        Task.set_args(args)
        Task.set_nargs(nargs)
        Task.set_kwargs(kwargs)
        Task.set_pack(self.digest(str(time.time() - self.pack)))
        self.queue.append(Task.serialize())

    def build_meta_frame(self, id):
        Meta = MetaFrame(self.pack)
        Meta.digest()
        Meta.set_pack(str(self.pack).encode())
        Meta.set_id(bytes(id, 'utf-8'))
        Meta.set_version(b'0.1')
        Meta.set_type(b'REQ')
        Meta.set_role(self.name.encode())
        self.meta = Meta

    def task_queue(self):
        message_hash = self.digest(str(self.queue))
        self.meta.set_length(len(self.queue))
        self.meta.set_serial(message_hash)
        envelope = [self.meta.serialize()] + self.queue
        print("Client Sending...")
        #print('ENVELOPE: ', envelope)
        self.task_socket.send_multipart(envelope)
        response = self.task_socket.recv_multipart()
        print("Client Received")
        self.results_queue.append(response)
        #print('[CLIENT] recv: {0}'.format(self.results_queue[-1]))

    def setup_container(self, name):
        self.generate_packing_id()
        self.build_meta_frame(name)

    def insert(self, task, args=[], nargs=[], kwargs={}):
        self.build_task_frame(task, args, nargs, kwargs)

    def send(self):
        self.task_queue()
        self.queue = []
        self.meta = None

    def deserialize(self, frame):
        try:
            return [eval(x.decode(), {"__builtins__":None}, {}) for x in frame]
        except Exception as e:
            return frame

    def last(self):
        return self.deserialize(self.results_queue[-1])

    def get(self):
        return_queue = []
        for frame in self.results_queue:
            return_queue.append(self.deserialize(frame))
        return return_queue

    def flush(self):
        self.results_queue = []

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

# Main
# ------------------------------------------------------------------------ 79->