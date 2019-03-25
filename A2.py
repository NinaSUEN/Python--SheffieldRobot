#!/usr/bin/env python3
'''COM2009-3009 EV3DEV TEST PROGRAM'''

# Connect left motor to Output C and right motor to Output B
# Connect an ultrasonic sensor to Input 3

import os
import sys
import time
import ev3dev.ev3 as ev3
import statistics as stat
#import math

# state constants
ON = True
OFF = False
RUNNING = 1
STOP = 0

SPD_LIMIT = 100

lightChecker = None

# hardware setting
_sensor_1 = ev3.UltrasonicSensor('in1')
#_sensor_1 = ev3.UltrasonicSensor('in1')
_sensor_3 = ev3.UltrasonicSensor('in3')
# set-up the light sensor
light_sensor = ev3.LightSensor('in2')

_left_motor = ev3.LargeMotor('outB')
_right_motor = ev3.LargeMotor('outC')

def main():
    find_light_target()



'''
def main():
    # This is the main method
    timer1 = time.time()
    bot_state = RUNNING

    while(True):
        current_time = time.time()
        if bot_state is RUNNING:
            if current_time - timer1 >= 0.01:
                # kValues = ZNM(1, mode="P")
                kValues = (2.5, 0, 0)
                uL, eL = PID(0, kValues, debug=False)
                uR, eR = PID(0, kValues, sensor=_sensor_3)

                base_speed = 50
                speed = uL - uR
                speed = limit(speed, base_speed)
                debug_print(uL, uR, speed)
                setMotorSpeed(base_speed + speed, base_speed - speed)

                timer1 = current_time
        elif bot_state is STOP:
            return None 
            '''
        
            

def find_light_target():
    # set the specific mode for light sensor
    light_sensor.mode = 'COL-REFLECT'
    light = light_sensor.value()

    if light_sensor.value() < 70:
        debug_print(light)
        lightChecker = False
    else:
        debug_print(light)
        lightChecker = True

    

def PID(target, kValues=(1, 0, 0),
        intergal=None, last_error=None,
        intergal_limit=None,
        sensor=_sensor_1, debug=False):
    """ A PID Controller which return 
        the signal strength u(t), and 
        the error e(t)"""
    kP, kI, kD = kValues
    ds = sensor.value()
    # PID calculation
    error = target - ds
    intergal = intergal + last_error if intergal is not None and last_error is not None else 0
    delta_error = (error - last_error) if last_error is not None else 0

    if intergal_limit is not None:
        intergal = limit(intergal, intergal_limit)

    # formula
    uT = kP*error + kI*intergal + kD*delta_error
    # debug messages
    if(debug):
        message = 'Distance= %d, Error= %d, Integral= %d, Error\'= %d, u(t)= %.5f' % (
            ds, error, intergal, delta_error, uT)
        debug_print(message)
    return (uT, error)


def ZNM(kU, tU=None, mode="P"):
    """ Ziegler-Nichols method """
    kP, kI, kD = 0, 0, 0
    if mode is "P":
        kP = (0.5*kU)
    elif mode is "PI":
        kP = (0.45*kU)
        kI = (0.54*kU/tU)
    elif mode is "PID":
        kP = (0.6*kU)
        kI = (1.2*kU/tU)
        kD = (3.0*kU*tU/40)
    return kP, kI, kD


def setMotorSpeed(left, right):
    """ Set Motors speed """
    # speed is capped at ±100%
    left = limit(left, 100)
    right = limit(right, 100)

    _left_motor.run_direct(duty_cycle_sp=left)
    _right_motor.run_direct(duty_cycle_sp=right)


def limit(value, _limit):
    """ Limit value with given limit """
    return max(min(_limit, value), -_limit)


"""
    Default functions from template
"""


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


if __name__ == '__main__':
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')
    # announce program start
    ev3.Sound.speak('Test program starting!').wait()
    # the main function of our program
    main()
    # announce program end /
    ev3.Sound.speak('Test program ending').wait()
