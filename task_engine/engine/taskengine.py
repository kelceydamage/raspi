#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Doc
#-------------------------------------------------------------------------------- <-80
"""
Broker-less distributed task queue.
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import time
import json
import zmq

# Globals
#-------------------------------------------------------------------------------- <-80
HOST = '127.0.0.1'
PORT = 9999
TASK_SOCKET = zmq.Context().socket(zmq.REQ)
TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))

# Classes
#-------------------------------------------------------------------------------- <-80
class Worker(object):
    """
NAME: Worker
DESCRIPTION: A remote task executor.
    """

    def __init__(self, host=HOST, port=PORT):
        """
NAME:           __init__
DESCRIPTION:    Initialize worker.
REQUIRES:       host [ip/hostname]
                port [numeric port]
        """
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)

    def start(self):
        """
NAME:           start
DESCRIPTION:    Start listening for tasks.
        """
        self._socket.bind('tcp://{0}:{1}'.format(
            self.host, 
            self.port
            ))
        while True:
            task = self._socket.recv_pyobj()
            response = self.run_task(task)
            self._socket.send_pyobj(response)

    def run_task(self, task):
        """
NAME:           _do_work
DESCRIPTION:    Return the result of executing the given task
REQUIRES:       task object [dict]
                - name
                - args
                - kwargs
        """
        task = json.loads(task)
        name = task['name']
        args = task['args']
        kwargs = task['kwargs']
        return self.functions[name](*args, **kwargs)

# Functions
#-------------------------------------------------------------------------------- <-80
def task_queue(task):
    """
NAME:           queue
DESCRIPTION:    Return the result of running the task with the given 
                arguments.
REQUIRES:       task object [dict]
                - name
                - args
                - kwargs
    """
    task = json.dumps(task)
    TASK_SOCKET.send_pyobj(task)
    results = TASK_SOCKET.recv_pyobj()
    return results

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    w = Worker()
    w.start()