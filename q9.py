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
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # display something on the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')

    # set the motor variables
    mb = ev3.LargeMotor('outB')
    mc = ev3.LargeMotor('outC')


    # set the ultrasonic sensor variable
    us3 = ev3.UltrasonicSensor('in3')

    # fetch the distance
    distance = us3.value()

    # constants
    kp = 1
    ki = 0
    kd = 0

    # the target distance
    offset = 500

    # target power level --> be applied when error=0
    tp = 0
    integral = 0
    lastError = 0
    derivative = 0
    error = 0

        

while True:

    # set the ultrasonic sensor variable
    us3 = ev3.UltrasonicSensor('in3')

    # set the motor variables
    mb = ev3.LargeMotor('outB')
    mc = ev3.LargeMotor('outC')

    # constants
    kp = 1
    ki = 0
    kd = 0

    # the target distance
    offset = 500

    # target power level --> be applied when error=0
    tp = 0
    integral = 0
    lastError = 0
    derivative = 0
    error = 0


    distance = us3.value()
    error = distance - offset 
    integral = integral + error
    derivative = error - lastError

    # Calculate the turning value
    turn = kp*error
    
    # set the range for turn value
    if turn > 100:
        turn = 100
    elif turn < -100:
        turn = -100
    else:
        turn = turn    

    debug_print(turn)
    
    
    # the range of wheels : -100 to 100
    mb.run_direct(duty_cycle_sp=turn)
    mc.run_direct(duty_cycle_sp=turn)
  

    lastError = error
        
    # Swift the target distance    
    if offset == 500:
    	offset = 300
    else:
    	offset = 500


if __name__ == '__main__':
    main()
