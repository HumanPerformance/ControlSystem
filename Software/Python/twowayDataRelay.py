"""
twowayDataRelay.py

Fluvio L. Lobo Fenoglietto 05/10/2016
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

#
# unpaired state loop (idle state loop)
#
while arduState == 'unpaired':
    inString = arduObj.readline()
    if inString == arduID:
        print 'Arduino OTO found!'
        print 'Sending GO message...'
        arduObj.write('GO')
        arduState = 'paired'

#
# paired state loop (active state loop)
#
arduDataList = []
while arduState == 'paired':
    arduDataList.append(int(arduObj.readline()))
