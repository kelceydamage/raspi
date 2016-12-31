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

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import requests
import time
import zmq
import json

# Globals
#-------------------------------------------------------------------------------- <-80
HOST = '127.0.0.1'
PORT = 9000
TASK_SOCKET = zmq.Context().socket(zmq.REQ)
TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def task_queue(task, meta):
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
    meta = json.dumps(meta)
    TASK_SOCKET.send_multipart([task, meta])
    results = TASK_SOCKET.recv_multipart()
    return results

# Main
#-------------------------------------------------------------------------------- <-80
start = time.time()
task_request = {
    'name': 'count',
    'args': [2, 3],
    'kwargs': {}
    }

for i in range(0, 1):
	result = task_queue(task_request, {'requestor': 111})

print(result)
end = time.time() - start
print('running {0} samples, took: {2}'.format(
	10000,
	result,
	end
	))