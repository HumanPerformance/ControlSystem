"""
Stethoscope Demo :: Blending

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
01/31/2017
"""

# Import Modules, Libraries and/or Functions
import  sys
import  os
import  serial
import  time
from    configurationProtocol    import *
device = "stethoscope"
homeDir, pythonDir, deviceDir = definePaths(device)
response = addPaths(pythonDir)

##import  stethoscopeDefinitions       as     definitions
##from    os.path                      import expanduser
from    stethoscopeProtocol          import *
from    bluetoothProtocol_teensy32   import *

# Demo Operation
print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 1  # cannot use port 0 for sockets
deviceBTAddress = "00:06:66:D0:C9:AE"

rfObject = createBTPort(deviceBTAddress, portNumber)

SOH     = chr(0x01)
EOT     = chr(0x04)
PLAY    = chr(0x21)

print fullStamp() + " Starting recording..." ,
time.sleep(1)
rfObject.send( SOH )
print( "DONE!" )

stop_time = 20
switch_time = 15


print fullStamp() + " RECORDING AORTIC %.03f seconds" %stop_time
time.sleep( 2.5 )
startTime = time.time()
while( time.time() - startTime < stop_time ):
    print( "{:3.3}".format(time.time() - startTime) )

##print fullStamp() + " %.03f seconds to switch to PULMONARY" %switch_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < switch_time ):
##    print( "{:3.3}".format(time.time() - startTime) )
##
##
##print fullStamp() + " RECORDING PULMONARY %.03f seconds" %stop_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < stop_time ):
##    print( "{:3.3}".format(time.time() - startTime) )
##
##print fullStamp() + " %.03f seconds to switch to MITRAL" %switch_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < switch_time ):
##    print( "{:3.3}".format(time.time() - startTime) )
##
##print fullStamp() + " RECORDING MITRAL %.03f seconds" %stop_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < stop_time ):
##    print( "{:3.3}".format(time.time() - startTime) )
##print fullStamp() + " %.03f seconds to switch to TRICUSPID" %switch_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < switch_time ):
##    print( "{:3.3}".format(time.time() - startTime) )
##
##print fullStamp() + " RECORDING TRICUSPID %.03f seconds" %stop_time
##time.sleep( 2.5 )
##startTime = time.time()
##while( time.time() - startTime < stop_time ):
##    print( "{:3.3}".format(time.time() - startTime) )

print fullStamp() + " Stopping recording..." ,
time.sleep( 1 )
rfObject.send( EOT )
print( "DONE!" )

print fullStamp() + " Releasing Serial Port"
time.sleep( 1 )
closeBTPort( rfObject )
