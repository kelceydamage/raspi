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
CONFIG_HOME = 'server_configs'

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def gen_node_hosts(nodes):
	hosts = []
	for i in range(nodes):
		hosts.append('r{0}'.format(i))
	return hosts

def copy_configs(host):
	print('Copying configs')
	output = commands.getoutput('scp -r {0}/{1}/etc {1}:/tmp/'.format(CONFIG_HOME, host))
	print(output)

def copy_keys(host):
	print('Copying keys')
	output = commands.getoutput('scp -r {0}/{1}/ssh/* {1}:~/.ssh/'.format(CONFIG_HOME, host))
	print(output)

def install_configs(host):
	print('Installing configs')
	output = commands.getoutput('ssh {0} "sudo cp -R /tmp/etc/* /etc/"'.format(host))
	print(output)

def install_keys(host):
	print('Installing keys')
	output = commands.getoutput('ssh {0} "sudo chmod 600 ~/.ssh/id_rsa"'.format(host))
	print(output)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	for host in gen_node_hosts(NODES):
		print('HOST: {0}'.format(host))
		copy_configs(host)
		copy_keys(host)
		install_configs(host)
		install_keys(host)