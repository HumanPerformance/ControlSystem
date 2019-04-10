"""
analogDataRelay.py

This script has been designed to retrieved data sent by an arduino module through a specific serial port

Fluvio L. Lobo Fenoglietto 05/09/2016

"""

# Importing Modules
import serial
import numpy
#import matplotlib.pyplot as plt
#from drawnow import *

# Creating Serial Objects
arduObj = serial.Serial('/dev/ttyUSB0',115200)

# Defining Variables
IRmeas = []


# Operating Loop
arduDataList = []
while True:
    while (arduObj.inWaiting()==0):
        pass
    arduDataList.append(int(arduObj.readline()))
    
    

"""
References

1- http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/

"""





