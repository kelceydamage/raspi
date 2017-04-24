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
This interface is for movement.

Controls for movement expecct that distance and speed are used to calculate duration
which then needs to be set with Movement().duration.

Movement response time is 500ms so set Movement().accel_interval to a value that
will allow you to reach your distance and adjust Movement().duration accordingly.

.stop() is called explicitly in the movement infterfaces. This is done to avoid damage 
to certain motor types. This means that when chaining interfaces to create complex 
movement patterns there will be a RESPONSE_TIME pause between interfaces.

Added support for accel and deccel on turns.

Still needs to call a task client. Currently it is calling the driver directly in the 
.register_movement() method. In the final version it will call the Task Engine and the 
task nodes will talk to the drivers.

"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import time

# Globals
#-------------------------------------------------------------------------------- <-80
# Numerical identifiers for basic movement patterns
FORWARD             = 0
REVERSE             = 1
LEFT                = 2
RIGHT               = 3
STOP                = 4
REVLEFT             = 5
REVRIGHT            = 6

INWARDS             = 7
OUTWARDS            = 8

MOTOR_FAILURE       = NotImplementedError

TRACKED             = True
RESPONSE_TIME       = 0.5 # 500ms

# Motor ports. Default settings are for MegaPi
LEFT_MOTOR          = 1
RIGHT_MOTOR         = 2

# Classes
#-------------------------------------------------------------------------------- <-80
class Movement(object):
    """
    NAME:               Movement
    DESCRIPTION:    
                        General movement class for controlling the motor drivers

    .bot                        the driver class for your motors. This needs to be set 
                                before this class will do anything. I've written this 
                                expecting a MegaPi() class object, but the code can be
                                easily modified to support other drivers
    .switch             bool    enable to reverse polarity
    .duration           int     how long the movement call will take:
                                    [RESPONSE_TIME * self.duration = seconds]
    .accel_interval     int     the incremements to speed when acceleration is enabled
    .polarity()                 easy method to reverse motor polarity in the event you 
                                robot drives inverted
        left_motor      int     speed value for left motor channel
        right_motor     int     speed value for right motor channel
    .accelerate()               generator for producing the acceleration speed increments
        initial         int     the initial speed the motor will start acceleration from
        speed           int     the final requested cruising speed
    .deccelerate()            generator for producing the decceleration speed increments
        initial         int     the final requested cruising speed
        speed           int     the initial speed the motor will start acceleration from
    .movement_type()            provided by sub-classes and determins movement patterns
        direction       int     specifies which polarity configuration and modifiers are 
                                used on the motor speed
        speed           int     the final requested cruising speed
    .move()                     invokes the drivers move command    
        speed           int     the requested cruising speed
        initial         int     the initial speed the motor will start acceleration from
        direction       int     specifies which polarity configuration and modifiers are 
                                used on the motor speed
        acceleration    bool    enable acceleration
        decceleration   bool    enable decceleration
    .register_movement()        inteface for sending movemeent command to driver/task 
                                engine
        velocity        tuple   left motor and right motor power values

    INTERFACES:
                        The following are default interfaces and have the same required
                        parameters:

        speed           int     the requested cruising speed
        acceleration    bool    enable acceleration
        initial         int     the initial speed the motor will start acceleration from

    .forward()                  provided default movement interface
    .reverse()                  provided default movement interface
    .turn_left()                provided default movement interface
    .turn_right()               provided default movement interface
    .update()                   provided default continuous movement interface
    .stop()                     provided default movement interface
    .graduated_stop()           provided default movement interface

    """
    def __init__(self):
        super(Movement, self).__init__()
        self.bot = None
        self.switch = False
        self.duration = 0
        self.accel_interval = 1

    def polarity(self, left_motor, right_motor):
        if self.switch == True:
            return [left_motor, right_motor]
        else:
            return [right_motor, left_motor]

    def accelerate(self, initial, speed):
        for i in range(initial, speed, self.accel_interval):
            yield i

    def deccelerate(self, initial, speed):
        for i in range(speed, initial, self.accel_interval * -1):
            yield i

    def movement_type(self, direction, speed):
        return (0, 0)

    def move(self, speed, initial=None, direction=None, acceleration=False, decceleration=False, gearing=1):
        if direction == STOP:
            direction = self.last_direction
            self.duration = self.last_speed / self.accel_interval
        if acceleration == True:
            if initial == None:
                initial = self.last_speed
            speed_up_generator = self.accelerate(initial, speed)
        elif decceleration == True:
            if speed == None:
                speed = self.last_speed
            speed_down_generator = self.deccelerate(initial, speed)
        i = 0
        while i <= self.duration:
            start_time = time.time()
            if acceleration == True:
                try:
                    speed = next(speed_up_generator)
                except StopIteration:
                    acceleration = False
            elif decceleration == True:
                try:
                    speed = next(speed_down_generator)
                except StopIteration:
                    decceleration = False
            velocity = self.movement_type(direction, speed, gearing)
            try:
                self.register_movement(velocity)
            except Exception, e:
                print(MOTOR_FAILURE)
                print(velocity)
            self.last_speed = speed
            if direction != None:
                self.last_direction = direction
            i += 1
            end_time = time.time() - start_time
            time.sleep(RESPONSE_TIME - end_time)

    def register_movement(self, velocity):
        self.bot.motorRun(LEFT_MOTOR, velocity[0])
        self.bot.motorRun(RIGHT_MOTOR, velocity[1])

    def forward(self, speed, acceleration=False, decceleration=False, initial=None):
        self.move(speed, initial, FORWARD, acceleration, decceleration)
        if acceleration or decceleration:
            self.graduated_stop()
        else:
            self.stop()

    def reverse(self, speed, acceleration=False, decceleration=False, initial=None):
        self.move(speed, initial, REVERSE, acceleration, decceleration)
        if acceleration or decceleration:
            self.graduated_stop()
        else:
            self.stop()

    def turn_left(self, speed, acceleration=False, decceleration=False, initial=None):
        self.move(speed, initial, LEFT, acceleration, decceleration)
        if acceleration or decceleration:
            self.graduated_stop()
        else:
            self.stop()

    def turn_right(self, speed, acceleration=False, decceleration=False, initial=None):
        self.move(speed, initial, RIGHT, acceleration, decceleration)
        if acceleration == True or decceleration == True:
            self.graduated_stop()
        else:
            self.stop()

    def update(self, args):
        speed           = args[0]
        initial         = args[1]
        direction       = args[2]
        acceleration    = args[3]
        decceleration   = args[4]
        gearing         = args[5]
        self.duration   = 0
        self.move(speed, initial, direction, acceleration, decceleration, gearing)

    def stop(self):
        self.duration = 0
        self.move(0)

    def graduated_stop(self):
        self.move(None, direction=STOP, initial=0, decceleration=True)
        self.stop()

class TrackedMovement(Movement):
    """
    NAME:               TrackedMovement
    DESCRIPTION:    
                        High-level interface for tracked movement. Designed to minimize 
                        track slipage by reducing turning thresholds. Implements 
                        .movement_type() required default interfaces. Custom interfaces 
                        can be added that describe complex meovement parts, and 
                        .movement_type() can be extended to support those insterfaces

    .movement_type()            speed and polarity modifiers for moters based on 
                                definened movement types
        direction       int     specifies which polarity configuration and modifiers are 
                                used on the motor speed
        speed           int     the requested cruising speed
    """
    def __init__(self):
        super(TrackedMovement, self).__init__()

    def movement_type(self, direction, speed, gearing):
        if direction == FORWARD:
            return self.polarity(speed, speed * -1)
        elif direction == REVERSE:
            return self.polarity(speed * -1, speed)
        elif direction == LEFT:
            return self.polarity(speed, speed / 5)
        elif direction == RIGHT:
            return self.polarity(speed / 5, speed)
        else:
            return (0, 0)

class ContinuousTrackedMovement(Movement):
    """
    NAME:               ContinuousTrackedMovement
    DESCRIPTION:        
                        Supplies the only four modes required for continuous movement
                        LEFT, RIGHT, REVLEFT, REVRIGHT. This means only one of four
                        possible biases is required to move in 2 dimentional space. 
                        the gearing value in fractions can be used to modify the
                        trajectory into a turn. With a gearing of 1 the two motors
                        will receive the same drive power. This enables minor course 
                        corrections if veerage occurs, and can rapidly update course
                        based on sensor data. also .stop()/.graduated_stop() now act
                        as idlers.

    .graduated_turn() 
    .movement_type()            speed and polarity modifiers for moters based on 
                                definened movement types
        direction       int     specifies which polarity configuration and modifiers are 
                                used on the motor speed
        speed           int     the requested cruising speed
        gearing         frac    the ratio used to steer the motors expressed as a fraction
                                of floats. [1.0/2.0, 1.0/4.0, 7.0/32.0, ...]
    """
    def __init__(self):
        super(ContinuousTrackedMovement, self).__init__()

    def graduated_turn(self, fraction, stepping, direction):
        if direction == OUTWARDS:
            return fraction / stepping
        elif direction == INWARDS:
            return fraction * stepping

    def movement_type(self, direction, speed, gearing):
        if direction == REVLEFT:
            return self.polarity(speed * -1, int((speed * gearing)))
        elif direction == REVRIGHT:
            return self.polarity(int((speed * gearing)) * -1, speed)
        elif direction == LEFT:
            return self.polarity(speed, int((speed * gearing)) * -1)
        elif direction == RIGHT:
            return self.polarity(int((speed * gearing)), speed * -1)
        else:
            return (0, 0)

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
# Example on how to use
if __name__ == '__main__':
    M = ContinuousTrackedMovement()
    # M.bot = SomeBot()
    # Set the speed increments for accelerating
    M.accel_interval = 1
    # Set the duration for the movement window

    '''
    # Basic movement interface.
    M.duration = 5
    M.forward(
        speed=50, 
        acceleration=True, 
        initial=10
        )
    M.duration = 5
    M.reverse(
        speed=50, 
        decceleration=True, 
        initial=10
        )
    M.duration = 5
    M.turn_left(
        speed=50, 
        acceleration=True, 
        initial=10
        )
    '''

    # Continuous movement interface. Note the explicit call of .stop() to terminate voltage
    # to te engine.
    gearing = 1.0/32.0
    while gearing < 1.0/2.0:
        gearing = M.graduated_turn(gearing, 2, INWARDS)
        M.update(
            [20, 0, LEFT, False, False, gearing]
            )

    gearing = 1.0/1.0
    while gearing > 1.0/32.0:
        gearing = M.graduated_turn(gearing, 2, OUTWARDS)
        M.update(
            [20, 0, LEFT, False, False, gearing]
            )
    time.sleep(3)
    M.stop()
