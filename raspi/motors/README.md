[![Coverage Status](https://coveralls.io/repos/github/kelceydamage/raspi/badge.svg?branch=master)](https://coveralls.io/github/kelceydamage/raspi?branch=master)
# Drive.so

## Classes
* ContinuousTrackedMovement()
* TrackedMovement()
* Movement()

## C++/Cython interface

### Basic movement
Setup interface
```python
M = ContinuousTrackedMovement()
```

Determing the acceleration interval
```python
M.accel_interval = 1
```

Move forward
```python
M.duration = 5
M.forward(speed=50, acceleration=True, initial=10)
```

Move backwards
```python
M.duration = 5
M.reverse(speed=50, deceleration=True, initial=10)
```

Move left turn
```python
M.duration = 5
M.turn_left(speed=50, acceleration=True, initial=10)
```

When moving there are two key parameters: `duration` and `acceleration/deceleration`. `duration` is an attribute and controls how long the movement command should be executed for (how long the motor should receive voltage), before the motor turns idle. `acceleration/deceleration` determines if there will be a gradual speed up and slowdown within the movement command.

### Continuous movement
Setup interface
```python
M = ContinuousTrackedMovement()
```

Determing the acceleration interval
```python
M.accel_interval = 1
```

Movement
```python
# Movement examples with graduated turning.
gearing = 1.0/32.0
while gearing < 1.0/2.0:
    gearing = M.graduated_turn(gearing, 2, INWARDS)
    M.update(
        [20, 0, FORWARD_LEFT_BIAS, False, False, gearing]
        )

gearing = 1.0/1.0
while gearing > 1.0/32.0:
    gearing = M.graduated_turn(gearing, 2, OUTWARDS)
    M.update(
        [20, 0, FORWARD_LEFT_BIAS, True, False, gearing]
        )

# Example of movement without graduated turning. In this example the motors will drive 
# leftwards accelerating by a multiple of 4 each duration interval.
gearing = 1.0/2.0
M.duration = 5
M.accel_interval = 4
M.update(
    [20, 5, FORWARD_LEFT_BIAS, True, False, gearing]
    )

# Explicit call to .stop(). This is required to terminate voltage to the motor.
M.stop()
```

Gearing determines the direction the movement will bias towards. the `graduated_turn` method allows for and increase or decrease in the gearing withing each loop interval.

The `update` method allows sending the motor a new signal without terminating any current signals. `update` is also a wrapper for `.move()` allowing a list of arguments to be passed instead of individual explicit arguments.