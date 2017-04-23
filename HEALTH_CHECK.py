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
from __future__ import print_function
import os
import commands

# Globals
#-------------------------------------------------------------------------------- <-80
NODES = 8

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def gen_node_hosts(nodes):
	hosts = []
	for i in range(nodes):
		hosts.append('r{0}'.format(i))
	return hosts

def ping_node(host):
	print('Pinging node')
	output = commands.getoutput('sudo ping {0}'.format(host))
	print(output)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	for host in gen_node_hosts(NODES):
		print('HOST: {0}'.format(host))
		ping_node(host)