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
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from registry.registry import functions
from engine.workers import TaskWorker, DataWorker
#from engine.routers import Router
from conf.configuration import *
from common.spawner import ProcessHandler

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def start_worker(args):
    """
NAME:           start_worker
DESCRIPTION:    Wrapper for starting worker class instances with ProcessHandler
    """
    if args[-1] == 0:
        print('Starting worker[TASK] on socket: {0}:{1}'.format(args[0], args[1]))
        TaskWorker(host=args[0], port=args[1], functions=args[2]).start()
    elif args[-1] == 1:
        print('Starting worker[DATA] on socket: {0}:{1}'.format(args[0], args[1]))
        DataWorker(host=args[0], port=args[1]).start()

def gen_services():
    """
NAME:           gen_services
DESCRIPTION:    Populates the SERVICES list for ProcessHandler
    """
    def _loop(count, worker_type, port):
        for i in range(count):
            SERVICES.append([start_worker, [HOST, port, functions, worker_type]])
            port += 1
        return SERVICES, port

    SERVICES = []
    port = STARTING_PORT
    SERVICES, port = _loop(TASK_WORKERS, 0, port)
    SERVICES, port = _loop(DATA_WORKERS, 1, port)
    return SERVICES

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    SERVICES = gen_services()
    PH = ProcessHandler(SERVICES)
    PH.start()
