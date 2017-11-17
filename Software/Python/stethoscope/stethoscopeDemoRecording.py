"""
Stethoscope Demo :: Recording & Tracking

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
01/31/2017
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
deviceBTAddress = "00:06:66:8C:9C:2E"
baudrate = 115200
attempts = 5
rfObject = createBTPort(deviceBTAddress,portNumber)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject)

print fullStamp() + " Triggering Heart Rate Tracking"
time.sleep(1)
startRecording(rfObject)

time.sleep(20)

print fullStamp() + " Stopping Device Recording"
time.sleep(1)
stopRecording(rfObject)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeBTPort(rfObject)

