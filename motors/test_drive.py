#! /usr/bin/env python3

from raspi.motors import drive as d

DRIVER = d.PyWrap_MotorDrive()

def test_configure():
    DRIVER.configure()
    assert DRIVER.__getattr__("polarity_bool") == False
    assert DRIVER.__getattr__("duration") == 0
    assert DRIVER.__getattr__("accel_interval") == 1

def test_polarity():
    # Natural polarity is revered on the DC motors
    assert DRIVER.polarity(5, -5) == (-5, 5)

def test_acceleration():
    assert DRIVER.accelerate(0, 5, True) == [x for x in range(0, 5)][::-1]
    assert DRIVER.accelerate(0, 5, False) == [x for x in range(0, 5)]

if __name__ == '__main__':
    print(test_instantiate())