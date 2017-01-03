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
SUMMARY:        Broker-less distributed task workers.
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
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
from tasks import *
import time
import json
import zmq
import md5

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION = 0.1

# Classes
#-------------------------------------------------------------------------------- <-80
class Worker(object):
    """
NAME:           Worker
DESCRIPTION:    A remote task executor.
    """

    def __init__(self, host, port, functions=''):
        super(Worker, self).__init__()
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
REQUIRES:       host [ip/hostname]
                port [numeric port]
        """
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self.version = VERSION
        self.data = DataFrame(0)
        self.task = TaskFrame(0)
        self.meta = MetaFrame(0)
        self.meta.message['version'] = self.version

    def deserialize(self, frame):
        return json.loads(frame)

    def log(self, action, message):
        if ENABLE_STDOUT == True:
            print('[WORKER-{0}({1})] {3}: {2}'.format(
                self.pid, 
                self.type, 
                message,
                action
                )) 

    def message(self, response, meta):
        """
NAME:           message
DESCRIPTION:    method for packing a message to be send ready.
REQUIRES:       Frame [Frame classtype]
                response [task output]
        """
        meta = self.deserialize(meta)
        self.meta.message['serial'] = meta['serial']
        self.meta.message['part'] = meta['part']
        self.meta.message['pack'] = meta['pack']
        self.meta.message['length'] = 1
        self.data.message['pack'] = meta['pack']
        self.data.message['size'] = len(response)
        self.data.message['data'] = response
        meta = self.meta.serialize()
        frame = self.data.serialize()
        return [meta, frame]

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        self.log('Listener online', '')
        while True:
            m = self._socket.recv_multipart()
            print('W-recv')
            self._socket.send_multipart(m)
            print('W-sent')
            """
            #message = self._socket.recv_multipart()
            print(999999)
            #message = self.recv_validation(message)
            if message == None:
                message = self.message(b'ERROR: Invalid request', self.meta.serialize())
            else:
                self.log('Received task', message[0])
                #response = self.run_task(message[1:])
                response = [{'done': 'done'}]
                #message = self.message(response, message[0])
                self.log('Task complete', message)
            print(77)
            self._socket.send_multipart(message)
            """

    def recv_validation(self, message):
        """
NAME:           recv_validation
DESCRIPTION:    Validate incoming requests
        """
        print('WORKER: {0}'.format(message))
        val1 = False
        meta = json.loads(message[0])
        print('@@@@@@@@@@')
        print(meta['length'])
        print(len(message[1:]))
        if meta['length'] == len(message[1:]):
            val1 = True
        if val1 == True:
            return message
        else:
            return None

class TaskWorker(Worker):
    """
NAME:           TaskWorker
DESCRIPTION:    A remote parallel task executor. Child of Worker.
    """

    def __init__(self, host, port, pid, dealer, dealer_port, functions):
        super(TaskWorker, self).__init__(host, port)
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
        """
        self._socket = self._context.socket(zmq.ROUTER)
        self._socket.connect('tcp://{}:{}'.format(dealer, dealer_port))
        self.functions = functions
        self.type = 'TASK'
        self.pid = pid
        self.meta.message['role'] = 'responder'
        self.meta.message['id'] = '{0}-{1}'.format(self.type, self.pid)
        self.meta.message['type'] = 'ACK'
        self.hash = self.task.hash

    def run_task(self, request):
        """
NAME:           run_task
DESCRIPTION:    Return the result of executing the given task
REQUIRES:       request message [JSON]
                - task
                - args
                - kwargs
        """
        i = 0
        response = []
        for frame in request:
            frame = self.deserialize(frame)
            try:
                task = frame['task']
                args = frame['args']
                kwargs = frame['kwargs']
                response.append('job-{0}: {1}'.format(
                    frame['pack'],
                    eval(self.functions[task])(*args, **kwargs))
                )
            except Exception, e:
                response.append('job-{0}: {1}'.format(
                    frame['pack'],
                    'ERROR: {0}'.format(e))
                )
            i += 1
        return response

class DataWorker(Worker):
    """
NAME:           DataWorker
DESCRIPTION:    A remote data subscriber. Child of Worker.
    """

    def __init__(self, host, port, pid):
        super(DataWorker, self).__init__(host, port)
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
        """
        self._socket = self._context.socket(zmq.SUB)
        self.type = 'DATA'
        self.pid = pid
        self.meta['id'] = '{0}-{1}'.format(self.type, self.pid)
        self.hash = self.data.hash

    def run_task(self, task):
        pass

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    TW = TaskWorker('127.0.0.1', 10000, os.getpid, '127.0.0.1', 9001, {})
    TW.start()