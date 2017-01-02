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
from tasks import *
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
        self.meta = {
            'id': '',
            'role': 'responder',
            'version': self.version,
            'type': '',
            'pack': ''
            }

    def log(self, action, message, _print):
        if _print == True:
            print('[WORKER-{0}({1})] {3}: {2}'.format(
                self.pid, 
                self.type, 
                message,
                action
                )) 

    def message(self, Frame, response):
        """
NAME:           message
DESCRIPTION:    method for packing a message to be send ready.
REQUIRES:       Frame [Frame classtype]
                response [task output]
        """
        pack = time.time()
        kwargs = {
        'data': response,
        'pack': pack
        }
        self.meta['pack'] = pack
        meta = prepare(MetaFrame(pack), self.meta)
        frame = prepare(Frame(pack), kwargs)
        return [meta, frame]

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        self.log('Listener online', '', True)
        while True:
            message = self._socket.recv_multipart()
            self.log('Received task', message, True)
            response = self.run_task(message[1])
            message = self.message(DataFrame, response)
            self.log('Task complete', message, True)
            self._socket.send_multipart(message)

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
        self.meta['id'] = '{0}-{1}'.format(self.type, self.pid)
        self.meta['type'] = 'ACK'

    def run_task(self, request):
        """
NAME:           run_task
DESCRIPTION:    Return the result of executing the given task
REQUIRES:       request message [JSON]
                - task
                - args
                - kwargs
        """
        try:
            request = json.loads(request)
            task = request['task']
            args = request['args']
            kwargs = request['kwargs']
            response = eval(self.functions[task])(*args, **kwargs)
        except Exception, e:
            response = 'ERROR: {0}'.format(e)
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

    def run_task(self, task):
        pass

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80