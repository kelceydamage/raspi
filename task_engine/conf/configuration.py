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

# Globals
#-------------------------------------------------------------------------------- <-80
# Workers
STARTING_PORT = 10000
TASK_WORKERS = 16        # Worker processes per node (per physical server)
DATA_WORKERS = 1
RESPONSE_TIME = 0.005   # Controls the rate at which tasks are sent to the workers,
                        # and in doing so, the size of the queue. 
                        # Example: 
                        #       1000 req @0.01 = ~100 tasks per queue
                        #       1000 reg @0.001 = ~10 tasks per queue
                        # A higher response time increases throughput at the cost of
                        # the systems responsiveness.

# Router
ROUTER = '127.0.0.1'
ROUTER_FRONTEND = 19000
ROUTER_BACKEND = 19001
CHUNKING = True         # Chunking determines if and how much the router breaks up 
                        # queues in order the better balance worker loads.
                        # Example:
                        #       chunking = 10 will break up all queues int ~ 10 tasks
                        #       per worker. This will negativly affect response time
                        #       since it adds delay at the router, and extra network 
                        #       activity.
                        # RESPONSE_TIME and CHUNKING should be balanced to get an 
                        # Optimal throughput and worker load balance.   
CHUNKING_SIZE = 500

# Logging
ENABLE_STDOUT = False
ENABLE_DEBUG = False

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
