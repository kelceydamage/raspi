#!python
#cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False
#distutils: define_macros=CYTHON_TRACE_NOGIL=1

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

# Doc
#---------------------------------------------------------------------------------------------------- <-100

# Imports
#---------------------------------------------------------------------------------------------------- <-100
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libc.stdint cimport uint_fast8_t
from libc.stdint cimport int_fast16_t
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libc.stdio cimport printf
cimport cython
cimport posix.time as p_time

# Constants
#---------------------------------------------------------------------------------------------------- <-100
# Numerical identifiers for basic movement patterns
FORWARD             = 0
REVERSE             = 1
LEFT                = 2
RIGHT               = 3
STOP                = 4
REVERSE_LEFT_BIAS   = 5
REVERSE_RIGHT_BIAS  = 6
FORWARD_LEFT_BIAS   = 7
FORWARD_RIGHT_BIAS  = 8

INWARDS             = 9
OUTWARDS            = 10

MOTOR_FAILURE       = NotImplementedError

TRACKED             = True
RESPONSE_TIME       = 0.5 # 500ms

# Motor ports. Default settings are for MegaPi
LEFT_MOTOR          = 1
RIGHT_MOTOR         = 2

O_MOVEMENT.speed           = 0
O_MOVEMENT.initial         = 0
O_MOVEMENT.direction       = 0
O_MOVEMENT.acceleration    = False
O_MOVEMENT.positive        = True
O_MOVEMENT.gearing         = 1.0
O_MOVEMENT.test            = False

# Classes
#---------------------------------------------------------------------------------------------------- <-100
# Python wrapper if the class needs to be called from Python. Wraps C++ class, mainly used for unit tests.
cdef class PyWrap_MotorDrive:

    def __cinit__(PyWrap_MotorDrive self):
        self.DRIVER = MotorDrive()

    def __setattr__(PyWrap_MotorDrive self, str a, object v):
        setattr(self.DRIVER, a, v)

    def __getattr__(PyWrap_MotorDrive self, str a):
        return getattr(self.DRIVER, a)

    cpdef void register_movement(PyWrap_MotorDrive self, pair[int_fast16_t, int_fast16_t] velocity):
        self.DRIVER._register_movement(velocity)

    cpdef void configure(PyWrap_MotorDrive self):
        self.DRIVER._configure()

    cpdef pair[int_fast16_t, int_fast16_t] polarity(PyWrap_MotorDrive self, int_fast16_t l, int_fast16_t r):
        return self.DRIVER._polarity(l, r)

    cpdef cpplist[uint_fast8_t] accelerate(PyWrap_MotorDrive self, uint_fast8_t initial, uint_fast8_t speed, bint positive):
        return self.DRIVER._gen_accelerator(initial, speed, positive)

    cpdef pair[int_fast16_t, int_fast16_t] move(PyWrap_MotorDrive self, uint_fast8_t speed, uint_fast8_t initial, uint_fast8_t direction, bint acceleration, bint positive, float gearing, bint test):
        return self.DRIVER._move(speed, initial, direction, acceleration, positive, gearing, test)

    cpdef pair[int_fast16_t, int_fast16_t] update(PyWrap_MotorDrive self, list args):
        O_MOVEMENT.speed           = args[0]
        O_MOVEMENT.initial         = args[1]
        O_MOVEMENT.direction       = args[2]
        O_MOVEMENT.acceleration    = args[3]
        O_MOVEMENT.positive        = args[4]
        O_MOVEMENT.gearing         = args[5]
        O_MOVEMENT.test            = args[6]
        return self.DRIVER._update(O_MOVEMENT)

    cpdef float graduated_turn(PyWrap_MotorDrive self, float fraction, uint_fast8_t stepping, uint_fast8_t direction):
        return self.DRIVER._graduated_turn(fraction, stepping, direction)

    cpdef pair[int_fast16_t, int_fast16_t] movement_type(PyWrap_MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing):
        return self.DRIVER._movement_type(direction, speed, gearing)

cdef class MotorDrive:

    cdef void _configure(MotorDrive self):
        #self.bot = None
        self.polarity_bool = False
        self.duration = 0
        self.accel_interval = 1
        self.timer = Timer()
        #self.client = TaskClient('control_movement')

    cdef void _register_movement(MotorDrive self, pair[int_fast16_t, int_fast16_t] velocity):
        pass
        #self.client.insert('call_motor', velocity)

    cdef pair[int_fast16_t, int_fast16_t] _polarity(MotorDrive self, int_fast16_t left_motor, int_fast16_t right_motor):
        cdef pair[int_fast16_t, int_fast16_t] p
        if self.polarity_bool == True:
            p.first = left_motor
            p.second = right_motor
        else:
            p.first = right_motor
            p.second = left_motor
        return p

    cdef cpplist[uint_fast8_t] _gen_accelerator(MotorDrive self, int initial, int speed, bint positive):
        cdef uint_fast8_t i
        cdef uint_fast8_t stepping
        cdef uint_fast8_t start
        cdef uint_fast8_t end
        cdef cpplist[uint_fast8_t] l_accel

        if positive:
            stepping = self.accel_interval
            start = initial
            end = speed
        else:
            stepping = self.accel_interval * -1
            start = speed - 1
            end = initial - 1
        i = start
        while i != end:
           l_accel.push_front(i)
           i += stepping

        return l_accel

    @cython.cdivision(True) 
    cdef pair[int_fast16_t, int_fast16_t] _move(MotorDrive self, uint_fast8_t speed, uint_fast8_t initial, uint_fast8_t direction, bint acceleration, bint positive, float gearing, bint test):
        cdef int i
        cdef int err
        cdef double rt
        cdef p_time.timespec t
        cdef pair[int_fast16_t, int_fast16_t] velocity
        cdef double f

        #if self.duration == 0:
            #return ('ERROR', 'no duration set')
        if direction == STOP:
            direction = self.last_direction
            if self.accel_interval == 0:
                self.accel_interval = 1
            self.duration = self.last_speed / self.accel_interval
        
        if acceleration == True:
            self.accelerator = self._gen_accelerator(initial, speed, positive)
        i = 0
        
        while i <= self.duration:
            
            self.timer.start()
            if acceleration == True:
                if not self.accelerator.empty():
                    speed = self.accelerator.back()
                    self.accelerator.pop_back()
                else:
                    acceleration = False
            
            velocity = self._movement_type(direction, speed, gearing)

            try:
                self._register_movement(velocity)
            except Exception:
                print(MOTOR_FAILURE)

            self.last_speed = speed

            if direction != 0:
                self.last_direction = direction

            i += 1

            self.timer.end()
            f = (RESPONSE_TIME - self.timer._result) * 1000000000
            t.tv_nsec = <long>f
            t.tv_sec = 0

            if t.tv_nsec > 0: 
                err = p_time.nanosleep(&t, NULL)
                if err == -1:
                    printf("CRITICAL: Response Time interupted\n")

            if test == True:
                return velocity

    cdef pair[int_fast16_t, int_fast16_t] _update(self, movementObject o_move):
        return self._move(o_move.speed, o_move.initial, o_move.direction, o_move.acceleration, o_move.positive, o_move.gearing, o_move.test)

    @cython.cdivision(True) 
    cdef float _graduated_turn(MotorDrive self, float fraction, uint_fast8_t stepping, uint_fast8_t direction):
        if stepping == 0:
            return 0
        if direction == OUTWARDS:
            return fraction / stepping
        elif direction == INWARDS:
            return fraction * stepping

    cdef pair[int_fast16_t, int_fast16_t] _movement_type(MotorDrive self, uint_fast8_t direction, uint_fast8_t speed, float gearing):
        cdef pair[int_fast16_t, int_fast16_t] p
        if direction == REVERSE_LEFT_BIAS:
            return self._polarity(speed * -1, <int>(speed * gearing))
        elif direction == REVERSE_RIGHT_BIAS:
            return self._polarity(<int>(speed * gearing) * -1, speed)
        elif direction == FORWARD_LEFT_BIAS:
            return self._polarity(speed, <int>(speed * gearing) * -1)
        elif direction == FORWARD_RIGHT_BIAS:
            return self._polarity(<int>(speed * gearing), speed * -1)
        elif direction == FORWARD:
            return self._polarity(<int>(speed * gearing), <int>(speed * gearing))
        elif direction == REVERSE:
            return self._polarity(<int>(-speed * gearing), <int>(-speed * gearing))
        else:
            p.first = 0
            p.second = 0
            return p

cdef class Timer:
    cdef double _to_float(Timer self, int i):
        return <double>i

    @cython.cdivision(True) 
    cdef double _join_time(Timer self, p_time.timeval t):
        return self._to_float(t.tv_sec) + self._to_float(t.tv_usec) / 1000000

    cdef void _subtract(Timer self):
        self._end = self._join_time(self._p_end)
        self._start = self._join_time(self._p_start)
        self._result = self._end - self._start

    cdef void start(Timer self):
        p_time.gettimeofday(&self._p_start, NULL)
        
    cdef void end(Timer self):
        p_time.gettimeofday(&self._p_end, NULL)
        self._subtract()

# Functions
#---------------------------------------------------------------------------------------------------- <-100
cpdef PyWrap_MotorDrive main():
    return PyWrap_MotorDrive()

# Main
#---------------------------------------------------------------------------------------------------- <-100
if __name__ == "__main__": 
    pym = main()