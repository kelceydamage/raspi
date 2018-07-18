from libcpp cimport bool
from libcpp.queue cimport queue
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

cdef class MotorDrive:
    def __cinit__(MotorDrive self):
        #self.bot = None
        self.switch = False
        self.duration = 0
        self.accel_interval = 1
        #self.timer = Timer()
        #self.client = TaskClient('control_movement')

    cdef int accelerate(MotorDrive self, int initial, int speed, bool positive):
        cdef int i
        cdef queue[int] v

    cdef queue[int] _gen_acelerator(MotorDrive self, int initial, int speed, bool positive):
        cdef int i
        cdef int stepping
        cdef int start
        cdef int end
        cdef queue[int] v
       
        if positive:
            stepping = self.accel_interval
            start = initial
            end = speed
        else:
            stepping = self.accel_interval * -1
            start = speed
            end = initial
        i = start
        while i != end:
           v.push(i)
           i += stepping

        return v

    cdef pair[int, int] polarity(MotorDrive self, int left_motor, int right_motor):
        cdef pair[int, int] p
        if self.switch == True:
            p.first = left_motor
            p.second = right_motor
        else:
            p.first = right_motor
            p.second = left_motor
        return p

    @cython.cdivision(True) 
    cdef void move(MotorDrive self, int speed, int initial=0, int direction=0, bool acceleration=False, bool positive=True, double gearing=1.0):
        cdef int i
        cdef int err
        cdef double rt
        cdef p_time.timespec t

        if direction == STOP:
            direction = self.last_direction
            if self.accel_interval == 0:
                self.accel_interval = 1
            self.duration = self.last_speed / self.accel_interval
        if acceleration == True:
            self.acelerator = self._gen_acelerator(initial, speed, positive)
        i = 0
        while i <= self.duration:
            self.timer.start()
            if acceleration == True:
                if not self.acelerator.empty():
                    speed = self.acelerator.front()
                    self.acelerator.pop()
                else:
                    acceleration = False
            
            velocity = self.movement_type(direction, speed, gearing)

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

            self.timer.end()
            rt = RESPONSE_TIME - self.timer._result
            if rt > 0: 
                err = p_time.nanosleep(&t, NULL)
                if err == -1:
                    printf("CRITICAL: Response Time interupted")

    cdef void update(self, vector[int] args):
        speed           = args[0]
        initial         = args[1]
        direction       = args[2]
        acceleration    = args[3]
        deceleration    = args[4]
        gearing         = args[5]
        self.move(speed, initial, direction, acceleration, deceleration, gearing)

    cdef pair[int, int] movement_type(MotorDrive self, int direction, int speed, float gearing):
        cdef pair[int, int] p
        p.first = 0
        p.second = 0
        return p

cdef class ContinuousTrackedMovement(MotorDrive):

    @cython.cdivision(True) 
    cdef double graduated_turn(ContinuousTrackedMovement self, double fraction, int stepping, int direction):
        if stepping == 0:
            return 0
        if direction == OUTWARDS:
            return fraction / stepping
        elif direction == INWARDS:
            return fraction * stepping

    cdef pair[int, int] movement_type(ContinuousTrackedMovement self, int direction, int speed, float gearing):
        cdef pair[int, int] p
        if direction == REVERSE_LEFT_BIAS:
            return self.polarity(speed * -1, <int>((speed * gearing)))
        elif direction == REVERSE_RIGHT_BIAS:
            return self.polarity(<int>((speed * gearing)) * -1, speed)
        elif direction == FORWARD_LEFT_BIAS:
            return self.polarity(speed, <int>((speed * gearing)) * -1)
        elif direction == FORWARD_RIGHT_BIAS:
            return self.polarity(<int>((speed * gearing)), speed * -1)
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