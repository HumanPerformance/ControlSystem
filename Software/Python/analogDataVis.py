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
from matplotlib import style
import numpy


style.use('fivethirtyeight')
fig  = plt.figure()
ax1 = fig.add_subplot(1,1,1)


#
# Establishing communication with Arduino board
connection = SerialManager(device='COM3')

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
flag = 0
while flag == 0:
   analogVals.append(a.analogRead(0))
   counter.append(i)
   i = i + 1
   
   ax1.clear()
   ax1.plot(counter,analogVals)
   plt.show()
       

connection.close()


"""

References:
1 - http://matplotlib.org/
2 - https://www.youtube.com/watch?v=zH0MGNJbenc

"""


