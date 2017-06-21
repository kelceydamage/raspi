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

def copy_repo(host):
	print('Copying repo')
	output = commands.getoutput('rsync -avz * {0}:~/projects/research'.format(host))
	print(output)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	if args.server:
		host = args.server
		print('HOST: {0}'.format(host))
		try:
			copy_repo(host)
		except Exception, e:
			print(e)
	else:
		for host in gen_node_hosts(NODES):
			print('HOST: {0}'.format(host))
			try:
				copy_repo(host)
			except Exception, e:
				print(e)

