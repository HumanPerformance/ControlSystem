
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

portNumber = 1
rfObject = createPort(portNumber, 115200, 20) 
dataRead(rfObject)

portRelease('rfcomm', 0)                                    
