# License
#---------------------------------------------------------------------------------------------------- <-100
# Author: Kelcey Damage
# Python: 3.5+

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#---------------------------------------------------------------------------------------------------- <-100
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
cimport cython
cimport posix.time as p_time

# Constants
#---------------------------------------------------------------------------------------------------- <-100
# Numerical identifiers for basic movement patterns
cdef int FORWARD
cdef int REVERSE
cdef int LEFT
cdef int RIGHT
cdef int STOP
cdef int REVERSE_LEFT_BIAS
cdef int REVERSE_RIGHT_BIAS
cdef int FORWARD_LEFT_BIAS
cdef int FORWARD_RIGHT_BIAS
cdef int INWARDS
cdef int OUTWARDS

#cdef object MOTOR_FAILURE
cdef bint TRACKED
cdef double RESPONSE_TIME

# Motor ports. Default settings are for MegaPi
cdef int LEFT_MOTOR
cdef int RIGHT_MOTOR

# Classes
#---------------------------------------------------------------------------------------------------- <-100
# Python wrapper if the class needs to be called from Python. Wraps C++ class, mainly used for unit tests.
cdef class PyWrap_MotorDrive:

    cdef MotorDrive DRIVER

    cpdef accelerate(PyWrap_MotorDrive self, int initial, int speed, bint positive)
    cpdef configure(PyWrap_MotorDrive self)
    cpdef polarity(PyWrap_MotorDrive self, int l, int r)
    cpdef move(PyWrap_MotorDrive self, int speed, int initial=?, int direction=?, bint acceleration=?, bint positive=?, double gearing=?, bool test=?)

cdef class MotorDrive:

    cdef int last_direction
    cdef int last_speed
    cdef public cython.int accel_interval
    cdef public int duration
    cdef public bool polarity_bool
    cdef Timer timer
    cdef cpplist[int] acelerator

    cdef void _configure(MotorDrive self)
    cdef pair[int, int] _movement_type(MotorDrive self, int direction, int speed, float gearing)
    cdef void _update(self, vector[int] args)
    cdef cpplist[int] _gen_accelerator(MotorDrive self, int initial, int speed, bint positive)
    cdef pair[int, int] _polarity(self, int left_motor, int right_motor)
    cdef pair[int, int] _move(MotorDrive self, int speed, int initial=?, int direction=?, bint acceleration=?, bint positive=?, double gearing=?, bool test=?)
    cdef double _graduated_turn(MotorDrive self, double fraction, int stepping, int direction)
    cdef pair[int, int] _movement_type(MotorDrive self, int direction, int speed, float gearing)

cdef class Timer:

    cdef public double _start
    cdef public double _end
    cdef public double _result
    cdef public p_time.timeval _p_start
    cdef public p_time.timeval _p_end
    cdef double _to_float(Timer self, int i)
    cdef double _join_time(Timer self, p_time.timeval t)
    cdef void _subtract(Timer self)
    cdef void start(Timer self)
    cdef void end(Timer self)

# Functions
#---------------------------------------------------------------------------------------------------- <-100
cpdef PyWrap_MotorDrive main()