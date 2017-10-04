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
<<<<<<< HEAD:BOUNCE_CLUSTER.py

=======
Dummy interface for testing 
>>>>>>> a9c8de734127b01ee34838eecf0eab6d19bb5c93:data_collector/interfaces/interface_dummy.py
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
<<<<<<< HEAD:BOUNCE_CLUSTER.py
import os
import commands
import argparse

# Globals
#-------------------------------------------------------------------------------- <-80
NODES = 8

# Parser
#-------------------------------------------------------------------------------- <-80
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--remote-server", action="store", dest='server')
args = parser.parse_args()

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def gen_node_hosts(nodes):
	hosts = []
	for i in range(nodes):
		hosts.append('r{0}'.format(i))
	return hosts

def restart_node(host):
	print('Restarting node')
	output = commands.getoutput('ssh {0} "sudo init 6"'.format(host))
	print(output)
=======
import random

# Globals
#-------------------------------------------------------------------------------- <-80
_DRIVER = 'DUMMY_DRIVER'

# Classes
#-------------------------------------------------------------------------------- <-80
class DummyCollector(object):
    """
    NAME:               UtrasonicSensor
    DESCRIPTION:
                        It is important to cut power to the sensor when not reading 
                        from it. The configure method has power controls built in to 
                        ensure a power cycle for any config changes

    .read()                     to receive sensor output for distance to nearest object
    .stop()                     to cut power to the sensor, cleanup GPIO
    """
    def __init__(self):
        super(DummyCollector, self).__init__()
        self.instrument = _DRIVER

    def read(self):
        output = {
            'distance': None
            }
        output['distance'] = random.randint(0, 256)
        return output
        
    def stop(self):
        self.instrument.gpio.cleanup()

# Functions
#-------------------------------------------------------------------------------- <-80
def print_ultrasonic(results):
    print('----------------------------------------')
    print("Instrument Read:")
    print("Distance : {0} CM".format(
        results['distance']
        )
    )
>>>>>>> a9c8de734127b01ee34838eecf0eab6d19bb5c93:data_collector/interfaces/interface_dummy.py

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
<<<<<<< HEAD:BOUNCE_CLUSTER.py
	if args.server:
		host = args.server
		print('HOST: {0}'.format(host))
		try:
			restart_node(host)
		except Exception, e:
			print(e)
	else:
		for host in gen_node_hosts(NODES):
			print('HOST: {0}'.format(host))
			try:
				restart_node(host)
			except Exception, e:
				print(e)
=======
    dummyCollector = DummyCollector()
    results = dummyCollector.read()
    print_ultrasonic(results)
>>>>>>> a9c8de734127b01ee34838eecf0eab6d19bb5c93:data_collector/interfaces/interface_dummy.py
