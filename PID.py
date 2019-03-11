#!/usr/bin/env python3

# Connect left motor to Output C and right motor to Output B
# Connect left ultrasonic sensor to input 3 and right to input 2

import os
import sys
import time
import ev3dev.ev3 as ev3

from ev3dev.ev3 import *
from time import sleep

# state constants
ON = True
OFF = False


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


# The main
def main():
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # set the motor variables
    mb = ev3.LargeMotor('outB') # left motor
    mc = ev3.LargeMotor('outC') # right motor
    
    #normalSpeed = 30

    # set the ultrasonic sensor variables
    us3 = ev3.UltrasonicSensor('in3') # left sensor
    us2 = ev3.UltrasonicSensor('in2') # right sensor

    # Constant 
    kp = 2.7
    ki = 10.8
    kd = 0.169

    # variables
    offset = 500
    tp = 50

    leftIntegral = 0
    rightIntegral = 0

    lastErrorLeft = 0
    lastErrorRight = 0

    leftDerivative = 0
    rightDerivative = 0
    

    # loop forever
    while True:

        # PID controller for left sensor
        leftDist = us3.value()

        leftError = leftDist - offset
        leftIntegral = leftIntegral + leftError
        leftDerivative = leftError - lastErrorLeft
        # Correction
        leftTurn = kp*leftError + ki*leftIntegral + kd*leftDerivative
        leftTurn = leftTurn/100

        debug_print("Left distance: {} ".format(leftDist))
        debug_print("Left Turn: {} ".format(LeftTurn))

        

        # PID controller for right sensor
        rightDist = us2.value()

        rightError = rightDist - offset
        rightIntegral = rightIntegral + rightError
        rightDerivative = rightError - lastErrorRight
        # Correction
        rightTurn = kp*rightError + ki*rightIntegral + kd*rightDerivative
        rightTurn = rightTurn/100

        debug_print("Right distance: {} ".format(rightDist))
        debug_print("Right Turn: {} ".format(rightTurn))



        if leftTurn > 0 and rightTurn < 0:
            mb.run_direct(duty_cycle_sp=tp+leftTurn) # left
            mc.run_direct(duty_cycle_sp=leftTurn) # right
        elif leftTurn < 0 and rightTurn > 0:
            mb.run_direct(duty_cycle_sp=tp+rightTurn) 
            mc.run_direct(duty_cycle_sp=rightTurn)
        else:
            mb.run_direct(duty_cycle_sp=tp) 
            mc.run_direct(duty_cycle_sp=tp)



        lastErrorLeft = leftError
        lastErrorRight = rightError


if __name__ == '__main__':
    main()
