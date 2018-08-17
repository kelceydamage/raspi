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
cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast32_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdio cimport sprintf
from libc.stdlib cimport atoi
from posix cimport time as p_time
import base64
import ujson

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
cdef class Frame:
    """
NAME:
DESCRIPTION:
    """
    def __cinit__(Frame self, uint_fast32_t pack):
        self.pack = pack

    cdef string encode(Frame self, string s):
        return base64.b64encode(s)

    cdef string decode(Frame self, string s):
        return base64.b64decode(s)

    cdef vector[string] encode_l(Frame self, list _list, bint encoded=False):
        cdef vector[string] v
        cdef unsigned long i
        cdef unsigned long l = len(_list)
        cdef string s
        for i in range(0, l):
            if encoded:
                s = _list[i].encode()
            else:
                s = self.encode(ujson.dumps(_list[i]).encode())
            v.push_back(s)
        return v

    cdef list decode_l(Frame self, vector[string] v, bint encoded=False):
        cdef list _list = []
        cdef unsigned long i
        cdef unsigned long l = v.size()
        cdef str s
        for i in range(0, l):
            _list.append(ujson.loads(self.decode(v[i])))
        return _list

    cdef dict decode_d(Frame self, map[string, string] m):
        cdef dict _dict = {}
        cdef pair[string, string] p
        for p in m:
            _dict[p.first.decode()] = p.second.decode()
        return _dict

    cdef map[string, string] encode_d(Frame self, dict _dict):
        cdef map[string, string] _map
        cdef pair[string , string] p
        cdef string _k
        cdef string _v
        for k in _dict:
            _k = k.encode()
            if isinstance(_dict[k], bytes):
                _v = _dict[k]
            else:
                _v = _dict[k].encode()
            p.first = _k
            p.second = _v
            _map.insert(p)
        return _map

    cdef string _serialize(Frame self, object obj):
        return (ujson.dumps(obj)).encode()
        
    cpdef string serialize(Frame self):
        """
NAME:           serialize
DESCRIPTION:    Convert self.message into a json object
        """
        return self._serialize(self.get_message())

    cpdef object deserialize(Frame self, string message):
        """
NAME:           serialize
DESCRIPTION:    Convert self.message into a json object
        """
        #return eval(message.decode(), {"__builtins__":None}, {})
        return ujson.loads(message.decode())

    cpdef void load(Frame self, dict message):
        #self.message = message
        self.gen_message(message)

    cpdef void _pack_frame(Frame self, dict kwargs):
        """
NAME:           pack_frames
DESCRIPTION:    Helper to setup an arbitrary frame
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    cpdef void digest(Frame self):
        self.hash = hashlib.md5(''.join(sorted(self.get_message())).encode()).hexdigest().encode()

cdef class MetaFrame(Frame):
    """
NAME:           MetaFrame
DESCRIPTION:    Frame object for metadata
    """
    def __cinit__(MetaFrame self, uint_fast32_t pack):
        super(MetaFrame, self).__init__(pack)
        self._message = <MetaMessage*>&M_MESSAGE
        self._message.part = <uint_fast16_t>0
        self.digest()

    cpdef MetaMessage get_message(MetaFrame self):
        # return message safely convertable to a python dict
        return <MetaMessage>self._message[0]

    cpdef void set_pack(MetaFrame self, string pack):
        self._message.pack = pack

    cpdef string get_pack(MetaFrame self):
        return self._message.pack

    cpdef void set_error(MetaFrame self, string error):
        self._message.error = error

    cpdef string get_error(MetaFrame self):
        return self._message.error

    cpdef void set_id(MetaFrame self, string id):
        self._message.id = id

    cpdef string get_id(MetaFrame self):
        return self._message.id

    cpdef void set_role(MetaFrame self, string role):
        self._message.role = role

    cpdef string get_role(MetaFrame self):
        return self._message.role

    cpdef void set_version(MetaFrame self, string version):
        self._message.version = version

    cpdef string get_version(MetaFrame self):
        return self._message.version

    cpdef void set_type(MetaFrame self, string _type):
        self._message.type = _type

    cpdef string get_type(MetaFrame self):
        return self._message.type

    cpdef void set_serial(MetaFrame self, string serial):
        self._message.serial = serial

    cpdef string get_serial(MetaFrame self):
        return self._message.serial

    cpdef void set_part(MetaFrame self, uint_fast16_t part):
        self._message.part = part
    
    cpdef uint_fast16_t get_part(MetaFrame self):
        return self._message.part

    cpdef void set_length(MetaFrame self, uint_fast16_t length):
        self._message.length = length

    cpdef uint_fast16_t get_length(MetaFrame self):
        return self._message.length

    cpdef void set_size(MetaFrame self, uint_fast16_t size):
        self._message.size = size

    cpdef uint_fast16_t get_size(MetaFrame self):
        return self._message.size

    cpdef void gen_message(MetaFrame self, dict params):
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
            self._message.id = <string>params['id'].encode()
            self._message.role = <string>params['role'].encode()
            self._message.version = <string>params['version'].encode()
            self._message.type = <string>params['type'].encode()
            self._message.pack = <string>params['pack'].encode()
            self._message.serial = <string>params['serial'].encode()
            self._message.part = <uint_fast16_t>params['part']
            self._message.length = <uint_fast16_t>params['length']
        except Exception as e:
            print(str(e))
            self._message.error = b'Missing key parameter'

cdef class DataFrame(Frame):
    """
NAME:           DataFrame
DESCRIPTION:    Frame object for data
    """
    def __cinit__(DataFrame self, uint_fast32_t pack):
        super(DataFrame, self).__init__(pack)
        self._message = <DataMessage*>&D_MESSAGE
        self.digest()

    cpdef DataMessage get_message(DataFrame self):
        # return message safely convertable to a python dict
        return <DataMessage>self._message[0]

    cpdef void set_pack(DataFrame self, string pack):
        self._message.pack = pack

    cpdef string get_pack(DataFrame self):
        return self._message.pack

    cpdef void set_error(DataFrame self, string error):
        self._message.error = error

    cpdef string get_error(DataFrame self):
        return self._message.error

    cpdef void set_size(DataFrame self, uint_fast16_t size):
        self._message.size = size

    cpdef uint_fast16_t get_size(DataFrame self):
        return self._message.size

    cpdef void set_data(DataFrame self, list data, bint encoded=False):
        self._message.data = self.encode_l(data, encoded)

    cpdef list get_data(DataFrame self, bint encoded=False):
        return self.decode_l(self._message.data, encoded)

    cpdef void gen_message(DataFrame self, dict params):
        """
NAME:           gen_message
DESCRIPTION:    Converts object into a serializable dict
REQUIRES:       self.data [Data payload]
                self.pack [Package ID]
        """
        try:
            self._message.pack = <string>params['pack'].encode()
            self._message.data = <vector[string]>self.encode_l(params['data'], encoded=True)
            self._message.size = <uint_fast16_t>params['size']
        except Exception as e:
            print(str(e))
            self._message.error = b'Missing key parameter'

cdef class TaskFrame(Frame):
    """
NAME:           TaskFrame
DESCRIPTION:    Frame object for tasks
    """
    def __cinit__(TaskFrame self, uint_fast32_t pack):
        super(TaskFrame, self).__init__(pack)
        self._message = <TaskMessage*>&T_MESSAGE
        self.digest() 

    cpdef TaskMessage get_message(TaskFrame self):
        # return message safely convertable to a python dict
        return <TaskMessage>self._message[0]

    cpdef void set_pack(TaskFrame self, string pack):
        self._message.pack = pack

    cpdef string get_pack(TaskFrame self):
        return self._message.pack

    cpdef void set_error(TaskFrame self, string error):
        self._message.error = error

    cpdef string get_error(TaskFrame self):
        return self._message.error

    cpdef void set_task(TaskFrame self, string task):
        self._message.task = task

    cpdef string get_task(TaskFrame self):
        return self._message.task

    cpdef void set_args(TaskFrame self, vector[string] args):
        self._message.args = args

    cpdef vector[string] get_args(TaskFrame self):
        return self._message.args

    cpdef void set_kwargs(TaskFrame self, dict kwargs):
        self._message.kwargs = self.encode(ujson.dumps(kwargs).encode())

    cpdef dict get_kwargs(TaskFrame self):
        return ujson.loads(self.decode(self._message.kwargs).decode())

    cpdef void set_nargs(TaskFrame self, vector[double] nargs):
        self._message.nargs = nargs

    cpdef vector[double] get_nargs(TaskFrame self):
        return self._message.nargs

    cpdef void gen_message(TaskFrame self, dict params):
        """
NAME:           gen_message
DESCRIPTION:    Converts object into a serializable dict
REQUIRES:       self.task [Name of task to run]
                self.args [Standard args (list)]
                self.kwargs [Standard kwargs (dict)]
                self.pack [Package ID]
        """
        try:
            self._message.task = <string>params['task'].encode()
            self._message.args = <vector[string]>params['args']
            self._message.nargs = <vector[double]>params['nargs']
            self._message.kwargs = <string>params['kwargs'].encode()
            self._message.pack = <string>params['pack'].encode()
        except Exception as e:
            self._message.error = b'Missing key parameter'

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
