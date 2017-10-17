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

"""

# Imports
#-------------------------------------------------------------------------------- <-80
from client.client import TaskClient
from common.print_helpers import print_nested, print_package, printc, Colours
import json
import time

# Globals
#-------------------------------------------------------------------------------- <-80
COLOURS = Colours()

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    # Instance the Task Client
    TC = TaskClient('control-1')

    # PACKAGE CREATION PROCESS
    # ------------------------  
    # Create a meta frame for the package
    TC.setup_container('test')

    # Simple loop to express creating multiple task frames for each task 
    # in the package
    for i in range(10):

        # Build a task frame requesting the execution of task_get_count 
        # with the arguments 2 and 3
        TC.insert('task_get_count', [2, 3])
        TC.insert('task_double_cuda_matrix', [32, 32])

    # Send the package
    start = time.time()
    TC.send()

    # Optional results
    last = TC.last()
    end = time.time() - start
    print('\n\n')
    print('---------------------------------------------------------------')
    printc('CLIENT RESPONSE: {0}s'.format(end), COLOURS.BLUE)
    print('---------------------------------------------------------------')
    printc('RUN: {0}, params=[2, 3]'.format('task_get_count'), COLOURS.GREEN)
    printc('RUN: {0}, matrix=[32 * 32]'.format('task_double_cuda_matrix'), COLOURS.GREEN)
    print('---------------------------------------------------------------')
    for item in last:
        print_package(item)

