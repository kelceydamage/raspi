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
import hashlib

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
cdef class Frame:
    """
NAME:
DESCRIPTION:
    """
    def __cinit__(Frame self, int pack):
        self.pack = pack
        
    cpdef serialize(self):
        """
NAME:           serialize
DESCRIPTION:    Convert self.message into a json object
        """
        return json.dumps(self.message).encode()

    cpdef pack_frame(Frame self, dict kwargs):
        """
NAME:           pack_frame
DESCRIPTION:    Helper to setup a frame
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    cpdef digest(Frame self):
        self.hash = hashlib.md5(''.join(sorted(self.message)).encode()).hexdigest()

cdef class MetaFrame(Frame):
    """
NAME:           MetaFrame
DESCRIPTION:    Frame object for metadata
    """
    def __cinit__(MetaFrame self, int pack):
        super(MetaFrame, self).__init__(pack)
        self.message = {
            'id': '',
            'role': '',
            'version': '',
            'type': '',
            'pack': '',
            'serial': '',
            'part': 0,
            'length': ''
        }
        self.digest()

    cpdef gen_message(MetaFrame self):
        """
NAME:           gen_message
DESCRIPTION:    Converts object into a serializable dict
REQUIRES:       self.id [formatted as '{ROLE}-{PID}'] Example: 'W-3223' 
                self.role [Requestor, Responder, Intermediary, etc...]
                self.version [version number of the conponent]
                self.type [ACK, DATAGRAM, etc...]
                self.pack [Package ID]
        """
        try:
            self.message['id'] = self.id
            self.message['role'] = self.role
            self.message['version'] = self.version
            self.message['type'] = self.type
            self.message['pack'] = self.pack
        except Exception as e:
            self.message['error'] = b'Missing key parameter'

cdef class DataFrame(Frame):
    """
NAME:           DataFrame
DESCRIPTION:    Frame object for data
    """
    def __cinit__(DataFrame self, int pack):
        super(DataFrame, self).__init__(pack)
        self.message = {
            'data': '',
            'pack': ''
        }   
        self.digest()

    cpdef gen_message(DataFrame self):
        """
NAME:           gen_message
DESCRIPTION:    Converts object into a serializable dict
REQUIRES:       self.data [Data payload]
                self.pack [Package ID]
        """
        try:
            self.message['data'] = self.data
            self.message['pack'] = self.paack
        except Exception as e:
            self.message['error'] = b'Missing key parameter'

cdef class TaskFrame(Frame):
    """
NAME:           TaskFrame
DESCRIPTION:    Frame object for tasks
    """
    def __cinit__(TaskFrame self, int pack):
        super(TaskFrame, self).__init__(pack)
        self.message = {
            'task': '',
            'args': '',
            'kwargs': '',
            'pack': ''
        }  
        self.digest() 

    cpdef gen_message(TaskFrame self):
        """
NAME:           gen_message
DESCRIPTION:    Converts object into a serializable dict
REQUIRES:       self.task [Name of task to run]
                self.args [Standard args (list)]
                self.kwargs [Standard kwargs (dict)]
                self.pack [Package ID]
        """
        try:
            self.message['task'] = self.task
            self.message['args'] = self.args
            self.message['kwargs'] = self.kwargs
            self.message['pack'] = self.pack 
        except Exception as e:
            self.message['error'] = b'Missing key parameter'

# Functions
#-------------------------------------------------------------------------------- <-80
def prepare(Frame, kwargs):
    """
NAME:           prepare
DESCRIPTION:    Helper to setup a frame
    """
    Frame.pack_frame(kwargs)
    Frame.gen_message()
    return Frame.serialize()

# Main
#-------------------------------------------------------------------------------- <-80
