#!/usr/bin/env python3
'''COM2009-3009 EV3DEV TEST PROGRAM'''

# Connect left motor to Output C and right motor to Output B
# Connect an ultrasonic sensor to Input 3

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


def main():
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')


    # set the motor variables
    mb = ev3.LargeMotor('outB')  # left motor
    mc = ev3.LargeMotor('outC')  # right motor


    # set the ultrasonic sensor variable
    # set it on the left side
    us3 = ev3.UltrasonicSensor('in3')

    # fetch the distance
    distance = us3.value()

    # constants
    kp = 1
    ki = 0
    kd = 0

    # target distance
    offset = 500

    # target power level, it would be applied when error=0
    tp = 30
    integral = 0
    lastError = 0
    derivative = 0
         

    while True: 
       
        # set the motor variables
        mb = ev3.LargeMotor('outB')  # left motor
        mc = ev3.LargeMotor('outC')  # right motor


        # set the ultrasonic sensor variable
        # set it on the left side
        us3 = ev3.UltrasonicSensor('in3')

        # fetch the distance
        distance = us3.value()

        # constants
        kp = 1
        ki = 0
        kd = 0

        # target distance
        offset = 200

        # target power level, it would be applied when error=0
        tp = 20
        integral = 0
        lastError = 0
        derivative = 0


        distance = us3.value()
        error = distance - offset 
        integral = integral + error
        derivative = error - lastError

        # turn
        turn = kp*error
        turn = turn/100

        if turn > 0:
            mb.run_direct(duty_cycle_sp=tp-5) # left
            mc.run_direct(duty_cycle_sp=tp+turn) # right
        elif turn < 0:
            mb.run_direct(duty_cycle_sp=tp-(turn)) 
            mc.run_direct(duty_cycle_sp=tp-5)    
        else:
            mb.run_direct(duty_cycle_sp=tp) 
            mc.run_direct(duty_cycle_sp=tp) 

        debug_print(turn)  


        lastError = error
        


if __name__ == '__main__':
    main()
