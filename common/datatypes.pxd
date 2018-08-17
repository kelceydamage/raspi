#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: Kelcey Damage
# Cython: 0.28+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Doc
# ------------------------------------------------------------------------ 79->

# Imports
# ------------------------------------------------------------------------ 79->
cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast32_t
from libc.stdint cimport uint_fast16_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdlib cimport atoi
from posix cimport time as p_time

# Globals
# ------------------------------------------------------------------------ 79->
cdef public struct MetaMessage:
    string id
    string role
    string version
    string type
    string pack
    string serial
    uint_fast16_t part
    uint_fast16_t length
    uint_fast16_t size
    string error

cdef struct TaskMessage:
    string task
    vector[string] args
    vector[double] nargs
    string kwargs
    string pack
    string error

cdef struct DataMessage:
    vector[string] data
    #string data
    string pack
    string error
    uint_fast16_t size

cdef MetaMessage M_MESSAGE
cdef TaskMessage T_MESSAGE
cdef DataMessage D_MESSAGE

# Classes
# ------------------------------------------------------------------------ 79->
cdef class Frame:
    cdef public uint_fast32_t pack
    cdef public string message
    cdef public string hash

    cdef string encode(Frame self, string s)
    cdef string decode(Frame self, string s)
    cdef list decode_l(Frame self, vector[string] v, bint encoded=?)
    cdef dict decode_d(Frame self, map[string, string] m)
    cdef map[string, string] encode_d(Frame self, dict _dict)
    cdef string _serialize(Frame self, object _dict)
    cdef vector[string] encode_l(Frame self, list _list, bint encoded=?)

    cpdef void load(Frame self, dict message)
    cpdef string serialize(Frame self)
    cpdef object deserialize(Frame self, string message)
    cpdef void _pack_frame(Frame self, dict kwargs)
    cpdef void digest(Frame self)

cdef class MetaFrame(Frame):
    cdef MetaMessage* _message
    
    # Python safe API. Use this to interact with C++ pointer structs
    cpdef MetaMessage get_message(MetaFrame self)
    cpdef void set_pack(MetaFrame self, string pack)
    cpdef string get_pack(MetaFrame self)
    cpdef void set_error(MetaFrame self, string error)
    cpdef string get_error(MetaFrame self)
    cpdef void set_id(MetaFrame self, string id)
    cpdef string get_id(MetaFrame self)
    cpdef void set_role(MetaFrame self, string role)
    cpdef string get_role(MetaFrame self)
    cpdef void set_version(MetaFrame self, string version)
    cpdef string get_version(MetaFrame self)
    cpdef void set_type(MetaFrame self, string _type)
    cpdef string get_type(MetaFrame self)
    cpdef void set_serial(MetaFrame self, string serial)
    cpdef string get_serial(MetaFrame self)
    cpdef void set_part(MetaFrame self, uint_fast16_t part)
    cpdef uint_fast16_t get_part(MetaFrame self)
    cpdef void set_length(MetaFrame self, uint_fast16_t length)
    cpdef uint_fast16_t get_length(MetaFrame self)
    cpdef void gen_message(MetaFrame self, dict params)
    cpdef void set_size(MetaFrame self, uint_fast16_t size)
    cpdef uint_fast16_t get_size(MetaFrame self)

cdef class DataFrame(Frame):
    cdef DataMessage* _message

    # Python safe API. Use this to interact with C++ pointer structs
    cpdef DataMessage get_message(DataFrame self)
    cpdef void set_pack(DataFrame self, string pack)
    cpdef string get_pack(DataFrame self)
    cpdef void set_error(DataFrame self, string error)
    cpdef string get_error(DataFrame self)
    cpdef void gen_message(DataFrame self, dict params)
    cpdef void set_size(DataFrame self, uint_fast16_t size)
    cpdef uint_fast16_t get_size(DataFrame self)
    cpdef void set_data(DataFrame self, list data, bint encoded=?)
    cpdef list get_data(DataFrame self, bint encoded=?)

cdef class TaskFrame(Frame):
    cdef TaskMessage* _message

    # Python safe API. Use this to interact with C++ pointer structs
    cpdef TaskMessage get_message(TaskFrame self)
    cpdef void set_pack(TaskFrame self, string pack)
    cpdef string get_pack(TaskFrame self)
    cpdef void set_error(TaskFrame self, string error)
    cpdef string get_error(TaskFrame self)
    cpdef void set_task(TaskFrame self, string task)
    cpdef string get_task(TaskFrame self)
    cpdef void set_args(TaskFrame self, vector[string] args)
    cpdef vector[string] get_args(TaskFrame self)
    cpdef void set_kwargs(TaskFrame self, dict kwargs)
    cpdef dict get_kwargs(TaskFrame self)
    cpdef void gen_message(TaskFrame self, dict params)
    cpdef void set_nargs(TaskFrame self, vector[double] nwargs)
    cpdef vector[double] get_nargs(TaskFrame self)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pass
