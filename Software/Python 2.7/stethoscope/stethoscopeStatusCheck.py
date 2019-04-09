"""
Stethoscope Demo :: Status Check

The following code was built to test/torubleshoot/demo the status check function

Fluvio L Lobo Fenoglietto
05/08/2017
"""

# ========================================================================================= #
# Import Libraries and/or Modules
# ========================================================================================= #
# Python modules
import  sys
import  os
import  serial
import  time
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs

# PD3D modules
from    configurationProtocol       import *
cons    = "consys"
stet    = "stethoscope"
homeDir, pythonDir, consDir = definePaths( cons )
homeDir, pythonDir, stetDir = definePaths( stet )
print( consDir )
print( stetDir )
response = addPaths(pythonDir)
response = addPaths(consDir)
response = addPaths(stetDir)

import  stethoscopeDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *
from    stethoscopeProtocol          import *

# Demo Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 1  # cannot use port 0 for sockets
deviceBTAddress = "00:06:66:D0:E4:37"
baudrate = 115200
attempts = 5
#rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)
rfObject = createBTPort(deviceBTAddress,portNumber)
#rfObject.close()

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry( rfObject )

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
systemCheck( rfObject )

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeBTPort( rfObject )
#portRelease('rfcomm', 0)

