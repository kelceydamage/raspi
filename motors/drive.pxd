from libcpp cimport bool
from libcpp.queue cimport queue
from libcpp.vector cimport vector
from libcpp.utility cimport pair
cimport cython
cimport posix.time as p_time

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
cdef bool TRACKED
cdef double RESPONSE_TIME

# Motor ports. Default settings are for MegaPi
cdef int LEFT_MOTOR
cdef int RIGHT_MOTOR

cdef class MotorDrive:
    cdef int last_direction
    cdef int last_speed
    cdef readonly cython.int accel_interval
    cdef int duration
    cdef bool switch
    cdef Timer timer
    cdef queue[int] acelerator

    cdef pair[int, int] movement_type(MotorDrive self, int direction, int speed, float gearing)

    cdef void update(self, vector[int] args)
    cdef queue[int] _gen_acelerator(MotorDrive self, int initial, int speed, bool positive)
    cdef int accelerate(MotorDrive self, int initial, int speed, bool positive)
    cdef pair[int, int] polarity(self, int left_motor, int right_motor)
    cdef void move(MotorDrive self, int speed, int initial=?, int direction=?, bool acceleration=?, bool positive=?, double gearing=?)
    

cdef class ContinuousTrackedMovement(MotorDrive):
    cdef double graduated_turn(ContinuousTrackedMovement self, double fraction, int stepping, int direction)
    cdef pair[int, int] movement_type(ContinuousTrackedMovement self, int direction, int speed, float gearing)

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