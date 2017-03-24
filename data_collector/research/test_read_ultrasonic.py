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
Sample collector for reading instrument data
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from interfaces.interface_ultrasonic import UtrasonicSensor
from interfaces.interface_ultrasonic import print_ultrasonic
import time

# Globals
#-------------------------------------------------------------------------------- <-80
INTERVAL = 100		# ms

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
	ultrasonic_sensor = UtrasonicSensor()

	i = 0
	while i < 30:
		time.sleep(float(INTERVAL) / float(1000)) # seconds
		print_ultrasonic(ultrasonic_sensor.read())
		i += 1

	ultrasonic_sensor.stop()