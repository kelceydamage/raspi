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
#
# This library is based on the work by Cedric Maion https://github.com/cmaion/TSL2561

# Doc
#-------------------------------------------------------------------------------- <-80
"""
Sample collector for reading instrument data
"""

# Imports
#-------------------------------------------------------------------------------- <-80
from __future__ import print_function
import time
import smbus2 as smbus
import RPi.GPIO as GPIO
from smbus2 import SMBus

# Globals
#-------------------------------------------------------------------------------- <-80
TSL2561_Control = 0x80
TSL2561_Timing = 0x81
TSL2561_Interrupt = 0x86
TSL2561_Channel0L = 0x8C
TSL2561_Channel0H = 0x8D
TSL2561_Channel1L = 0x8E
TSL2561_Channel1H = 0x8F

TSL2561_Address = 0x29      #device address

LUX_SCALE = 14              # scale by 2^14
RATIO_SCALE = 9             # scale ratio by 2^9
CH_SCALE = 10               # scale channel values by 2^10
CHSCALE_TINT0 = 0x7517      # 322/11 * 2^CH_SCALE
CHSCALE_TINT1 = 0x0fe7      # 322/81 * 2^CH_SCALE

K1T = 0x0040                # 0.125 * 2^RATIO_SCALE
B1T = 0x01f2                # 0.0304 * 2^LUX_SCALE
M1T = 0x01be                # 0.0272 * 2^LUX_SCALE
K2T = 0x0080                # 0.250 * 2^RATIO_SCA
B2T = 0x0214                # 0.0325 * 2^LUX_SCALE
M2T = 0x02d1                # 0.0440 * 2^LUX_SCALE
K3T = 0x00c0                # 0.375 * 2^RATIO_SCALE
B3T = 0x023f                # 0.0351 * 2^LUX_SCALE
M3T = 0x037b                # 0.0544 * 2^LUX_SCALE
K4T = 0x0100                # 0.50 * 2^RATIO_SCALE
B4T = 0x0270                # 0.0381 * 2^LUX_SCALE
M4T = 0x03fe                # 0.0624 * 2^LUX_SCALE
K5T = 0x0138                # 0.61 * 2^RATIO_SCALE
B5T = 0x016f                # 0.0224 * 2^LUX_SCALE
M5T = 0x01fc                # 0.0310 * 2^LUX_SCALE
K6T = 0x019a                # 0.80 * 2^RATIO_SCALE
B6T = 0x00d2                # 0.0128 * 2^LUX_SCALE
M6T = 0x00fb                # 0.0153 * 2^LUX_SCALE
K7T = 0x029a                # 1.3 * 2^RATIO_SCALE
B7T = 0x0018                # 0.00146 * 2^LUX_SCALE
M7T = 0x0012                # 0.00112 * 2^LUX_SCALE
K8T = 0x029a                # 1.3 * 2^RATIO_SCALE
B8T = 0x0000                # 0.000 * 2^LUX_SCALE
M8T = 0x0000                # 0.000 * 2^LUX_SCALE

K1C = 0x0043                # 0.130 * 2^RATIO_SCALE
B1C = 0x0204                # 0.0315 * 2^LUX_SCALE
M1C = 0x01ad                # 0.0262 * 2^LUX_SCALE
K2C = 0x0085                # 0.260 * 2^RATIO_SCALE
B2C = 0x0228                # 0.0337 * 2^LUX_SCALE
M2C = 0x02c1                # 0.0430 * 2^LUX_SCALE
K3C = 0x00c8                # 0.390 * 2^RATIO_SCALE
B3C = 0x0253                # 0.0363 * 2^LUX_SCALE
M3C = 0x0363                # 0.0529 * 2^LUX_SCALE
K4C = 0x010a                # 0.520 * 2^RATIO_SCALE
B4C = 0x0282                # 0.0392 * 2^LUX_SCALE
M4C = 0x03df                # 0.0605 * 2^LUX_SCALE
K5C = 0x014d                # 0.65 * 2^RATIO_SCALE
B5C = 0x0177                # 0.0229 * 2^LUX_SCALE
M5C = 0x01dd                # 0.0291 * 2^LUX_SCALE
K6C = 0x019a                # 0.80 * 2^RATIO_SCALE
B6C = 0x0101                # 0.0157 * 2^LUX_SCALE
M6C = 0x0127                # 0.0180 * 2^LUX_SCALE
K7C = 0x029a                # 1.3 * 2^RATIO_SCALE
B7C = 0x0037                # 0.00338 * 2^LUX_SCALE
M7C = 0x002b                # 0.00260 * 2^LUX_SCALE
K8C = 0x029a                # 1.3 * 2^RATIO_SCALE
B8C = 0x0000                # 0.000 * 2^LUX_SCALE
M8C = 0x0000                # 0.000 * 2^LUX_SCALE

# bus parameters
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

# Classes
#-------------------------------------------------------------------------------- <-80
class GroveI2CDigitalLightSensor(object):
    """
    NAME: GroveI2CDigitalLightSensor
    DESCRIPTION:
    """
    def __init__(self):
        super(GroveI2CDigitalLightSensor, self).__init__()
        self.bus = bus
        self.debug = False
        self.packageType = 0 # 0=T package, 1=CS package
        self.gain = 0        # current gain: 0=1x, 1=16x
        self.gain_m = 0      # current gain, as multiplier
        self.timing = 0      # current integration time: 0=13.7ms, 1=101ms, 2=402ms
        self.timing_ms = 0   # current integration time, in ms
        self.channel0 = 0    # raw current value of visible+ir sensor
        self.channel1 = 0    # raw current value of ir sensor
        self.schannel0 = 0   # normalized current value of visible+ir sensor
        self.schannel1 = 0   # normalized current value of ir sensor

    def configure(self, timing_mode=0, gain_mode=0, auto=False, night_vision=False):
        if auto == True and night_vision != True:
            if self.debug:
                print('START CALIBRATION')
            self.set_conf_values(0, 0)
            self.powerUp()
            self.readLux()
            self.powerDown()
            self.calibrate(0, 0)
        elif night_vision:
            self.set_conf_values(3, 2)
        else:
            self.set_conf_values(gain_mode, timing_mode)

    def set_conf_values(self, gain_mode, timing_mode):
        self.powerUp()
        self.set_gain(gain_mode)
        self.set_timing(timing_mode)
        self.writeRegister(TSL2561_Timing, self.timing | self.gain << 4)
        self.writeRegister(TSL2561_Interrupt, 0x00)
        self.powerDown()

    def calibrate(self, timing, gain):
        if self.channel0 < 500 and self.timing == timing and self.gain == gain:
            if timing < 1:
                timing += 1
            elif timing == 1 and gain < 4:
                gain += 1
            self.set_conf_values(timing_mode=timing, gain_mode=gain)
            if self.debug:
                print("TSL2561.readVisibleLux: too dark. Increasing integration time to: {0} and gain to {1}".format(timing, gain))
            self.powerUp()
            self.readLux()
            self.powerDown()
            if not (timing == 1 and gain == 3):
                self.calibrate(timing, gain)
        elif (self.channel0 > 20000 or self.channel1 > 20000) and self.timing > 0 and self.gain > 0:
            if gain > 0:
                gain -= 1
            elif gain == 0 and timing > 0:
                timing -= 1
            self.set_conf_values(timing_mode=timing, gain_mod=gain)
            if self.debug:
                print("TSL2561.readVisibleLux: too dark. Increasing integration time to: {0} and gain to {1}".format(timing, gain))
            self.powerUp()
            self.readLux()
            self.powerDown()
            if not (timing == 0 and gain == 0):
                self.calibrate(timing, gain)
        if self.debug:
            print('CALIBRATION COMPLETE')
            print('Timing: {0}, Gain: {1}'.format(self.timing_ms, self.gain_m))
        self.timing = timing
        self.gain = gain

    def set_gain(self, gain):
        self.gain = gain
        if self.gain == 0:
            self.gain_m = 1
        elif self.gain == 1:
            self.gain_m = 4
        elif self.gain == 2:
            self.gain_m = 16
        else:
            self.gain_m = 64

    def set_timing(self, timing):
        self.timing = timing
        if self.timing == 0:
            self.timing_ms = 13.7
        elif self.timing == 1:
            self.timing_ms = 101
        else:
            self.timing_ms = 402

    def powerUp(self):
        self.writeRegister(TSL2561_Control, 0x03)

    def powerDown(self):
        self.writeRegister(TSL2561_Control, 0x00)

    def writeRegister(self, address, val):
        try:
            self.bus.write_byte_data(
                TSL2561_Address,
                address,
                val
                )
            if (self.debug):
                print("TSL2561.writeRegister: wrote 0x%02X to reg 0x%02X" % (val, address))
        except IOError:
            print("TSL2561.writeRegister: error writing byte to reg 0x%02X" % address)

    def readRegister(self, address):
        try:
            byteval = self.bus.read_byte_data(
                TSL2561_Address,
                address
                )
            if (self.debug):
                print("TSL2561.readRegister: returned 0x%02X from reg 0x%02X" % (byteval, address))
            return byteval
        except IOError:
            print("TSL2561.readRegister: error reading byte from reg 0x%02X" % address)

    def readLux(self):
        time.sleep(float(self.timing_ms + 1) / 1000)
        ch0_low  = self.readRegister(TSL2561_Channel0L)
        ch0_high = self.readRegister(TSL2561_Channel0H)
        ch1_low  = self.readRegister(TSL2561_Channel1L)
        ch1_high = self.readRegister(TSL2561_Channel1H)
        self.channel0 = (ch0_high<<8) | ch0_low
        self.channel1 = (ch1_high<<8) | ch1_low
        if self.debug:
            print("TSL2561.readVisibleLux: channel 0 = %i, channel 1 = %i [gain=%ix, timing=%ims]" % (self.channel0, self.channel1, self.gain_m, self.timing_ms))

    def overflow(self):
        if (self.timing == 0 and (self.channel0 > 5000 or self.channel1 > 5000)) \
        or (self.timing == 1 and (self.channel0 > 37000 or self.channel1 > 37000)) \
        or (self.timing == 2 and (self.channel0 > 65000 or self.channel1 > 65000)):
            return -1

    def calculateLux(self):
        chScale = 0
        if self.timing == 0:   # 13.7 msec
            chScale = CHSCALE_TINT0
        elif self.timing == 1: # 101 msec
            chScale = CHSCALE_TINT1;
        else:           # assume no scaling
            chScale = (1 << CH_SCALE)

        if self.gain == 0:
            chScale = chScale << 4 # scale 1X to 16X

        # scale the channel values
        #global self.schannel0, self.schannel1
        self.schannel0 = (self.channel0 * chScale) >> CH_SCALE
        self.schannel1 = (self.channel1 * chScale) >> CH_SCALE

        ratio = 0
        if self.schannel0 != 0:
            ratio = (self.schannel1 << (RATIO_SCALE+1)) / self.schannel0
        ratio = (ratio + 1) >> 1

        if self.packageType == 0: # T package
            if ((ratio >= 0) and (ratio <= K1T)):
                b=B1T; m=M1T;
            elif (ratio <= K2T):
                b=B2T; m=M2T;
            elif (ratio <= K3T):
                b=B3T; m=M3T;
            elif (ratio <= K4T):
                b=B4T; m=M4T;
            elif (ratio <= K5T):
                b=B5T; m=M5T;
            elif (ratio <= K6T):
                b=B6T; m=M6T;
            elif (ratio <= K7T):
                b=B7T; m=M7T;
            elif (ratio > K8T):
                b=B8T; m=M8T;
        elif self.packageType == 1: # CS package
            if ((ratio >= 0) and (ratio <= K1C)):
                b=B1C; m=M1C;
            elif (ratio <= K2C):
                b=B2C; m=M2C;
            elif (ratio <= K3C):
                b=B3C; m=M3C;
            elif (ratio <= K4C):
                b=B4C; m=M4C;
            elif (ratio <= K5C):
                b=B5C; m=M5C;
            elif (ratio <= K6C):
                b=B6C; m=M6C;
            elif (ratio <= K7C):
                b=B7C; m=M7C;

        temp = ((self.schannel0*b)-(self.schannel1*m))
        if temp < 0:
            temp = 0;
        temp += (1<<(LUX_SCALE-1))
        # strip off fractional portion
        lux = temp>>LUX_SCALE
        if self.debug:
            print("TSL2561.calculateLux: %i" % lux)

        return [lux, self.channel0, self.channel1, self.gain_m, self.timing_ms]
