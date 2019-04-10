"""
Stethoscope Demo :: Random Filename Recording

Fluvio L Lobo Fenoglietto
12/01/2017
"""

# Import
import  sys
import  os
import  serial
import  time

from    configurationProtocol    import *
device = "stethoscope"
homeDir, pythonDir, deviceDir = definePaths(device)
response = addPaths(pythonDir)

import  stethoscopeDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *
from    stethoscopeProtocol          import *

# Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 1
deviceBTAddress = "00:06:66:D0:E4:37"
baudrate = 115200
attempts = 5
rfObject = createBTPort(deviceBTAddress,portNumber)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject)

print fullStamp() + " Generating String "
randString = genRandString( 4 )
print fullStamp() + " Generated : " + randString

print fullStamp() + " Parsing Rand. Generated String "
startMultiChannelRecording( rfObject, randString )

time.sleep(10)

print fullStamp() + " Stop Recording"
stopRecording( rfObject )

print fullStamp() + " Quick SD card check"
systemCheck( rfObject )

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeBTPort(rfObject)

