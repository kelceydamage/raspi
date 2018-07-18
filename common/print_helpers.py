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
import json

# Globals
#-------------------------------------------------------------------------------- <-80

# Parser
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class Colours(object):
	"""docstring for Colours"""
	def __init__(self):
		super(Colours, self).__init__()
		self.RED 			= '\033[38;5;1m'
		self.BLUE 			= '\033[38;5;12m'
		self.GREEN 			= '\033[38;5;10m'
		self.CORAL 			= '\033[38;5;9m'
		self.DARKBLUE		= '\033[38;5;4m'
		self.PURPLE			= '\033[38;5;5m'
		self.CYAN			= '\033[38;5;6m'
		self.LIGHTBLUE		= '\033[38;5;14m'
		self.BRED			= '\033[48;5;1m'
		self.BBLUE			= '\033[48;5;12m'
		self.BGREEN			= '\033[48;5;10m'
		self.BCORAL			= '\033[48;5;9m'
		self.BDARKBLUE		= '\033[48;5;4m'
		self.BPURPLE		= '\033[48;5;5m'
		self.BCYAN	     	= '\033[48;5;6m'
		self.BLIGHTBLUE		= '\033[48;5;14m'
		self.BLACK			= '\033[38;5;0m'
		self.ENDC 			= '\033[m'

# Functions
#-------------------------------------------------------------------------------- <-80
def padding(message, width):
	if len(message) < width:
		message += ' ' * (width - len(message))
	return message

def printc(message, colour):
	endc = '\033[m'
	print('{0}{1}{2}'.format(colour, message, endc))

def print_package(message):
	print('PACK: {0}, SIZE: {1}'.format(message['pack'], message['size']))
	if 'data' in message.keys():
		for item in message['data']:
			if type(list(item.values())[0]) is list:
				print('JOB-ID: {0}, CUDA Response Time: {1}'.format(list(item.keys())[0], list(item.values())[0][0][1]))
			else:
				print('JOB-ID: {0}, Return Values: {1}'.format(list(item.keys())[0], list(item.values())[0]))

def print_nested(message):
	if type(message) is dict:
		print('---------------------------------------------------------------')
		for item in message:
			if type(message[item]) is list:
				print_package(message[item])
			else:
				print('{0}: {1}'.format(item, message[item]))
	elif type(message) is list:
		for item in message:
			print_package(item)
	else:
		print('{0}'.format(message))


# Main
#-------------------------------------------------------------------------------- <-80