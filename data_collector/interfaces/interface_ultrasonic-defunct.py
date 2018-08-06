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

"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
                )
            )
        )
    )
from sensors.grove.raw.ultrasonic import GroveDigitalUltrasonicSensor

# Globals
#-------------------------------------------------------------------------------- <-80
ULTRASONIC_DRIVER = GroveDigitalUltrasonicSensor()

# Classes
#-------------------------------------------------------------------------------- <-80
class UtrasonicSensor(object):
    """
    NAME:               UtrasonicSensor
    DESCRIPTION:
                        It is important to cut power to the sensor when not reading 
                        from it. The configure method has power controls built in to 
                        ensure a power cycle for any config changes

    .read()                     to receive sensor output for distance to nearest object
    .stop()                     to cut power to the sensor, cleanup GPIO
    """
    def __init__(self):
        super(UtrasonicSensor, self).__init__()
        self.instrument = ULTRASONIC_DRIVER

    def read(self):
        output = {
            'distance': None
            }
        output['distance'] = self.instrument.measurementInCM()
        return output
        
    def stop(self):
        self.instrument.gpio.cleanup()

# Functions
#-------------------------------------------------------------------------------- <-80
def print_ultrasonic(results):
    print('----------------------------------------')
    print("Instrument Read:")
    print("Distance : {0} CM".format(
        results['distance']
        )
    )

# Main
#-------------------------------------------------------------------------------- <-80
    