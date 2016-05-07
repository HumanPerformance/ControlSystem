"""
analogDataVis.py

Analog data Visualization is a sample code designed to demo the data acquisition and visualization capabilities of python


Fluvio L. Lobo Fenoglietto 05/06/2016

"""

#
# Import libraries or modules
from nanpy import SerialManager
from nanpy import ArduinoApi
import numpy

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



