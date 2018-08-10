#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Doc
#-------------------------------------------------------------------------------- <-80

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
from task_engine.conf.configuration import RESPONSE_TIME
from task_engine.conf.configuration import ROUTER
from task_engine.conf.configuration import ROUTER_FRONTEND
from raspi.common.datatypes import TaskFrame
from raspi.common.datatypes import MetaFrame
from raspi.common.datatypes import prepare
import time
import zmq
import json
import hashlib

# Globals
#-------------------------------------------------------------------------------- <-80
VOLUME = 70

# Classes
#-------------------------------------------------------------------------------- <-80
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
            return hashlib.md5(''.join(message).encode()).hexdigest()
        elif isinstance(message, bytes):
            return hashlib.md5(''.join(message)).hexdigest()

    def build_task_frame(self, task, args=[], kwargs={}):
        Task = TaskFrame(self.pack)
        Task.digest()
        Task.message['pack'] = Task.hash
        Task.message['task'] = task
        Task.message['args'] = args
        Task.message['kwargs'] = kwargs
        Task.message['pack'] = self.digest(str(time.time() - self.pack))
        self.queue.append(Task.serialize())

    def build_meta_frame(self, id):
        Meta = MetaFrame(self.pack)
        Meta.digest()
        Meta.message['pack'] = self.pack
        Meta.message['id'] = id
        Meta.message['version'] = 0.1
        Meta.message['type'] = 'REQ'
        Meta.message['role'] = self.name
        self.meta = Meta

    def task_queue(self):
        message_hash = self.digest(self.queue)
        self.meta.message['length'] = len(self.queue)
        self.meta.message['serial'] = message_hash
        envelope = [self.meta.serialize()] + self.queue
        print("Client Sending...")
        print(envelope)
        self.task_socket.send_multipart(envelope)
        print("Client Receiving")
        response = self.task_socket.recv_multipart()
        print(response)
        self.results_queue.append(response)

        print('[CLIENT] recv: {0}'.format(self.results_queue[-1]))

    def setup_container(self, name):
        self.generate_packing_id()
        self.build_meta_frame(name)

    def insert(self, task, args):
        self.build_task_frame(task, args)

    def send(self):
        self.task_queue()
        self.queue = []
        self.meta = None

    def deserialize(self, frame):
        try:
            return [json.loads(x.decode()) for x in frame]
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
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
