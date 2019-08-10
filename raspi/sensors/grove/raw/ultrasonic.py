#!/usr/bin/env python
"""
 * ultrasonic.py
 * A library for ultrasonic sensor at RP
 *
 * Copyright (c) 2012 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : seeed fellow
 * Create Time:
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
"""
import RPi.GPIO as GPIO
import time

GPIO_SIG = 4

# Obsolete example
def getAndPrint():

    print("SeeedStudio Grove Ultrasonic get data and print")

    # test 100 times
    for i in range(100):
        measurementInCM()

    # Reset GPIO settings
    GPIO.cleanup()

class GroveDigitalUltrasonicSensor(object):
    """docstring for GroveDigitalUltrasonicSensor"""
    def __init__(self):
        super(GroveDigitalUltrasonicSensor, self).__init__()
        self.gpio = GPIO
        self.gpio.setmode(self.gpio.BCM)

    def measurementInCM(self):
        # setup the GPIO_SIG as output
        self.gpio.setup(GPIO_SIG, self.gpio.OUT)

        self.gpio.output(GPIO_SIG, self.gpio.LOW)
        time.sleep(0.2)
        self.gpio.output(GPIO_SIG, self.gpio.HIGH)
        time.sleep(0.5)
        self.gpio.output(GPIO_SIG, self.gpio.LOW)
        start = time.time()

        # setup GPIO_SIG as input
        self.gpio.setup(GPIO_SIG, self.gpio.IN)

        # get duration from Ultrasonic SIG pin
        while self.gpio.input(GPIO_SIG) == 0:
            start = time.time()

        while self.gpio.input(GPIO_SIG) == 1:
            stop = time.time()

        return self.measurementPulse(start, stop)


    def measurementPulse(self, start, stop):

        print("Ultrasonic Measurement")

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = distance / 2

        return distance