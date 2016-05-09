"""
analogDataVis.py

Analog data Visualization is a sample code designed to demo the data acquisition and visualization capabilities of python


Fluvio L. Lobo Fenoglietto 05/06/2016

"""

#
# Import libraries or modules
from nanpy import SerialManager
from nanpy import ArduinoApi
import matplotlib.pyplot as plt
from drawnow import *
import numpy
import time


#
# Establishing communication with Arduino board
connection = SerialManager(device='/dev/ttyUSB0')

#
# Creating Arduino object
a = ArduinoApi(connection=connection)

#
# Signaling connection
a.pinMode(8, a.OUTPUT)
a.digitalWrite(8, a.HIGH)


readTime = []
analogVals = []


#
# Plotting function
plt.ion()
def makeFig():
   plt.title('Sensor Analog Input')
   plt.xlabel('Time (s)')
   plt.ylabel('Voltage (mV)')
   plt.grid(True)
   plt.plot(readTime, analogVals, 'ro-')

#
# Output file
outFile = open('outdata.txt', 'w')


#
# Operation loop
counter = 0 # Start counter for data storage
startTime = time.time() # Start timer - using CPU clock
currentTime = 0 # time measurement made at the end of each loop
stopTime = 20 # time at which loop must terminate
while currentTime < stopTime:
    
   #
   # Measuring analog values
   analogVals.append(a.analogRead(0))
   
   #
   # Measuring time using CPU clock
   readTime.append(time.time() - startTime)
   
   #
   # Plotting data live
   drawnow(makeFig)

   #
   # Printing data to file
   outString = str(readTime[counter]) + ", " + str(analogVals[counter]) + "\n"
   outFile.write(outString)

   currentTime = time.time() - startTime
   counter = counter + 1

outFile.close()
connection.close()


"""

References:
1 - http://matplotlib.org/
2 - https://www.youtube.com/watch?v=zH0MGNJbenc

"""


