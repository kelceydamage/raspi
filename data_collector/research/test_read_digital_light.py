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
from interfaces.interface_digital_light import DigitalLightSensor
from interfaces.interface_digital_light import print_digital_light
import time

# Globals
#-------------------------------------------------------------------------------- <-80
INTERVAL = 100          # ms
TIMING_MODE = 1         # supported 0, 1, 2
                        # maps to integrations timings: 13.7ms, 101ms, 403ms
GAIN_MODE = 1           # supported 0, 1, 2, 3
                        # maps to gain/prescalar multipliers: 1, 4, 16, 64
AUTO = True             # auto configure gain and timing
NIGHT_VISION = False    # max out gain an timing for low light usage

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    digital_light_sensor = DigitalLightSensor()
    digital_light_sensor.configure(
        duration=TIMING_MODE, 
        prescalar=GAIN_MODE, 
        auto=AUTO,
        night_vision=NIGHT_VISION
        )
    digital_light_sensor.start()

    i = 0
    while i < 30:
        time.sleep(float(INTERVAL) / float(1000)) # seconds
        print_digital_light(digital_light_sensor.read(
            lux=True, 
            vis_ir=True, 
            ir=True, 
            gain=True, 
            timing=True
            ))
        i += 1

    digital_light_sensor.stop()