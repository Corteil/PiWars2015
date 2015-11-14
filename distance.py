#!/usr/bin/env python
# coding: Latin-1

  # Stop robot from hitting wall!

  # Import library functions we need

import Diablo
import time


from Adafruit_ADS1x15 import ADS1x15

ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

# Select the gain
# gain = 6144  # +/- 6.144V
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
# sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
# sps = 860  # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)

# Setup the Diablo
DIABLO = Diablo.Diablo()            # Create a new Diablo object
DIABLO.Init()                       # Set the board up (checks the board is connected)
DIABLO.ResetEpo()                   # Reset the stop switch (EPO) state
                                    # if you do not have a switch across the two pin header then fit the jumper


# Loop over the sequence until the user presses CTRL+C
print 'Press CTRL+C to finish'

#Start motors running

stopValue = 2.3
volts1 = 0
volts2 = 0
run = True
try:
    volts1 = adc.readADCSingleEnded(0, gain, sps) / 1000
    volts2 = adc.readADCSingleEnded(1, gain, sps) / 1000
    while run:

        print("Left: %.2f" % (volts1))
        print("Right: %.2f" % (volts2))
        print(run)
        time.sleep(0.01)
        volts1 = adc.readADCSingleEnded(0, gain, sps) / 1000
        volts2 = adc.readADCSingleEnded(1, gain, sps) / 1000


        if (volts1 > stopValue) or (volts2 > stopValue):
            run = False
        else:
            DIABLO.SetMotors(0.15)


except KeyboardInterrupt:
    # User has pressed CTRL+C
    DIABLO.MotorsOff()                 # Turn both motors off
    print 'Ctl C been pressed'
DIABLO.MotorsOff()                 # Turn both motors off
print 'Stop!!!!'
