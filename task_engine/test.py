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

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    # Instance the Task Client
    TC = TaskClient()

    # PACKAGE CREATION PROCESS
    # ------------------------
    # Generate a packing ID for a series off commands
    TC.generate_packing_id()
    # Create a meta frame for the package
    meta = TC.build_meta_frame('test')

    # Simple loop to express creating multiple task frames for each task in the package
    for i in range(20):
            # Build a task frame requesting the execution of task_get_count with the 
            # arguments 2 and 3
            TC.build_task_frame('task_get_count', [2, 3])

    # Send the package
    TC.send(meta)