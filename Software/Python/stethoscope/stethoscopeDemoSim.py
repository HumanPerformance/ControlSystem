"""
Stethoscope Demo :: TSimulation

Fluvio L Lobo Fenoglietto
--2018
"""

# Import
import  sys
import  os
import  serial
import  time

from    configurationProtocol    import *
device = "stethoscope"
homeDir, pythonDir, deviceDir = definePaths(device)
response = addPaths(pythonDir)

import  stethoscopeDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *
from    stethoscopeProtocol          import *

# Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 1
deviceBTAddress = "00:06:66:D0:E4:37"
baudrate = 115200
attempts = 5
rfObject = createBTPort(deviceBTAddress,portNumber)

#
# Simulation Steps
#

# Device Preparation
## SD Card Check
print( fullStamp() + " Checking SD Card" )
time.sleep( 0.50 )
systemCheck( rfObject )

## Status Enquiry
print( fullStamp() + " Enquiring Stethoscope Status" )
time.sleep( 0.50 )
statusEnquiry( rfObject )

## Set Recording mode
print( fullStamp() + " Setting Stethoscope Recording Mode " )
time.sleep( 0.50 )
recMode = 0
setRecordingMode( rfObject, recMode )

## Generate Recording String
print( fullStamp() + " Generating Recording String " )
randString = genRandString( 4 )
print( fullStamp() + " Generated : " + randString )

## Parse Rand. Generated Recording String
print( fullStamp() + " Parsing Recording String " )
parseString( rfObject, randString )

# Start Simulation
print fullStamp() + " Triggering Simulation"
time.sleep(1)
startSimulation( rfObject )

## Simulating
tracking_stop_time = 20
print fullStamp() + " Monitoring for %.03f seconds" %tracking_stop_time
time.sleep(20)

## Stopping Simulation
print( fullStamp() + " Stopping Simulation" )
stopSimulation( rfObject );

## SD Card Check
print( fullStamp() + " Checking SD Card" )
time.sleep( 5 )
systemCheck( rfObject )

# Closing Communication
print( fullStamp() + " Releasing Serial Port" )
time.sleep( 0.50 )
closeBTPort(rfObject)


