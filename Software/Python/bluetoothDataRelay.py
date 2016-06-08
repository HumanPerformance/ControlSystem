"""
bluetoothDataRelay.py

Fluvio L. Lobo Fenoglietto 06/07/2016
"""

# Import Modules
import os
import serial

# Variable Definitions
arduID = 'oto\n'
inString = ''
stateSwitch = ''

# Creating Serial Object
## PORTS
port = "rfcomm0"
## Device Address
address = "00:06:66:7D:98:58"
## Talking to the terminal
cmd = "sudo rfcomm bind /dev/" + port + " " + address
## Sending command
os.system(cmd)

#arduObj = serial.Serial('/dev/rfcomm1',115200)


#arduState = 'unpaired'

#
# unpaired state loop (idle state loop)
#
#while arduState == 'unpaired':
 #   inString = arduObj.readline()
 #   print inString

