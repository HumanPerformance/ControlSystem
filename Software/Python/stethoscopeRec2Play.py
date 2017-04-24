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
portNumber = 0
#deviceBTAddress = "00:06:66:8C:D3:F6"
deviceBTAddress = "00:06:66:86:60:02"
#deviceBTAddress = "00:06:66:86:77:09"
baudrate = 115200
attempts = 5

rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject,attempts)

print fullStamp() + " Triggering Heart Rate Tracking"
time.sleep(1)
startRecording(rfObject,attempts)

print fullStamp() + " Openning Stethoscope Serial Port"
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()

tracking_start_time = time.time()
tracking_stop_time = 20
tracking_current_time = 0
dataStream = []
print fullStamp() + " Recording and Tracking Heart Rate for %.03f seconds" %tracking_stop_time
while tracking_current_time < tracking_stop_time:
    
    dataStream.append(["%.02f" %tracking_current_time,
                       rfObject.readline()[:-1]])
    
    tracking_current_time = time.time() - tracking_start_time
    print fullStamp() + " Current Simulation Time = %.03f" %tracking_current_time

print fullStamp() + " Closing Stethoscope Serial Port"
time.sleep(1)
rfObject.close()

print fullStamp() + " Stopping Device Recording"
time.sleep(1)
stopRecording(rfObject,attempts)

print fullStamp() + " Start Blending Recorded File"
fileByte = definitions.BRECORD
startBlending(rfObject,fileByte,attempts)

tracking_stop_time = 20
print fullStamp() + " Blend for %.03f seconds" %tracking_stop_time
time.sleep(20)

print fullStamp() + " Stop Blending Recorded File"
stopBlending(rfObject,attempts)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
portRelease('rfcomm', 0)

