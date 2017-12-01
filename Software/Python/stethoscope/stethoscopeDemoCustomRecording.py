"""
Stethoscope Demo :: Custom Recording

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
deviceBTAddress = "00:06:66:8C:9C:2E"
baudrate = 115200
attempts = 5
rfObject = createBTPort(deviceBTAddress,portNumber)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject)

print fullStamp() + " Sending String "
recString = "SP02HHS"
startCustomRecording(rfObject,recString)

time.sleep(20)

print fullStamp() + " Stopping Device Recording"
stopRecording(rfObject)

print fullStamp() + " Checking SD Card"
systemCheck(rfObject)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeBTPort(rfObject)

