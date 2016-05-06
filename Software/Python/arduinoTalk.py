
#
# arduinoTalk
#
# The following python script was designed to demo the communication between the Raspberry Pi and an Arduino module in a master-slave configuration
#
# Fluvio L. Lobo Fenoglietto 05/06/2016


#
# Requirements:
# a) The 'nanpy-firmaware' must have been installed on the Arduino board to be used as a slave


#
# Import libraries and/or Modules

from nanpy import SerialManager
from nanpy import ArduinoApi


#
# Creating Serial Object
connection = SerialManager(device='/dev/ttyUSB0')


#
# Creating Arduino object
a = ArduinoApi(connection=connection)

#
# Signaling successful connection
a.pinMode(8, a.OUTPUT)
a.digitalWrite(8, a.HIGH)



