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
from task_engine.conf.configuration import ROUTER_BACKEND
from common.datatypes import Envelope
from common.datatypes import Udf
from common.datatypes import Meta
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
        self.envelope = Envelope()

    def r_log(self, message, header):
        printc(header, COLOURS.CORAL)
        print(len(message))
        for item in message:
            print('DEBUG: ', item[:160])
        print('END: ')

    def r_log2(self, message, header):
        printc(header, COLOURS.GREEN)
        print(len(message))
        for item in message:
            print('DEBUG: ', item[:160])
        print('END: ')

    def log(self, action, message):
        if ENABLE_STDOUT == True:
            printc('[WORKER-{0}({1})] {3}: {2}'.format(
                self.pid, 
                self.type, 
                message,
                action
                ), COLOURS.GREEN) 

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        print('listener online')
        while True:
            try:
                self.envelope.empty()
                self.envelope.load(self.pull_socket.recv_multipart())
            except Exception as e:
                printc('[WORKER] (start): {0}'.format(str(e)), COLOURS.RED)
            self.run_task()
            self.push_socket.send_multipart(self.envelope.seal())

class TaskWorker(Worker):
    """
NAME:           TaskWorker
DESCRIPTION:    A remote parallel task executor. Child of Worker.
    """

    def __init__(self, host, port, pid, backend, backend_port, frontend, frontend_port, functions):
        super(TaskWorker, self).__init__(host, port)
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
        """
        self.pull_socket = self._context.socket(zmq.PULL)
        self.push_socket = self._context.socket(zmq.PUSH)
        self.pull_socket.connect('tcp://{0}:{1}'.format(backend, backend_port))
        self.push_socket.connect('tcp://{0}:{1}'.format(frontend, frontend_port))
        self.functions = functions
        self.type = 'TASK'
        self.pid = pid

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
        udf = self.envelope.get_udf()
        meta = self.envelope.get_meta()
        func = udf.consume()
        meta.lifespan -= 1
        if len(udf.data) > 0:
            for item in udf.data:
                try:
                    container = udf.extract_less()
                    container['data'] = [item]
                    r = eval(self.functions[func])(container)
                except Exception as e:
                    printc('[WORKER] (run_task_multi): {0}'.format(str(e)), COLOURS.RED)
                    exit()
                response.append(r)
        else:
            try:
                r = eval(self.functions[func])(udf.extract())
            except Exception as e:
                printc('[WORKER] (run_task): {0}'.format(str(e)), COLOURS.RED)
                exit()
            response = r
        udf.set_data(response)
        print(len(udf.data))
        self.envelope.update_contents(meta, udf)

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