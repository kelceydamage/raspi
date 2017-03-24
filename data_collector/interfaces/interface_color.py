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
from sensors.grove.i2c.color_sensor import GroveI2CColorSensor

# Globals
#-------------------------------------------------------------------------------- <-80
# Open connection to sensor
COLOR_SENSOR_DRIVER = GroveI2CColorSensor()

# Classes
#-------------------------------------------------------------------------------- <-80
class ColorSensor(object):
    """
    NAME: ColorSensor
    DESCRIPTION:
    """
    def __init__(self):
        super(ColorSensor, self).__init__()
        self.instrument = COLOR_SENSOR_DRIVER

    def configure(self, duration, prescalar, continuous=False):
        # Supported gain/prescalar multipliers: 1, 4, 16 and 64
        self.continuous = continuous
        if self.continuous:
            self.instrument.use_continuous_integration(duration)
        else:
            self.instrument.use_manual_integration()
        self.instrument.set_gain_and_prescaler(prescalar)

    def start(self):
        self.instrument.start_integration()

    def stop(self):
        # Stop integration before changing settings
        self.instrument.stop_integration()

    def read(self, rgb=False, cie=False, closest=True):
        # Returns a dict of instrument readings. If the instrument is not ready it 
        # will return a string error message. 
        output = {
            'closest': None, 
            'rgb': None, 
            'cie': None
            }
        if self.instrument.is_integration_complete():
            if closest:
                output['closest'] = self.instrument.read_color_name()
            if rgb:
                output['rgb'] = self.instrument.read_rgbc()
            if cie:
                output['cie'] = self.instrument.read_xy()
            return output
        else:
            return "Continuous integration incomplete"

# Functions
#-------------------------------------------------------------------------------- <-80
def print_color(results):
    print('----------------------------------------')
    print("Instrument Read:")
    print("RGB: {0},{1},{2} - Clear {3}".format(
        results['rgb'][0], 
        results['rgb'][1], 
        results['rgb'][2], 
        results['rgb'][3]
        )
    )
    print("CIE [x|y]: {0},{1}".format(
        results['cie'][0], 
        results['cie'][1]
        )
    )
    print("Closest color match: {0}".format(
        results['closest']
        )
    )

# Main
#-------------------------------------------------------------------------------- <-80
    