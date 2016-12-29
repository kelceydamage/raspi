#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Doc
#-------------------------------------------------------------------------------- <-80

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
from engine.taskengine import task_queue
import requests
import time

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
start = time.time()
task_request = {
    'name': 'count',
    'args': [2, 3],
    'kwargs': {}
    }

for i in range(0, 10000):
	result = task_queue(task_request)

end = time.time() - start
print('running {0} samples, took: {2}'.format(
	10000,
	result,
	end
	))