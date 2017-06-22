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
SUMMARY:        Utility for starting aand configuring a task_engine cluster
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
from registry.registry import load_tasks
from engine.workers import TaskWorker, DataWorker
from engine.routers import Router
from conf.configuration import *
from common.spawner import ProcessHandler
import argparse

# Globals
#-------------------------------------------------------------------------------- <-80

# Parser
#-------------------------------------------------------------------------------- <-80
parser = argparse.ArgumentParser(prog="Task Engine")
group_1 = parser.add_argument_group('Mode Of Operation')
group_1.add_argument(
    'mode', 
    nargs='?',
    help='Available modes: ROUTER, TASK, DATA'
    )
group_2 = parser.add_argument_group('Parameters')
group_2.add_argument(
    '-a', 
    "--address", 
    dest="address", 
    help="Specify listening ip address [ex: 0.0.0.0]"
    )
group_2.add_argument(
    '-p', 
    "--port", 
    dest="port", 
    help="Specify listening port [ex: 10001]"
    )
args = parser.parse_args()

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def start_worker(args, pid):
    """
NAME:           start_worker
DESCRIPTION:    Wrapper for starting worker class instances with ProcessHandler
    """
    if args[-1] == 0:
        print('Starting [ROUTER] on socket: {0}:{1}'.format(args[0], ROUTER_FRONTEND))
        R = Router(pid=pid)
        R.setup_frontend('0.0.0.0', ROUTER_FRONTEND)
        R.setup_backend('0.0.0.0', ROUTER_BACKEND)
        R.start()
    elif args[-1] == 1:
        print('Starting worker[TASK] on socket: {0}:{1}'.format(args[0], args[1]))
        TaskWorker(
            host=args[0], 
            port=args[1], 
            pid=pid,
            dealer=ROUTER, 
            dealer_port=ROUTER_BACKEND, 
            functions=args[2],
            ).start()
    elif args[-1] == 2:
        print('Starting worker[DATA] on socket: {0}:{1}'.format(args[0], args[1]))
        DataWorker(
            host=args[0], 
            port=args[1],
            pid=pid,
            service='test'
            ).start()

def gen_services(host, port, mode):
    """
NAME:           gen_services
DESCRIPTION:    Populates the SERVICES list for ProcessHandler
    """
    def _loop(count, worker_type, port, host, functions=''):
        for i in range(count):
            SERVICES.append([start_worker, [host, port, functions, worker_type]])
        return SERVICES

    functions = load_tasks('../tasks')
    SERVICES = []
    try:
        if mode == 'router':
            if host == None:
                raise
            else:
                SERVICES = _loop(1, 0, port, host)
        elif mode == 'task':
            if host == None or port == None:
                raise
            else:
                SERVICES = _loop(TASK_WORKERS, 1, port, host, functions)
        elif mode == 'data':
            if host == None or port == None:
                raise
            else:
                SERVICES = _loop(DATA_WORKERS, 2, port, host, functions)
    except Exception, e:
        print('Invald options and arguments provided. Unable to start services')
        exit(1)

    return SERVICES, functions

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    if not args.mode or not args.address:
        parser.print_help()
        exit(1)
    SERVICES, functions = gen_services(args.address, args.port, args.mode.lower())
    PH = ProcessHandler(SERVICES)
    print('[REGISTERED-TASKS]: \n[-] {0}'.format('\n[-] '.join(functions.keys())))
    print('------------------')
    PH.start()
