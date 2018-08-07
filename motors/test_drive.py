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

# Test the move function to ensure the basic direction types return the desired velocities for the 
# motor controller.
def test_move():
    # Available keywords:
    #
    # speed             uint_fast8_t
    # initial           uint_fast8_t
    # direction         uint_fast8_t
    # acceleration      bint
    # positive          bint
    # gearing           float
    # test              bint
    # 
    # Returns velocity == pair[int_fast16_t, int_fast16_t]
    DRIVER.duration = 1
    assert DRIVER.move(5, direction=0, gearing=1/2, test=True) == (2, 2)

# Test the update function which is a wrapper for the move function allowing the passing of a list 
# of args.
def test_update():
    # actual _update() c++ method takes the O_MOVEMENT struct. Below is a mapping of list to struct 
    # attributes.
    #
    # type(list) => O_MOVEMENT type(movementObject) STRUCT attributes
    # speed           = args[0]                      uint_fast8_t
    # initial         = args[1], default 0           uint_fast8_t
    # direction       = args[2], default 0           uint_fast8_t
    # acceleration    = args[3], default False       bint
    # positive        = args[4], default True        bint
    # gearing         = args[5], 1.0                 float
    # test            = args[6], default False       bint
    # 
    # Returns velocity == pair[int_fast16_t, int_fast16_t]
    DRIVER.duration = 1
    args = [5, 0, 0, False, True, 1/2, True]
    assert DRIVER.update(args) == (2, 2)

# test the graduate_turn function  to ensure correct turning parameters.
def test_graduated_turn():
    # Available keywords:
    #
    # fraction         float
    # stepping         uint_fast8_t
    # direction        uint_fast8_t, INWARDS=9 || OUTWARDS=10
    #
    # Returns float
    assert DRIVER.graduated_turn(direction=9, stepping=1, fraction=1/2) == 0.5

# Test the movement_type function to ensure the correct velocities are returned. (0, 0) cases are
# currently un-implemented.
def test_movement_type():
    # Directions:
    #
    # FORWARD             = 0
    # REVERSE             = 1
    # LEFT                = 2
    # RIGHT               = 3
    # STOP                = 4
    # REVERSE_LEFT_BIAS   = 5
    # REVERSE_RIGHT_BIAS  = 6
    # FORWARD_LEFT_BIAS   = 7
    # FORWARD_RIGHT_BIAS  = 8
    # 
    # Available keywords:
    #
    # direction         uint_fast8_t         
    # speed             uint_fast8_t        
    # gearing           float       
    #
    # Returns velocity == pair[int_fast16_t, int_fast16_t]
    assert DRIVER.movement_type(direction=0, speed=5, gearing=1/2) == (2, 2)
    assert DRIVER.movement_type(direction=1, speed=5, gearing=1/2) == (-2, -2)
    assert DRIVER.movement_type(direction=2, speed=5, gearing=1/2) == (0, 0)
    assert DRIVER.movement_type(direction=3, speed=5, gearing=1/2) == (0, 0)
    assert DRIVER.movement_type(direction=4, speed=5, gearing=1/2) == (0, 0)
    assert DRIVER.movement_type(direction=5, speed=5, gearing=1/2) == (2, -5)
    assert DRIVER.movement_type(direction=6, speed=5, gearing=1/2) == (5, -2)
    assert DRIVER.movement_type(direction=7, speed=5, gearing=1/2) == (-2, 5)
    assert DRIVER.movement_type(direction=8, speed=5, gearing=1/2) == (-5, 2)

# Main
#---------------------------------------------------------------------------------------------------- <-100
if __name__ == '__main__':
    pass