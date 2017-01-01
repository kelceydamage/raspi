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
SUMMARY: Classes to represent various message frame datatypes
"""

# Imports
#-------------------------------------------------------------------------------- <-80
import json

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class Frame(object):
	"""
NAME:
DESCRIPTION:
	"""
	def __init__(self, pack):
		super(Frame, self).__init__()
		self.pack = pack
		
	def serialize(self):
		"""
NAME:			serialize
DESCRIPTION:	Convert self.message into a json object
		"""
		return json.dumps(self.message)

	def pack_frame(self, kwargs):
		"""
NAME:			pack_frame
DESCRIPTION:	Helper to setup a frame
		"""
	for key in kwargs:
		setattr(self, key, kwargs[key])

class MetaFrame(Frame):
	"""
NAME:			MetaFrame
DESCRIPTION:	Frame object for metadata
	"""
	def __init__(self, pack):
		super(MetaReply, self).__init__(pack)

	def gen_message(self):
		"""
NAME:			gen_message
DESCRIPTION:	Converts object into a serializable dict
REQUIRES:		self.id [formatted as '{ROLE}-{PID}'] Example: 'W-3223' 
				self.role [Requestor, Responder, Intermediary, etc...]
				self.version [version number of the conponent]
				self.type [ACK, DATAGRAM, etc...]
				self.pack [Package ID]
		"""
		self.message = {
			'id': self.id,
			'role': self.role
			'version': self.version,
			'type': self.type,
			'pack': self.pack
		}

class DataFrame(Frame):
	"""
NAME:			DataFrame
DESCRIPTION:	Frame object for data
	"""
	def __init__(self, pack):
		super(DataFrame, self).__init__(pack)

	def gen_message(self):
		"""
NAME:			gen_message
DESCRIPTION:	Converts object into a serializable dict
REQUIRES:		self.data [Data payload]
				self.pack [Package ID]
		"""
		self.message = {
			'data': self.data,
			'pack': self.pack
		}	

class TaskFrame(Frame):
	"""
NAME:			TaskFrame
DESCRIPTION:	Frame object for tasks
	"""
	def __init__(self, pack):
		super(DataFrame, self).__init__(pack)

	def gen_message(self):
		"""
NAME:			gen_message
DESCRIPTION:	Converts object into a serializable dict
REQUIRES:		self.task [Name of task to run]
				self.args [Standard args (list)]
				self.kwargs [Standard kwargs (dict)]
				self.pack [Package ID]
		"""
		self.message = {
			'task': self.task,
			'args': self.args,
			'kwargs': self.kwargs,
			'pack': self.pack
		}	

# Functions
#-------------------------------------------------------------------------------- <-80
def prepare(Frame, kwargs):
	"""
NAME:			prepare
DESCRIPTION:	Helper to setup a frame
	"""
	Frame.pack_frame(kwargs)
	Frame.gen_message()
	return Frame.serialize()

# Main
#-------------------------------------------------------------------------------- <-80
