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

executionTimeStamp = fullStamp()                                                                        # Program execution timestamp
deviceNames = ["SH","SH"]                                                                            # Hard-coded device name
deviceBTAddresses = ["00:06:66:80:8C:BE","00:06:66:80:8C:A9"]                                                                  # Hard-code device bluetooth address
rfObject = createPorts2(deviceNames, deviceBTAddresses, 115200, 5, 5)

time.sleep(1)
triggerDevices(rfObject,deviceNames)
time.sleep(1)

rfObject[1].open()
time.sleep(1)
rfObject[0].open()
time.sleep(1)
for i in range(0,20):
    print rfObject[1].readline(), rfObject[0].readline()
    #time.sleep(0.25)

rfObject[1].close()
rfObject[0].close()
time.sleep(1)
stopDevices(rfObject,deviceNames)

"""
startStreaming(rfObject)
time.sleep(2)
for i in range(0,20):
    readStream(rfObject)
time.sleep(5)
stopStreaming(rfObject)
portRelease('rfcomm',0)
"""


"""
#CSEC Demo Nov. 2016
triggerDevice(rfObject, deviceName, 20)
startTime = time.time()                                                                                 # Start loop timer
currentTime = 0                                                                                         # 0 sec.
stopTime = 20                                                                                           # Stop time



while currentTime < stopTime:

        # Read data from device
        inString = dataRead(rfObject)

        # Write data from device
        dataWrite(executionTimeStamp, currentTime, outputFilePath, deviceName, inString)

        # Update time
        currentTime = time.time() - startTime
        # print currentTime

print "Program Concluded"
stopDevice(rfObject, deviceName, 20)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection


#portRelease('rfcomm', 0)
"""
