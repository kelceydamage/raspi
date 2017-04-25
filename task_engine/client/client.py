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
from conf.configuration import RESPONSE_TIME
from conf.configuration import ROUTER
from conf.configuration import ROUTER_FRONTEND
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import prepare
import time
import zmq
import json
import md5

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
        return md5.md5(''.join(message)).hexdigest()

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

    def task_queue(self, meta):
        message_hash = self.digest(self.queue)
        self.meta.message['length'] = len(self.queue)
        self.meta.message['serial'] = message_hash
        envelope = [self.meta.serialize()] + self.queue
        self.task_socket.send_multipart(envelope)
        self.results_queue.append(self.task_socket.recv_multipart())

        print('[CLIENT] recv: {0}'.format(self.results_queue[-1]))

    def setup_container(self, name):
        self.generate_packing_id()
        self.build_meta_frame(name)

    def insert(task, args):
        self.build_task_frame(task, args)

    def send(self):
        self.task_queue()
        self.queue = []
        self.meta = None

    def last(self):
        return self.results_queue[-1]

    def flush(self):
        self.results_queue = []

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
