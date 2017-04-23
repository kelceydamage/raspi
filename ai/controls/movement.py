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
This interface is for tracked movement.

Controls for movement expecct that distance and speed are used to calculate duration
which then needs to be set with Movement().duration.

Movement response time is 500ms so set Movement().accel_interval to a value that
will allow you to reach your distance and adjust Movement().duration accordingly.

"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import time

# Globals
#-------------------------------------------------------------------------------- <-80
# Numerical identifiers for basic movement patterns
FORWARD 			= 0
REVERSE 			= 1
LEFT 				= 2
RIGHT 				= 3

MOTOR_FAILURE		= NotImplementedError

TRACKED 			= True
RESPONSE_TIME 		= 0.5 # 500ms

# Classes
#-------------------------------------------------------------------------------- <-80
class Movement(object):
	"""
	NAME:				Movement
	DESCRIPTION:	
						General movement class for controlling the motor drivers

	.bot						the driver class for your motors. This needs to be set 
								before this class will do anything. I've written this 
								expecting a MegaPi() class object, but the code can be
								easily modified to support other drivers
	.switch				bool	enable to reverse polarity
	.duration			int 	how long the movement call will take:
									[RESPONSE_TIME * self.duration = seconds]
	.accel_interval		int 	the incremements to speed when acceleration is enabled
	.polarity()					easy method to reverse motor polarity in the event you 
								robot drives inverted
		left_motor		int 	speed value for left motor channel
		right_motor		int 	speed value for right motor channel
	.accelerate()				generator for producing the aceleration speed increments
		initial			int 	the initial speed the motor will start acceleration from
		speed 			int 	the final requested cruising speed
	.movement_type()			provided by sub-classes and determins movement patterns
		direction 		int 	specifies which polarity configuration and modifiers are 
								used on the motor speed
		speed 			int 	the final requested cruising speed
	.move()						invokes the drivers move command	
		speed 			int 	the requested cruising speed
		initial			int 	the initial speed the motor will start acceleration from
		direction		int 	specifies which polarity configuration and modifiers are 
								used on the motor speed
		acceleration 	bool 	enable acceleration

	INTERFACES:
						The following are default interfaces and have the same required
						parameters:

		speed 			int 	the requested cruising speed
		acceleration 	bool	enable acceleration
		initial 		int 	the initial speed the motor will start acceleration from

	.forward()					provided default movement interface
	.reverse()					provided default movement interface
	.turn_left()				provided default movement interface
	.turn_right()				provided default movement interface
	.stop()						provided default movement interface

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

	def movement_type(self, direction, speed):
		return (0, 0)

	def move(self, speed, initial, direction, acceleration):
		if acceleration == True:
			speed_generator = self.accelerate(initial, speed)
		i = 0
		while i <= self.duration:
			start_time = time.time()
			if acceleration == True:
				try:
					speed = next(speed_generator)
				except StopIteration:
					acceleration = False
			velocity = self.movement_type(direction, speed)
			try:
				self.bot.motorRun(1, velocity[0])
				self.bot.motorRun(2, velocity[1])
			except Exception, e:
				print(MOTOR_FAILURE)
				print(velocity)
			i += 1
			end_time = time.time() - start_time
			time.sleep(RESPONSE_TIME - end_time)

	def forward(self, speed, acceleration=False, initial=None):
		self.move(speed, initial, FORWARD, acceleration)

	def reverse(self, speed, acceleration=False, initial=None):
		self.move(speed, initial, REVERSE, acceleration)

	def turn_left(self, speed, acceleration=False, initial=None):
		self.move(speed, initial, LEFT, acceleration)

	def turn_right(self, speed, acceleration=False, initial=None):
		self.move(speed, initial, RIGHT, acceleration)

	def stop(self):
		self.duration = 0
		self.move(0, 0, None, False)

class TrackedMovement(Movement):
	"""
	NAME: 				TrackedMovement
	DESCRIPTION: 	
						High-level interface for tracked movement. Designed to minimize 
						track slipage by reducing turning thresholds. Implements 
						.movement_type() required default interfaces. Custom interfaces 
						can be added that describe complex meovement parts, and 
						.movement_type() can be extended to support those insterfaces

	.movement_type()			speed and polarity modifiers for moters based on 
								definened movement types
		direction 		int 	specifies which polarity configuration and modifiers are 
								used on the motor speed
		speed 			int 	the requested cruising speed
	"""
	def __init__(self):
		super(TrackedMovement, self).__init__()

	def movement_type(self, direction, speed):
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

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
# Example on how to use
if __name__ == '__main__':
	M = TrackedMovement()
	# M.bot = SomeBot()
	# Set the speed increments for accelerating
	M.accel_interval = 1
	# Set the duration for the movement window
	M.duration = 5

	M.forward(
		speed=50, 
		acceleration=True, 
		initial=10
		)
	M.reverse(
		speed=50, 
		acceleration=True, 
		initial=10
		)
	M.turn_left(
		speed=50, 
		acceleration=True, 
		initial=10
		)
	M.turn_right(
		speed=50, 
		acceleration=True, 
		initial=10
		)
	M.stop()