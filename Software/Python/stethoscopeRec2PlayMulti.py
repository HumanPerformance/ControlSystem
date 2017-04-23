"""
Stethoscope Demo :: Blending

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
04/22/2017
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


print fullStamp() + " Connecting to the Stethoscopes"
deviceName = "SS"
deviceBTAddress = ["00:06:66:86:77:09","00:06:66:86:60:02","00:06:66:8C:D3:F6"]
baudrate = 115200
attempts = 5

rfObject = []
for i in range(0,len(deviceBTAddress)):
    rfObject.append(createPort(deviceName,i,deviceBTAddress[i],baudrate,attempts))

print fullStamp() + " Enquiring Stethoscope Status"

for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    statusEnquiry(rfObject[i],attempts)


print fullStamp() + " Start Recording"
for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    startRecording(rfObject[i],attempts)

tracking_stop_time = 20
print fullStamp() + " Record for %.03f seconds" %tracking_stop_time
time.sleep(20)

print fullStamp() + " Closing Stethoscopes Serial Port"
for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    rfObject[i].close()

print fullStamp() + " Stop Recording"
for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    stopRecording(rfObject[i],attempts)


print fullStamp() + " Start Blending Recorded File"
fileByte = definitions.BRECORD
for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    startBlending(rfObject[i],fileByte,attempts)

tracking_stop_time = 20
print fullStamp() + " Blend for %.03f seconds" %tracking_stop_time
time.sleep(20)

print fullStamp() + " Stop Blending Recorded File"
for i in range(2,len(deviceBTAddress)):
    time.sleep(1)
    stopBlending(rfObject[i],attempts)

for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    portRelease('rfcomm', i)

