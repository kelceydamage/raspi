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
SUMMARY:        Demo task shipper
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from conf.configuration import RESPONSE_TIME
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
import requests
import time
import zmq
import json
import md5

# Globals
#-------------------------------------------------------------------------------- <-80
HOST = '127.0.0.1'
PORT = 9000
TASK_SOCKET = zmq.Context().socket(zmq.REQ)
TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))
Q = []

VOLUME = 70
# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def digest(message):
    return md5.md5(''.join(message)).hexdigest()

def task_queue(m, q):
    """
NAME:           queue
DESCRIPTION:    Return the result of running the task with the given 
                arguments.
REQUIRES:       task object [dict]
                - name
                - args
                - kwargs
    """
    message_hash = digest(q)
    m.message['length'] = len(q)
    m.message['serial'] = message_hash
    envelope = [m.serialize()] + q
    print('sending...')
    TASK_SOCKET.send_multipart(envelope)
    results = TASK_SOCKET.recv_multipart()
    print('[CLIENT] recv: {0}'.format(results))
    #return results

# Main
#-------------------------------------------------------------------------------- <-

start = time.time()
s2 = time.time()
results = []

# Pack is simply a time epoch which can be used to identify all frames in an envelope
pack = time.time()
T = TaskFrame(pack)
M = MetaFrame(pack)
M.digest()
T.digest()
M.message['id'] = 'CLIENT'
M.message['version'] = 0.1
M.message['type'] = 'REQ'
M.message['role'] = 'requestor'

T.message['pack'] = T.hash
n = 0

for i in range(VOLUME):
    #print(i)
    # prepare is a helper function that will enforce correct message structure. however for
    # slightly more performance you can just call json.dumps() om a dict and send.
    T.message['task'] = 'task_get_average'
    T.message['args'] = [2, 3]
    T.message['kwargs'] = {}
    T.message['pack'] = digest(str(time.time() - start))

    # prepare is a helper function that will enforce correct message structure. however for
    # slightly more performance you can just call json.dumps() om a dict and send.

#for i in range(0, 1000):
    #print('[CLIENT] Sending: {0}'.format([meta, task]))
    Q.append(T.serialize())
    if time.time() - start >= RESPONSE_TIME:
        M.message['pack'] = pack
        print('send')
        task_queue(M, Q)
        start = time.time()
        Q = []
        pack = time.time()
        n += 1
    #print('[CLIENT] Received: {0}'.format(result))

"""
for i in range(100):
    t = json.dumps({})
    TASK_SOCKET.send_multipart([t])
    results = TASK_SOCKET.recv_multipart()
    print(results)
    #end = time.time() - s2
"""
end = time.time() - s2
print('running {0} samples, took: {2}'.format(
    VOLUME,
    results,
    end
    ))

# enable to see output
#print(results)

