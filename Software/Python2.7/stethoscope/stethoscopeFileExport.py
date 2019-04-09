"""
Stethoscope Demo :: Blending

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
01/31/2017
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
#rfObject.open()
time.sleep(1)
sendRaw(rfObject)

i = 0
inBytes = []
rfObject.settimeout(1)
while True:
#for i in range(0, 100):
    inBytes.append( rfObject.recv(1) )
    print( str(i) + ", " + inBytes[i].encode('hex') )
    if i > 3:
        #print( " check " )
        if inBytes[i] == "D":
            print( " hola " )
            if inBytes[i-1] == "N":
                print( " hola " )
                if inBytes[i-2] == "E":
                    print( " yes, hola " )
                    break
    i = i + 1


print fullStamp() + " Releasing Serial Port"
time.sleep(1)
closeBTPort(rfObject)
#portRelease('rfcomm', 0)

