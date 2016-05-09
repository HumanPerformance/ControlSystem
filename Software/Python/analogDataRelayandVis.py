"""
analogDataRelay.py

This script has been designed to retrieved data sent by an arduino module through a specific serial port

Fluvio L. Lobo Fenoglietto 05/09/2016

"""

# Importing Modules
import serial
import numpy
from matplotlib import pyplot as plt
from drawnow import *
import time

# Note that:
# 1- In order to install "matplotlib"
#    > sudo apt-get install python-matplotlib
# 2- In order to install "drawnow"
#    > sudo pip install drawnow==0.60

# Creating Serial Objects
arduObj = serial.Serial('/dev/ttyUSB0',115200)

# Defining Variables
IRmeas = []
readTime = []


# Plotting Function
plt.ion()
def dataPlot():
    plt.title('Sensor Analog Output')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.grid(True)
    plt.plot(readTime, IRmeas, 'ro-')

# Operating Loop
counter = 0 # Start counter for data storage
startTime = time.time() # Start timer - using CPU clock
currentTime = 0 # time measurement made at the end of each loop
stopTime = 20 # time at which loop must terminate
while currentTime < stopTime:
    while (arduObj.inWaiting()==0):
        pass
    IRmeas.append(int(arduObj.readline()))
    readTime.append(time.time() - startTime)
    drawnow(dataPlot)

    currentTime = time.time() - startTime
    
    

"""
References

1- http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/

"""





