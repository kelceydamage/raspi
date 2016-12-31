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
SUMMARY:        A simple wrapper class for the python multiprocessing module.
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from multiprocessing import Process, Pool, Queue

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class Processing(object):
    """
NAME:           Processing
DESCRIPTION:    A simple wrapper class for the python multiprocessing module.
    """

    def __init__(self):
        super(Processing, self).__init__()

    def create_queue(self):
        """
NAME:           create_queue
DESCRIPTION:    Return a Queue object.
        """
        queue = Queue()
        return queue

    def generate_pool(self, processes=4):
        """
NAME:           generate_pool
DESCRIPTION:    Return a processing pool
REQUIRES:       processes [number of procs in the pool]
        """
        pool = Pool(processes)
        return pool

    def new_process_pool(self, pool, func, *args, **kwargs):
        """
NAME:           new_process_pool
DESCRIPTION:    Execute a function within a process pool
REQUIRES:       pool [process pool]
                func [function]
                args
        """
        result = pool.apply_async(func, *args, **kwargs)
        return result

    def new_process(self, func, args):
        """
NAME:           new_process
DESCRIPTION:    execute a function in a subprocess and return the process object
REQUIRES:       func [function]
                args
        """
        process = Process(target=func, args=args)
        process.start()
        return process

    def new_process_map(self, pool, func, *args, **kwargs):
        """
NAME:           new_process_pool
DESCRIPTION:    Execute a function on all processes in a process pool
REQUIRES:       pool [process pool]
                func [function]
                args
        """
        result = pool.map(func, *args, **kwargs)
        return result

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80