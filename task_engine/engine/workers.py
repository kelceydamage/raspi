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
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
import time
import json
import zmq

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

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        print('[WORKER-{0}({1})] Listener online'.format(self.pid, self.type))
        while True:
            message = self._socket.recv_multipart()
            print('[WORKER-{0}({1})] Received task: {2}'.format(
                self.pid, 
                self.type, 
                message[1]
                ))
            #response = self.run_task(message[1])
            pack = time.time()
            kwargs = {
            'id': self.id,
            'role': 'responder',
            'version': self.version,
            'type': 'ACK',
            'pack': pack
            }
            message = prepare(MetaFrame(pack), kwargs)
            print('[WORKER-{0}({1})] Task complete: {2}'.format(
                self.pid, 
                self.type,
                message
                ))
            self._socket.send_multipart([message, ])

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
        self._socket.connect('tcp://{}:{}'.format(dealer, dealer_port))
        self.functions = functions
        self.type = 'TASK'
        self.pid = pid
        self.id = '{0}-{1}'.format(self.type, self.pid)

    def run_task(self, task):
        """
NAME:           run_task
DESCRIPTION:    Return the result of executing the given task
REQUIRES:       task object [dict]
                - name
                - args
                - kwargs
        """
        print(task)
        task = json.loads(task)
        name = task['name']
        args = task['args']
        kwargs = task['kwargs']
        #return self.functions[name](*args, **kwargs)

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
        self.id = '{0}-{1}'.format(self.type, self.pid)

    def run_task(self, task):
        pass

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80