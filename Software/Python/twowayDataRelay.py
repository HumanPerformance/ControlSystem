"""
twowayCom.py

Two-way communication was design to establish bidirectional communication between the arduinos and raspberry pi (control system)

Fluvio L. Lobo Fenoglietto 05/09/2016
"""

# Import Modules
import serial

# Variable Definitions
arduID = 'oto\n'
inString = ''
stateSwitch = ''

# Creating Serial Object
arduObj = serial.Serial('/dev/ttyUSB0',115200)

arduState = 'unpaired'
while arduState == 'unpaired':
    inString = arduObj.readline()
    if inString == arduID:
        print 'Arduino OTO found!'
        print 'Sending GO message...'
        arduObj.write('GO')
        arduState = 'paired'





