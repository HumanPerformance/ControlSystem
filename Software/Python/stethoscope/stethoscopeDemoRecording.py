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
import  stethoscopeDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *
from    stethoscopeProtocol          import *

# Operation


print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 0
deviceBTAddress = "00:06:66:8C:9C:2E"
baudrate = 115200
attempts = 5
rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject,attempts)

print fullStamp() + " Triggering Heart Rate Tracking"
time.sleep(1)
startRecording(rfObject,attempts)

time.sleep(40)

print fullStamp() + " Stopping Device Recording"
time.sleep(1)
stopRecording(rfObject,attempts)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
portRelease('rfcomm', 0)

