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
from task_engine.conf.configuration import ENABLE_STDOUT
from task_engine.conf.configuration import ENABLE_DEBUG
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
from common.print_helpers import printc
from common.print_helpers import Colours
from tasks import *
import time
import json
import zmq
import ujson
import base64

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION                 = b'0.1'
COLOURS                 = Colours()

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
        self.meta.set_version(self.version)

    def log(self, action, message):
        if ENABLE_STDOUT == True:
            printc('[WORKER-{0}({1})] {3}: {2}'.format(
                self.pid, 
                self.type, 
                message,
                action
                ), COLOURS.GREEN) 

    def message(self, response, meta):
        """
NAME:           message
DESCRIPTION:    method for packing a message to be send ready.
REQUIRES:       Frame [Frame classtype]
                response [task output]
        """
        self.meta.set_serial(meta.get_serial())
        self.meta.set_part(meta.get_part())
        self.meta.set_pack(meta.get_pack())
        self.meta.set_length(1)
        self.data.set_pack(self.meta.get_pack())
        self.data.set_size(len(response))
        self.data.set_data(response)
        t = self.data.serialize()
        return [self.meta.serialize(), self.data.serialize()]

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        self.log('Listener online', '')
        while True:
            message = self._socket.recv_multipart()
            meta = MetaFrame(0)
            meta.load(meta.deserialize(message[0]))
            valid = self.recv_validation(meta, message)
            if valid == False:
                message = self.message(b'ERROR: Invalid request', self.meta.serialize())
            else:
                self.log(
                    'Received task', 
                    'Package {0}, Chunk {1}'.format(meta.get_serial(), meta.get_part())
                    )
                response = self.run_task(message[1:])
                message = self.message(response, meta)
            self._socket.send_multipart(message)
            

    def recv_validation(self, meta, message):
        """
NAME:           recv_validation
DESCRIPTION:    Validate incoming requests
        """
        if meta.get_length() == len(message[1:]):
            return True
        return False

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
        self._socket = self._context.socket(zmq.REP)
        self._socket.connect('tcp://{0}:{1}'.format(dealer, dealer_port))
        self.functions = functions
        self.type = 'TASK'
        self.pid = pid
        self.meta.set_role(b'responder')
        self.meta.set_id('{0}-{1}'.format(self.type, self.pid).encode())
        self.meta.set_type(b'ACK')
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
        for item in request:
            task = TaskFrame(0)
            task.load(task.deserialize(item))
            try:
                func = task.get_task()
                args = task.get_args()
                nargs = task.get_nargs()
                kwargs = task.get_kwargs()
                r = {'job-{0}'.format(task.get_pack()): eval(self.functions[func.decode()])(*args, *nargs, **kwargs)}
            except Exception as e:
                r = {'job-{0}'.format(frame['pack']): 'ERROR: {0}'.format(e)}
            i += 1
            response.append(r)
        return response

class DataWorker(Worker):
    """
NAME:           DataWorker
DESCRIPTION:    A remote data subscriber. Child of Worker.
    """

    def __init__(self, host, port, pid, service):
        super(DataWorker, self).__init__(host, port)
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
        """
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind('tcp://{0}:{1}'.format(host, port))
        self.service = service
        self.type = 'DATA'
        self.pid = pid
        self.meta.set_role(b'publisher')
        self.meta.set_id('{0}-{1}'.format(self.type, self.pid).encode())
        self.meta.set_type(b'PUB')
        self.hash = self.data.hash

    def run_task(self):
        """
NAME:           run_task
DESCRIPTION:    Return the result of executing the given task
REQUIRES:       request message [JSON]
                - task
                - args
                - kwargs
        """
        response = []
        response.append('job-{0}: {1}'.format(
            self.service,
            #eval(self.functions[task])(*args, **kwargs))
            'sample')
        )
        return response

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        self.log('Publisher online', '')
        while True:
            #response = self.run_task()
            #meta = self.meta.serialize()
            #self.data.message['data'] = response
            #frame = self.data.serialize()
            #message = [meta, frame]
            message = 'hello world'
            print(message)
            topic = 'sample'
            frame = '{0} {1}'.format(topic, message)
            print(frame)
            try:
                self._socket.send_multipart([topic, message])
            except Exception as e:
                print(e)
            time.sleep(0.05)

# Functions
#-------------------------------------------------------------------------------- <-80
def _test(obj):
    return True

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    TW = TaskWorker('127.0.0.1', 10000, os.getpid, '127.0.0.1', 9001, {})
    TW.start()