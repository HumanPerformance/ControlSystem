"""
Stethoscope Demo :: Blending

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
#deviceBTAddress = "00:06:66:7D:99:D9"
deviceBTAddress = "00:06:66:86:77:09"
baudrate = 115200
attempts = 5
rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject,attempts)

print fullStamp() + " Triggering EARLY SYSTOLIC HEART MURMUR OVERLAY"
time.sleep(1)
#earlyHMBlending(rfObject, attempts)
fileByte = definitions.EDHMUR
#fileByte = definitions.PEJECT
#fileByte = definitions.ASYSL
#earlyHMBlending(rfObject, attempts)
startBlending(rfObject,fileByte,attempts)

tracking_stop_time = 20
print fullStamp() + " Playback for %.03f seconds" %tracking_stop_time
time.sleep(20)

print fullStamp() + " Stopping EARLY SYSTOLIC HEART MURMUR OVERLAY"
time.sleep(1)
stopBlending(rfObject,attempts)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
portRelease('rfcomm', 0)

