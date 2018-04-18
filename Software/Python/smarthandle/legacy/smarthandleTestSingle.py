"""
smarthandleTest.py

The following script has been created to test/debug functions specific to the smart handle prototype

Fluvio L Lobo Fenoglietto
11/21/2016
"""

# Import
import time
from timeStamp import *
from bluetoothProtocol import *
from smarthandleProtocol import *

# Operation
executionTimeStamp = fullStamp()
testDir = "/home/pi/Desktop/test"
deviceNames = ["SH","SH"]
deviceBTAddresses = ["00:06:66:80:8C:BE","00:06:66:80:8C:A9"]
<<<<<<< HEAD
rfObject = createPort2(deviceNames[1], deviceBTAddresses[1], 115200, 5, 5)
=======
rfObject = createPort2(deviceNames[0], deviceBTAddresses[0], 115200, 5, 5)
>>>>>>> smartHolder

print fullStamp() + " Triggering Smart Handle"
time.sleep(1)
triggerDevice2(rfObject,deviceNames[1])

print fullStamp() + " Openning Smart Handle Serial Port"
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()
time.sleep(1)

print fullStamp() + " Starting Data Collection Loop"
startTime = time.time()
currentTime = 0
stopTime = 90
dataStream = []
while currentTime < stopTime:

    dataStream.append("TIM," + str(currentTime) + "," + rfObject.readline()[:-1])

    currentTime = time.time() - startTime

print fullStamp() + " Closing Smart Handle Serial Port"
time.sleep(1)
if rfObject.isOpen() == True:
    rfObject.close()
time.sleep(1)
print fullStamp() + " Stopping Smart Handle"
<<<<<<< HEAD
stopDevice2(rfObject,deviceNames[1])
=======
stopDevice2(rfObject,deviceNames[0])
>>>>>>> smartHolder

print fullStamp() + " Saving Output Text File"
Nlines = len(dataStream)
for i in range(0,Nlines):
    dataWrite(executionTimeStamp, currentTime, testDir, deviceNames[0], dataStream[i])

print fullStamp() + " Program completed"

