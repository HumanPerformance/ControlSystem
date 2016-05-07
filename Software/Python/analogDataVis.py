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




counter = []
i = 0
analogVals = []


#
# Plotting function
plt.ion()
def makeFig():
   plt.plot(analogVals)


flag = 0
while flag == 0:
   analogVals.append(a.analogRead(0))
   counter.append(i)
   i = i + 1
   drawnow(makeFig)
   plt.pause(0.000001)
       

connection.close()


"""

References:
1 - http://matplotlib.org/
2 - https://www.youtube.com/watch?v=zH0MGNJbenc

"""


