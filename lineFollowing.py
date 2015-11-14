#!/usr/bin/env python
# coding: Latin-1

# 3 Point Turn - hopefully!
# Import library functions we need

import serial
import time
import Diablo
import pygame
import sys
import os




# Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
sys.stdout = sys.stderr

# Setup the Diablo
DIABLO = Diablo.Diablo()
#DIABLO.i2cAddress = 0x44                  # Uncomment and change the value if you have changed the board address
DIABLO.Init()
if not DIABLO.foundChip:
    boards = Diablo.ScanForDiablo()
    if len(boards) == 0:
        print 'No Diablo found, check you are attached :)'
    else:
        print 'No Diablo at address %02X, but we did find boards:' % (DIABLO.i2cAddress)
        for board in boards:
            print '    %02X (%d)' % (board, board)
        print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
        print 'DIABLO.i2cAddress = 0x%02X' % (boards[0])
    sys.exit()
#DIABLO.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
DIABLO.ResetEpo()
DIABLO.SetCommsFailsafe(True)
failsafe = DIABLO.GetCommsFailsafe()
if not failsafe:
    print 'Failsafe did not enable!'
    sys.exit()

# Settings for the joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = True              # Set this to True if up and down appear to be swapped
axisLeftRight = 2                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
buttonResetEpo = 3                      # Joystick button number to perform an EPO reset (Start)
buttonFast = 8                          # Joystick button number for driving fast whilst held (L2)
slowFactor = 0.5                        # Speed to slow to when the drive fast button is not held, e.g. 0.5 would be half speed
buttonFastTurn = 9                      # Joystick button number for turning fast (R2)
buttonQuit = 0                          # Quit button = select button
interval = 0.01                         # Time between updates in seconds, smaller responds faster but uses more processor time


def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv


# Setup pygame
os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

flag = True

# start serial port
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=0.1)

print 'Press CTRL+C or "SELECT" on joypad to quit'

# read the serial port

try:
        flag = True

        while flag:
            #print 'Press CTRL+C or "SELECT" on joypad to quit'
            # Get the latest events from the system
            hadEvent = False
            events = pygame.event.get()
            # Handle each event individually
            for event in events:
                if event.type == pygame.QUIT:
                    # User exit
                    running = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    # A button on the joystick just got pushed down
                    hadEvent = True

                if joystick.get_button(buttonQuit):
                    DIABLO.MotorsOff()
                    print('Exit Button Pressed')
                    sys.exit()
                 # Start the motors

            '''
            DIABLO.SetMotor1(motorSpeed1)
            DIABLO.SetMotor2(motorSpeed2)
            '''

            # read the serial port
            print('reading')
            rcv = readlineCR(port)

            # and then spilt the result into 2 int's if possable

            numberAsString = rcv.split()
            print(type(numberAsString))
            print(numberAsString[0])
            position = int(numberAsString[0])

            print position

            if position > 3550:
                print('more power to right motor')
                DIABLO.SetMotor1(0)
                DIABLO.SetMotor2(-0.5)
            elif position < 3450:
                print('more power to left motor')
                DIABLO.SetMotor1(-0.5)
                DIABLO.SetMotor2(0)
            else:
                print('power to both motors')
                DIABLO.SetMotor1(-0.4)
                DIABLO.SetMotor2(-0.4)
        time.sleep(0.01)

except KeyboardInterrupt:
    # User has pressed CTRL+C
    DIABLO.MotorsOff()                 # Turn both motors off
    print ('**** Ctl C been pressed ****')

DIABLO.MotorsOff()                 # Turn both motors off
