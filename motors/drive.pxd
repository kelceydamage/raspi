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
from libc.stdint cimport uint_fast8_t
from libc.stdint cimport int_fast16_t
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
cimport cython
cimport posix.time as p_time

# Structs
#---------------------------------------------------------------------------------------------------- <-100
cdef struct movementObject:
    uint_fast8_t speed
    uint_fast8_t initial
    uint_fast8_t direction
    bint acceleration
    bint positive
    float gearing
    bint test

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

cdef movementObject O_MOVEMENT

# Classes
#---------------------------------------------------------------------------------------------------- <-100
# Python wrapper if the class needs to be called from Python. Wraps C++ class, mainly used for unit tests.
cdef class PyWrap_MotorDrive:

    cdef MotorDrive DRIVER

    cpdef accelerate(PyWrap_MotorDrive self, uint_fast8_t initial, uint_fast8_t speed, bint positive)
    cpdef configure(PyWrap_MotorDrive self)
    cpdef polarity(PyWrap_MotorDrive self, int_fast16_t l, int_fast16_t r)
    cpdef move(PyWrap_MotorDrive self, uint_fast8_t speed, uint_fast8_t initial=?, uint_fast8_t direction=?, bint acceleration=?, bint positive=?, float gearing=?, bool test=?)
    cpdef update(PyWrap_MotorDrive self, list args)
    cpdef graduated_turn(PyWrap_MotorDrive self, float fraction, uint_fast8_t stepping, uint_fast8_t direction)
    cpdef movement_type(PyWrap_MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing)

cdef class MotorDrive:

    cdef uint_fast8_t last_direction
    cdef uint_fast8_t last_speed
    cdef public cython.int accel_interval
    cdef public int duration
    cdef public bool polarity_bool
    cdef Timer timer
    cdef cpplist[uint_fast8_t] acelerator

    cdef void _configure(MotorDrive self)
    cdef pair[int_fast16_t, int_fast16_t] _movement_type(MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing)
    cdef pair[int_fast16_t, int_fast16_t] _update(self, movementObject o_move)
    cdef cpplist[uint_fast8_t] _gen_accelerator(MotorDrive self, uint_fast8_t initial, uint_fast8_t speed, bint positive)
    cdef pair[int_fast16_t, int_fast16_t] _polarity(self, int_fast16_t left_motor, int_fast16_t right_motor)
    cdef pair[int_fast16_t, int_fast16_t] _move(MotorDrive self, uint_fast8_t speed, uint_fast8_t initial=?, uint_fast8_t direction=?, bint acceleration=?, bint positive=?, float gearing=?, bool test=?)
    cdef float _graduated_turn(MotorDrive self, float fraction, uint_fast8_t stepping, uint_fast8_t direction)

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