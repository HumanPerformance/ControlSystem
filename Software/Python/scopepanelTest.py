"""
scopepanelTest.py

The following script has been created to test/debug functions specific to the scope panel prototype

Fluvio L Lobo Fenoglietto
11/21/2016
"""

# Import
import time
from timeStamp import *
from usbProtocol import *
from scopepanelProtocol import *

# Operation
executionTimeStamp = fullStamp()
deviceName = "scp"
usbObject = createPort(1,115200, 5)              # Make more robust function
startTime = time.time()                                                                                 # Start loop timer
currentTime = 0                                                                                         # 0 sec.
stopTime = 10                                                                                          # Stop time

triggerDevice(usbObject,deviceName,20)

while currentTime < stopTime:

        # Read data from device
        inString = dataRead(usbObject)

        # Write data from device
        dataWrite(executionTimeStamp, currentTime, outputFilePath, deviceName, inString)

        # Update time
        currentTime = time.time() - startTime
        # print currentTime

print "Program Concluded"

stopDevice(usbObject, deviceName, 20)
