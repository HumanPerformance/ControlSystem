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
deviceName = "oto"                                                                             # Hard-coded device name
deviceBTAddress = "00:06:66:80:8C:BE"                                                                  # Hard-code device bluetooth address
rfObject = createPort(deviceName, deviceBTAddress, 115200, 5, 5)

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
