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
SUMMARY:        A class for spawning child services and collapsing them.
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
from processing import Processing
from multiprocessing import current_process
import os
import signal
import sys

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class ProcessSpawner(object):
    """
NAME:           ProcessSpawner
DESCRIPTION:    A class for spawning child services and collapsing them.
    """

    def __init__(self):
        super(ProcessSpawner, self).__init__()
        self.status = []

    def spawn(self, services):
        """
NAME:           spawn
DESCRIPTION:    starts the spawner process and retrieves the process objects.
REQUIRES:       services [list of functions]
    """
        current_process().daemon = False
        processing_object = Processing()
        self.q = processing_object.create_queue()
        p = processing_object.new_process(
            self._child_process,
            [processing_object, services]
            )
        status = [] 
        for service in services:
            queue_response = self.q.get(timeout=4)
            self.status.append(queue_response)

    def _child_process(self, processing_object, services):
        """
NAME:           spawn
DESCRIPTION:    starts the spawner process and retrieves the process objects.
REQUIRES:       processing_object [class instance]
                services [list of functions]
    """

        def __start(self, service):
            """
NAME:           start
DESCRIPTION:    Start the requested service.
REQUIRES:       services [list of functions]
    """
            try:
                pid = os.getpid()
                print('Starting process [{0}]: {1}'.format(pid, service[0]))
                reply = ['success', pid, service] 
                self.q.put(reply)
                service[0](service[1])
            except Exception as e:
                reply = ['FAIL: {0}'.format(e), pid, service] 
                self.q.put(reply)

        for service in services:
            p = processing_object.new_process(
                __start,
                [self, service]
                )

    def kill_proc(self, status):
        """
NAME:           kill_proc
DESCRIPTION:    Kill all the outstanding processes.
REQUIRES:       status [output of self.spawn]
"""
        for process in status:
            try:
                os.kill(int(process[1]), signal.SIGTERM)
            except OSError, e:
                print('Error: {0}'.format(e))
            else:
                print('Sucessfully terminated process [{0}]: {1}'.format(
                    process[1],
                    process[2][0]
                    ))

class ProcessHandler(ProcessSpawner):
    """
NAME:           ProcessHandler
DESCRIPTION:    Handles the safe exit and cleanup of spawning multiple processes
    """
    def __init__(self, services):
        super(ProcessHandler, self).__init__()
        self.services = services
        signal.signal(signal.SIGINT, self.ctrl_c)

    def start(self):
        """
NAME:           start
DESCRIPTION:    Starts the given services using ProcessSpawner and collects the PIDs
REQUIRES:       services [list of functions]
        """
        print('### Type [ctrl-c] to exit and shutdown workers ###')
        self.spawn(self.services)

    def ctrl_c(self, signal, frame):
        """
NAME:           ctrl_c
DESCRIPTION:    Handler for trapped ctrl-c commands
        """
        print('\nClosing application and stopping services...')
        print(self.status)
        self.kill_proc(self.status)
        sys.exit(0)

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80

