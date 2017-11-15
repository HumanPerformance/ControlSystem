"""
Stethoscope Demo :: Blending

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
01/31/2017
"""

# Import Modules, Libraries and/or Functions
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

# Demo Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 0
deviceBTAddress = "00:06:66:8C:9C:2E"
baudrate = 115200
attempts = 5
#rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)
rfObject = createBTPort(deviceBTAddress,portNumber)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject)

print fullStamp() + " Triggering EARLY SYSTOLIC HEART MURMUR OVERLAY"
time.sleep(1)
#fileByte = definitions.ESMSYN
fileByte = definitions.KOROT
startBlending(rfObject,fileByte)

tracking_stop_time = 40
print fullStamp() + " Playback for %.03f seconds" %tracking_stop_time
time.sleep(40)

print fullStamp() + " Stopping EARLY SYSTOLIC HEART MURMUR OVERLAY"
time.sleep(1)
stopBlending(rfObject)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeeBTPort(rfObject)
#portRelease('rfcomm', 0)

