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
import commands
import argparse
import textwrap

# Globals
#-------------------------------------------------------------------------------- <-80
PROGRAM_NAME = 'CLUSTER_TOOL.py'
DESCRIPTION = 'this is a test'
USAGE = 'CLUSTER_TOOL.py {1,2} [-r REMOTE_HOST] [-p REMOTE_PATH] [-h]'
CONFIG_HOME = 'server_configs'

# Parser
#-------------------------------------------------------------------------------- <-80
parser = argparse.ArgumentParser(
	prog=PROGRAM_NAME,
	usage=USAGE,
	formatter_class=argparse.RawTextHelpFormatter,
	description=textwrap.dedent(DESCRIPTION)
	)
functions = parser.add_argument_group('functions')
help = '''
[1] Copy code repository to a remote host.
[2] Copy configuration files over to new hosts.
[3] Ping host for health check.
[4] Restart a remote host.
'''
functions.add_argument(
	choices=['1', '2', '3', '4'],
	action="store",
	dest="command",
	help=textwrap.dedent(help)
	)
parameters = parser.add_argument_group('parameters')
help = 'The remote hosts you with to interact with'
parameters.add_argument(
	"-r", 
	nargs='+',
	action="store", 
	dest="remote_hosts", 
	required=True,
	help=textwrap.dedent(help)
	)
help = 'The remote path you with to interact with'
parameters.add_argument(
	"-p", 
	action="store", 
	dest="remote_path", 
	help=textwrap.dedent(help)
	)
optional = parser.add_argument_group('optional')
help = 'Usage RSYNC for deployment operations'
optional.add_argument(
	"-s", 
	"--sync",
	action="store_true", 
	dest="sync", 
	default=False,
	help=textwrap.dedent(help)
	)
help = 'Usage SUDO for remote execution operations'
optional.add_argument(
	"-k", 
	"--sudo",
	action="store_true", 
	dest="sudo", 
	default=False,
	help=textwrap.dedent(help)
	)
args = parser.parse_args()

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def task_header(header):
	message = '''
------------------------------------------------------
{0}
------------------------------------------------------
	'''.format(header)
	print(message)

def iterate(func):
	for host in args.remote_hosts:
		return func(host)

def function_wrapper(option, host, command_if_true=None, command_if_false=None, header=None):
	if option == True:
		command = command_if_true
	else:
		command = command_if_false
	task_header(header)
	print('Executing command: {0}'.format(command))
	try:
		output = commands.getoutput(command)
	except Exception, e:
		output = str(e)
	print(output)

def copy_repo(host):
	function_wrapper(
		option=args.sync,
		host=host,
		command_if_true='rsync -avz * {0}:{1}'.format(host, args.remote_path),
		command_if_false='scp -r * {0}:{1}'.format(host, args.remote_path),
		header='Copying repo: HOST={0} SYNC={1}'.format(host, args.sync)
		)

def copy_configuration(host):
	function_wrapper(
		option=args.sync,
		host=host,
		command_if_true='rsync -avz {0}/{1}/etc {1}:/tmp/'.format(CONFIG_HOME, host),
		command_if_false='scp -r {0}/{1}/etc {1}:/tmp/'.format(CONFIG_HOME, host),
		header='Copying configs: HOST={0} SYNC={1}'.format(host, args.sync)
		)
	function_wrapper(
		option=args.sync,
		host=host,
		command_if_true='rsync -avz {0}/{1}/ssh/* {1}:~/.ssh/'.format(CONFIG_HOME, host),
		command_if_false='scp -r {0}/{1}/ssh/* {1}:~/.ssh/'.format(CONFIG_HOME, host),
		header='Copying keys: HOST={0} SYNC={1}'.format(host, args.sync)
		)
	function_wrapper(
		option=args.sudo,
		host=host,
		command_if_true='ssh {0} "sudo cp -R /tmp/etc/* /etc/"'.format(host),
		command_if_false='ssh {0} "cp -R /tmp/etc/* /etc/"'.format(host),
		header='Installing configs: HOST={0} SUDO={1}'.format(host, args.sudo)
		)
	function_wrapper(
		option=args.sudo,
		host=host,
		command_if_true='ssh {0} "sudo chmod 600 ~/.ssh/id_rsa"'.format(host),
		command_if_false='ssh {0} "hmod 600 ~/.ssh/id_rsa"'.format(host),
		header='Copying configs: HOST={0} SUDO={1}'.format(host, args.sudo)
		)

def health_check(host):
	function_wrapper(
		option=args.sudo,
		host=args.remote_hosts,
		command_if_true='sudo ping -w 4 -W 2 {0}'.format(host),
		command_if_false='ping -w 4 -W 2 {0}'.format(host),
		header='Heartbeat server: HOST={0} SUDO={1}'.format(host, args.sudo)
		)

def restart(host):
	function_wrapper(
		option=args.sudo,
		host=args.remote_hosts,
		command_if_true='ssh {0} "sudo init 6"'.format(host),
		command_if_false='ssh {0} "init 6"'.format(host),
		header='Restarting server: HOST={0} SUDO={1}'.format(host, args.sudo)
		)

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	if int(args.command) == 1:
		iterate(copy_repo)
	elif int(args.command) == 2:
		iterate(copy_configuration)
	elif int(args.command) == 3:
		iterate(health_check)
	elif int(args.command) == 4:
		iterate(restart)
