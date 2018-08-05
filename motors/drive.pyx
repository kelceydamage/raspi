#!python
#cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False

from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libc.stdio cimport printf
#from time import sleep
cimport cython
cimport posix.time as p_time

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

#MOTOR_FAILURE       = NotImplementedError

TRACKED             = True
RESPONSE_TIME       = 0.5 # 500ms

# Motor ports. Default settings are for MegaPi
LEFT_MOTOR          = 1
RIGHT_MOTOR         = 2

# Wrappers For python testing

# Python wrapper if the class needs to be called from Python. Wraps C++ class, mainly used for unit tests.
cdef class PyWrap_MotorDrive:

    def __cinit__(PyWrap_MotorDrive self):
        self.DRIVER = MotorDrive()

    def __setattr__(PyWrap_MotorDrive self, str a, object v):
        setattr(self.DRIVER, a, v)

    def __getattr__(PyWrap_MotorDrive self, str a):
        return getattr(self.DRIVER, a)

    cpdef configure(PyWrap_MotorDrive self):
        self.DRIVER._configure()

    cpdef polarity(PyWrap_MotorDrive self, int l, int r):
        return self.DRIVER._polarity(l, r)

    cpdef accelerate(PyWrap_MotorDrive self, int initial, int speed, bint positive):
        return self.DRIVER._gen_accelerator(initial, speed, positive)

    cpdef move(PyWrap_MotorDrive self, int speed, int initial=0, int direction=0, bint acceleration=False, bint positive=True, double gearing=1.0, bool test=False):
        return self.DRIVER._move(speed, initial, direction, acceleration, positive, gearing, test)

cdef class MotorDrive:

    cdef void _configure(MotorDrive self):
        #self.bot = None
        self.polarity_bool = False
        self.duration = 0
        self.accel_interval = 1
        #self.timer = Timer()
        #self.client = TaskClient('control_movement')

    cdef pair[int, int] _polarity(MotorDrive self, int left_motor, int right_motor):
        cdef pair[int, int] p
        if self.polarity_bool == True:
            p.first = left_motor
            p.second = right_motor
        else:
            p.first = right_motor
            p.second = left_motor
        return p

    cdef cpplist[int] _gen_accelerator(MotorDrive self, int initial, int speed, bint positive):
        cdef int i
        cdef int stepping
        cdef int start
        cdef int end
        cdef cpplist[int] v
       
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
           v.push_front(i)
           i += stepping

        return v

    @cython.cdivision(True) 
    cdef pair[int, int] _move(MotorDrive self, int speed, int initial=0, int direction=0, bint acceleration=False, bint positive=True, double gearing=1.0, bool test=False):
        cdef int i
        cdef int err
        cdef double rt
        cdef p_time.timespec t
        cdef pair[int, int] velocity
        cdef cpplist[int] accelerator

        #if self.duration == 0:
            #return ('ERROR', 'no duration set')
        if direction == STOP:
            direction = self.last_direction
            if self.accel_interval == 0:
                self.accel_interval = 1
            self.duration = self.last_speed / self.accel_interval
        
        if acceleration == True:
            accelerator = self._gen_acelerator(initial, speed, positive)
        i = 0
        
        while i <= self.duration:
            
            #self.timer.start()
            if acceleration == True:
                if not accelerator.empty():
                    speed = accelerator.back()
                    accelerator.pop_back()
                else:
                    acceleration = False
            
            velocity = self._movement_type(direction, speed, gearing)

            '''
            try:
                self.register_movement(velocity)
            except Exception, e:
                print(MOTOR_FAILURE)
                print(velocity)
            '''
            self.last_speed = speed

            if direction != 0:
                self.last_direction = direction

            i += 1

            #self.timer.end()
            #rt = RESPONSE_TIME - self.timer._result
            #if rt > 0: 
            #    err = p_time.nanosleep(&t, NULL)
            #    if err == -1:
            #        printf("CRITICAL: Response Time interupted")

            if test == True:
                return velocity

    cdef void _update(MotorDrive self, vector[int] args):
        speed           = args[0]
        initial         = args[1]
        direction       = args[2]
        acceleration    = args[3]
        deceleration    = args[4]
        gearing         = args[5]
        self._move(speed, initial, direction, acceleration, deceleration, gearing)

    @cython.cdivision(True) 
    cdef double _graduated_turn(MotorDrive self, double fraction, int stepping, int direction):
        if stepping == 0:
            return 0
        if direction == OUTWARDS:
            return fraction / stepping
        elif direction == INWARDS:
            return fraction * stepping

    cdef pair[int, int] _movement_type(MotorDrive self, int direction, int speed, float gearing):
        cdef pair[int, int] p
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