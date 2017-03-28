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
from sensors.grove.i2c.digital_light_sensor import GroveI2CDigitalLightSensor

# Globals
#-------------------------------------------------------------------------------- <-80
# Open connection to sensor
COLOR_SENSOR_DRIVER = GroveI2CDigitalLightSensor()

# Classes
#-------------------------------------------------------------------------------- <-80
class DigitalLightSensor(object):
    """
    NAME:               DigitalLightSensor
    DESCRIPTION:
                        It is important to cut power to the sensor when not reading 
                        from it. The configure method has power controls built in to 
                        ensure a power cycle for any config changes

    .configure                  to initialize the sensor
        duration        int     set to either: 0 (13.7ms), 1 (101ms), 2 (403ms)
        prescalar       int     set to either: 0 (1x), 1 (4x), 2 (16x), 3 (64x)
        auto            bool    enable to auto adjust gain and integration timing
        night_vision    bool    enable to maximize gain and timing for low-light usage
    .start()                    to start power to the sensor
    .read()                     to receive sensor output
        lux             bool    to receive illuminance
        vis_ir          bool    to receive visible spectrum illuminance
        ir              bool    to receive infrared illuminance
        gain            bool    to receive current gain level
        timing          bool    to receive the current integration timing
    .stop()                     to cut power to the sensor, cleanup GPIO
    """
    def __init__(self):
        super(DigitalLightSensor, self).__init__()
        self.instrument = COLOR_SENSOR_DRIVER

    def configure(self, duration, prescalar, auto=False, night_vision=False):
        self.instrument.configure(duration, prescalar, auto, night_vision)

    def start(self):
        self.instrument.powerUp()

    def stop(self):
        self.instrument.powerDown()

    def read(self, lux=True, vis_ir=False, ir=False, gain=False, timing=False):
        # Returns a dict of instrument readings. If the instrument is not ready it 
        # will return a string error message. 
        output = {
            'lux': None, 
            'vis_ir': None, 
            'ir': None,
            'gain': None,
            'timing': None,
            'error': None
            }
        self.instrument.readLux()
        if self.instrument.overflow == -1:
            output['error'] = 'overflow'
            return output
        raw = self.instrument.calculateLux()
        if lux:
            output['lux'] = raw[0]
        if vis_ir:
            output['vis_ir'] = raw[1]
        if ir:
            output['ir'] = raw[2]
        if gain:
            output['gain'] = raw[3]
        if timing:
            output['timing'] = raw[4]
        return output

# Functions
#-------------------------------------------------------------------------------- <-80
def print_digital_light(results):
    print('----------------------------------------')
    print("Instrument Read:")
    print("LUX: {0}".format(
        results['lux']
        )
    )
    print("VIS_IR: {0}".format(
        results['vis_ir']
        )
    )
    print("IR: {0}".format(
        results['ir']
        )
    )
    print("GAIN: {0}".format(
        results['gain']
        )
    )
    print("TIMING [ms]: {0}".format(
        results['timing']
        )
    )

# Main
#-------------------------------------------------------------------------------- <-80
    