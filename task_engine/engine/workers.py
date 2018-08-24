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
from task_engine.conf.configuration import TASK_WORKERS
from common.datatypes import *
from common.print_helpers import printc
from common.print_helpers import padding
from common.print_helpers import Colours
from tasks import *
from multiprocessing import *
import time
import json
import zmq
import ujson
import base64
import lmdb
import collections
from zmq.devices import monitored_queue

# Globals
#-------------------------------------------------------------------------------- <-80
VERSION                 = b'0.1'
PAD                     = 0
COLOURS                 = Colours()

# Classes
#-------------------------------------------------------------------------------- <-80
class Worker(object):
    """
NAME:           Worker
DESCRIPTION:    A remote task executor.
    """

    def __init__(self, host='0.0.0.0', port='19500', functions=''):
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
        self.pid = pid
        self.pull_socket = self._context.socket(zmq.PULL)
        self.push_socket = self._context.socket(zmq.PUSH)
        self.pull_socket.connect('tcp://{0}:{1}'.format(backend, backend_port))
        self.push_socket.connect('tcp://{0}:{1}'.format(frontend, frontend_port))
        self.functions = functions
        self.type = 'TASK'

    def receive(self):
        envelope = Envelope()
        envelope.load(self.pull_socket.recv_multipart())
        return envelope

    def start(self):

        while True:
            envelope = self.receive()
            if envelope.lifespan > 0:
                envelope = self.run_task(envelope)
            else:
                raise Exception('Rounting Error, envelope has no lifespan')
            #print('worker-{0} <---'.format(self.pid))
            time.sleep(0.001)
            self.push_socket.send_multipart(envelope.seal())

    def run_task(self, envelope):
        header, meta, udf, data = envelope.unpack()
        func = udf.consume()
        kwargs = udf.extract()
        kwargs['data'] = data
        kwargs['worker'] = self.pid
        try:
            r = eval(self.functions[func])(kwargs)
        except Exception as e:
            raise Exception(e)
        envelope.pack(header, meta.extract(), udf.extract(), r)
        return envelope

class CacheWorker(Worker):
    """
NAME:           CacheWorker
DESCRIPTION:    A remote cache server. Child of Worker.
    """

    def __init__(self, pid):
        super(CacheWorker, self).__init__()
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
        """
        self.router_socket = self._context.socket(zmq.ROUTER)
        self.poller = zmq.Poller()
        self.type = 'CACHE'
        self.pid = pid
        mylmdb = lmdb.Environment(
            path='/opt/nvme/raspi/task_engine/cache',
            map_size=1000000000,
            subdir=True,
            map_async=True,
            writemap=True,
            max_readers=TASK_WORKERS,
            max_dbs=0,
            max_spare_txns=TASK_WORKERS,
            lock=True
        )
        self.lmdb = mylmdb
        print('cache loaded')

    def cache_key_set(self, key, value):
        with lmdb.Environment.begin(self.lmdb, write=True) as txn:
            txn.put(
                key,
                value,
                overwrite=True
                )

    def cache_key_get(self, key):
        with lmdb.Environment.begin(self.lmdb, write=True) as txn:
            return txn.get(key)

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        print('cache online')
        while True:
            socks = dict(self.poller.poll(10))
            if socks.get(self.router_socket) == zmq.POLLOUT:
                try:
                    cr = self.router_socket.recv_multipart()
                except Exception as e:
                    printc('[CACHE] (start): {0}'.format(str(e)), COLOURS.RED)
                result = self.run_task(cr)
                self.router_socket.send_multipart([cr[0], cr[1], result])

    def run_task(self, cr):
        req = Tools.deserialize(cr[2])
        key = Tools.deserialize(cr[3])
        if req == 'check':
            try:
                r = self.cache_key_get(key.encode())
                if r != None:
                    return Tools.serialize(True)
                else:
                    return Tools.serialize(False)
            except Exception as e:
                printc('[CACHE]: (check) {0}'.format(str(e)), COLOURS.RED)
                return Tools.serialize(False)
        elif req == 'get':
            return self.cache_key_get(key.encode())
        elif req == 'set':
            try:
                self.cache_key_set(key.encode(), cr[4])
                return Tools.serialize(True)
            except Exception as e:
                printc('[CACHE]: (set) {0}'.format(str(e)), COLOURS.RED)
                return Tools.serialize(False)

    def setup_router(self, host, port, proto='tcp'):
        """
NAME:           setup_router
DESCRIPTION:    Configure the router socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
        """
        try:
            self.router_socket.bind('{2}://{0}:{1}'.format(
                host, 
                port,
                proto
                ))
            self.poller.register(self.router_socket, zmq.POLLIN|zmq.POLLOUT)
        except Exception as e:
            printc('[CACHE] (setup_router): {0}'.format(str(e)), COLOURS.RED)
        printc('{0}cache online'.format(padding('[CACHE-{0}(ROUTER)] '.format(port), PAD)), COLOURS.GREEN)


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