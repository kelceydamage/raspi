#! /usr/bin/env python3

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
# 

# Imports
#---------------------------------------------------------------------------------------------------- <-100
from raspi.motors import drive as d

# Constants
#---------------------------------------------------------------------------------------------------- <-100
DRIVER = d.PyWrap_MotorDrive()

# Functions
#---------------------------------------------------------------------------------------------------- <-100
# Test to make sure configuration settings are applied. configure() replaces __init__ in pure c++ classes.
def test_configure():
    assert DRIVER.__getattr__("polarity_bool") == False
    assert DRIVER.__getattr__("duration") == 0
    assert DRIVER.__getattr__("accel_interval") == 0
    DRIVER.configure()
    assert DRIVER.__getattr__("polarity_bool") == False
    assert DRIVER.__getattr__("duration") == 0
    assert DRIVER.__getattr__("accel_interval") == 1

# Test the polarity function is returning the corret reverse polarity with the polarity_bool attribute 
# initialized to False. Natural polarity is revered on the DC motors.
def test_polarity():
    assert DRIVER.polarity(5, -5) == (-5, 5)

# Test the acceleration function is correctly returning a list of spead values to be consumed with 
# .pop_back().
def test_acceleration():
    assert DRIVER.accelerate(0, 5, True) == [x for x in range(0, 5)][::-1]
    assert DRIVER.accelerate(0, 5, False) == [x for x in range(0, 5)]

# Test the ove function to ensure the basic direction types return the desired velocities for the 
# motor controller.
def test_move():
    DRIVER.duration = 1
    assert DRIVER.move(5, direction=0, gearing=1/2, test=True) == (2, 2)
    assert DRIVER.move(5, direction=1, gearing=1/2, test=True) == (-2, -2)
    assert DRIVER.move(5, direction=5, gearing=1/2, test=True) == (2, -5)
    assert DRIVER.move(5, direction=6, gearing=1/2, test=True) == (5, -2)
    assert DRIVER.move(5, direction=7, gearing=1/2, test=True) == (-2, 5)
    assert DRIVER.move(5, direction=8, gearing=1/2, test=True) == (-5, 2)

# Main
#---------------------------------------------------------------------------------------------------- <-100
if __name__ == '__main__':
    pass