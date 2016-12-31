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
import sys
import zmq
from zmq.asyncio import Context, Poller, ZMQEventLoop
import asyncio

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class Router(object):
	"""
NAME: 			Router
DESCRIPTION: 	Routes messages to available workers.
	"""
	def __init__(self):
		super(Router, self).__init__()
		context = Context()
		self.frontend = context.socket(zmq.ROUTER)
		self.backend = context.socket(zmq.DEALER)
		self.poller = Poller()

	def setup_frontend(self, host, port, proto='tcp'):
		"""
NAME: 			setup_frontend
DESCRIPTION: 	Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
		"""
		self.frontend.bind('{2}://{0}:{1}'.format(
            host, 
            port,
            proto
            ))
		self.poller.register(self.frontend, zmq.POLLIN)

	def setup_backend(self, host, port, proto='tcp'):
		"""
NAME:			setup_backend
DESCRIPTION: 	Configure the frontend socket
REQUIRES:       host [ip/hostname]
                port [numeric port]
                proto [protocol: tcp, ipc,...]
		"""
		self.backend.bind('{2}://{0}:{1}'.format(
            host, 
            port,
            proto
            ))
		self.poller.register(self.backend, zmq.POLLIN)

	def run_broker(self):
		"""
NAME:
DESCRIPTION:
		"""
		while True:
			socks = yield from self.poller.poll()
			socks = dict(socks)
			if socks.get(self.frontend) == zmq.POLLIN:
				message = yield from self.frontend.recv_multipart()
				print('received from frontend: {}'.format(message))
	            yield from backend.send_multipart(message)
	        if socks.get(backend) == zmq.POLLIN:
	            message = yield from backend.recv_multipart()
	            print('received from backend: {}'.format(message))
	            yield from frontend.send_multipart(message)

	def start(self):
		"""
NAME:
DESCRIPTION:
		"""
		yield from self.run_broker()


# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	pass