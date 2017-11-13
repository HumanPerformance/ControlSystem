"""
Stethoscope Demo :: Tracking

The following code was built to show the heart-rate tracking capabilities of the stethoscope

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

print fullStamp() + " Triggering Heart Rate Monitoring"
time.sleep(1)
startHBMonitoring(rfObject,attempts)

tracking_stop_time = 40
print fullStamp() + " Monitoring for %.03f seconds" %tracking_stop_time
time.sleep(40)

print fullStamp() + " Stopping Device Streaming"
time.sleep(1)
stopHBMonitoring(rfObject,attempts)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
portRelease('rfcomm', 0)

