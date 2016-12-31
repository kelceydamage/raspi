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
from registry.registry import functions
from engine.workers import TaskWorker
#from engine.routers import Router
from conf.configuration import *
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.spawner import ProcessHandler
import time

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def test():
    while True:
        time.sleep(1)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    #w = TaskWorker(HOST, PORT)
    #w.functions = functions
    #w.start()
    services = [
        test,
        test
    ]
    PH = ProcessHandler(services)
    PH.start()
