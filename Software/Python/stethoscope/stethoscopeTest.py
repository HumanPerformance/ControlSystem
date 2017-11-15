
# Import
import sys
import os
import serial
import stethoscopeDefinitions       as     definitions
from   os.path                      import expanduser
from   bluetoothProtocol_teensy32   import *
from   stethoscopeProtocol          import *

# =========
# OPERATION
# =========

deviceName = "SS"
portNumber = 0
deviceBTAddress = "00:06:66:7D:99:D9"
baudrate = 115200
attempts = 5
rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)

time.sleep(2)
statusEnquiry(rfObject,attempts)

time.sleep(2)
bogusFun(rfObject,attempts)

time.sleep(10)

time.sleep(2)
bogusFun2(rfObject,attempts)

"""
time.sleep(2)
sdCardCheck(rfObject,attempts)

time.sleep(2)
startTrackingMicStream(rfObject,attempts)

time.sleep(5)

time.sleep(2)
stopTrackingMicStream(rfObject,attempts)
"""

portRelease('rfcomm', 0)

