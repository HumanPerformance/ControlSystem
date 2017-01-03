
# Import
import sys
import os
from os.path import expanduser
import serial
from configurationProtocol import *
from usbProtocol import *
from smartHolderProtocol import *

# =========
# OPERATION
# =========

portNumber = 0
rfObject = createPort(portNumber, 115200, None)
print "Enter command: "
rfObject.write(raw_input())
time.sleep(1)
dataRead_interrupt(rfObject)
#dataRead(rfObject)
