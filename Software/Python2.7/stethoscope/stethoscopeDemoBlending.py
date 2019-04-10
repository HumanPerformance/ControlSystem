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

from  stethoscopeDefinitions          import *
from    os.path                         import expanduser
#from    bluetoothProtocol_teensy32   import *
from    stethoscopeBTProtocol           import *
from    stethoscopeProtocol             import *

# Demo Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 1  # cannot use port 0 for sockets
#deviceBTAddress = "00:06:66:D0:C9:60"
deviceBTAddress = "00:06:66:8C:D3:C8"
baudrate = 115200
attempts = 5
#rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)
rfObject = createBTPort(deviceBTAddress,portNumber)
#rfObject.close()


print fullStamp() + " Enquiring Stethoscope Status"
#rfObject.open()
time.sleep(1)
statusEnquiry(rfObject)
time.sleep(1)
#rfObject.close()

print fullStamp() + " Triggering EARLY SYSTOLIC HEART MURMUR OVERLAY"
time.sleep(1)

#blendFileName = 'AORSTE'
blendFileName = 'S4GALL'
matchIndex = blendByteMatching( blendFileName, blendFiles )
fileByte = chr( blendInt[matchIndex] )

startBlending(rfObject,fileByte)

tracking_stop_time = 10
print fullStamp() + " Playback for %.03f seconds" %tracking_stop_time
time.sleep(10)

print fullStamp() + " Stopping blending"
time.sleep(1)
stopBlending(rfObject)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)

closeBTPort(rfObject)

