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
cdef public uint_fast8_t FORWARD
cdef public uint_fast8_t REVERSE
cdef public uint_fast8_t LEFT
cdef public uint_fast8_t RIGHT
cdef public uint_fast8_t STOP
cdef public uint_fast8_t REVERSE_LEFT_BIAS
cdef public uint_fast8_t REVERSE_RIGHT_BIAS
cdef public uint_fast8_t FORWARD_LEFT_BIAS
cdef public uint_fast8_t FORWARD_RIGHT_BIAS
cdef public uint_fast8_t INWARDS
cdef public uint_fast8_t OUTWARDS

#cdef object MOTOR_FAILURE
cdef public bint TRACKED
cdef public double RESPONSE_TIME

# Motor ports. Default settings are for MegaPi
cdef public int LEFT_MOTOR
cdef public int RIGHT_MOTOR

cdef movementObject O_MOVEMENT

# Classes
#---------------------------------------------------------------------------------------------------- <-100
# Python wrapper if the class needs to be called from Python. Wraps C++ class, mainly used for unit tests.
cdef class PyWrap_MotorDrive:

    cdef MotorDrive DRIVER

    cpdef void register_movement(PyWrap_MotorDrive self, pair[int_fast16_t, int_fast16_t] velocity)
    cpdef cpplist[uint_fast8_t] accelerate(PyWrap_MotorDrive self, uint_fast8_t initial, uint_fast8_t speed, bint positive)
    cpdef void configure(PyWrap_MotorDrive self)
    cpdef pair[int_fast16_t, int_fast16_t] polarity(PyWrap_MotorDrive self, int_fast16_t l, int_fast16_t r)
    cpdef pair[int_fast16_t, int_fast16_t] move(PyWrap_MotorDrive self, uint_fast8_t speed, uint_fast8_t initial, uint_fast8_t direction, bint acceleration, bint positive, float gearing, bint test)
    cpdef pair[int_fast16_t, int_fast16_t] update(PyWrap_MotorDrive self, list args)
    cpdef float graduated_turn(PyWrap_MotorDrive self, float fraction, uint_fast8_t stepping, uint_fast8_t direction)
    cpdef pair[int_fast16_t, int_fast16_t] movement_type(PyWrap_MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing)

cdef class MotorDrive:

    cdef uint_fast8_t last_direction
    cdef uint_fast8_t last_speed
    cdef public uint_fast8_t accel_interval
    cdef public int duration
    cdef public bint polarity_bool
    cdef Timer timer
    cdef cpplist[uint_fast8_t] accelerator

    cdef cpplist[uint_fast8_t] _gen_accelerator(MotorDrive self, int a, int b, bint c)

    cdef void _configure(MotorDrive self)
    cdef void _register_movement(MotorDrive self, pair[int_fast16_t, int_fast16_t] velocity)
    cdef pair[int_fast16_t, int_fast16_t] _movement_type(MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing)
    cdef pair[int_fast16_t, int_fast16_t] _update(self, movementObject o_move)
    cdef pair[int_fast16_t, int_fast16_t] _polarity(self, int_fast16_t left_motor, int_fast16_t right_motor)
    cdef pair[int_fast16_t, int_fast16_t] _move(MotorDrive self, uint_fast8_t speed, uint_fast8_t initial, uint_fast8_t direction, bint acceleration, bint positive, float gearing, bint test)
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