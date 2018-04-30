"""
status4.3.py

Script dedicated to test the availabiltiy of devices associated with the panel
in question
            
Fluvio L. Lobo Fenoglietto 04/29/2018
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
shan    = "smarthandle"
shol    = "smartholder"
stet    = "stethoscope"
homeDir, pythonDir, consDir = definePaths(cons)
homeDir, pythonDir, shanDir = definePaths(shan)
homeDir, pythonDir, sholDir = definePaths(shol)
homeDir, pythonDir, stetDir = definePaths(stet)

response = addPaths(pythonDir)
response = addPaths(consDir)
response = addPaths(shanDir)
response = addPaths(sholDir)
response = addPaths(stetDir)

from    timeStamp                   import fullStamp
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *


# ========================================================================================= #
# Variables
# ========================================================================================= #

# ----------------------------------------------
# Devices
# ----------------------------------------------
smarthandle_name            = (["Otoscope",
                                "Ophthalmoscope"])

otoscope_bt_address         = "00:06:66:83:89:6D"
ophthalmoscope_bt_address   = "00:06:66:80:8C:08"

smarthandle_bt_address      = ([otoscope_bt_address,
                                ophthalmoscope_bt_address])


SOH             			= chr(0x01)                                         # Start of Header
ENQ					= chr(0x05)                                         # Enquiry
ACK             			= chr(0x06)                                         # Positive Acknowledgement
NAK             			= chr(0x15)                                         # Negative Acknowledgement


# ----------------------------------------------
# Timers
# ----------------------------------------------
executionTimeStamp  = fullStamp()

# ========================================================================================= #
# Operation
# ========================================================================================= #

# ----------------------------------------------------------------------------------------- #
# Device Configuration, Connection and Activation
# ----------------------------------------------------------------------------------------- #
print fullStamp() + " OPERATION "
print fullStamp() + " Begin device configuration "

port = 0
baud = 115200
timeout = 1
notReady = True

print( fullStamp() + " Connecting to panel devices " )
print( fullStamp() + " Connecting to smart handles " )
N_smarthandles = 2
smarthandle_bt_object = []
for i in range(0, N_smarthandles):

    try:
        smarthandle_bt_object.append( createBTPort( smarthandle_bt_address[i], 1 ) )            # Connecting to bluetooth handle
    
    startDataStream( smarthandle_bt_object[i], 20, '\n' )                                   # Starting data streaming

print( fullStamp() + " Connecting to smart holders " )

try:
    smartholder_usb_object  = createUSBPort( port, baud, timeout )                          # test USB vs ACM port issue
except:
    smartholder_usb_object  = createACMPort( port, baud, timeout )

if smartholder_usb_object.is_open:
    pass
else:
    smartholder_usb_object.open()

while( notReady ):                                                                          # Loop until we receive SOH
    inData = smartholder_usb_object.read( size=1 )                                          # ...
    if( inData == SOH ):                                                                    # ...
        #print( "{} [INFO] SOH Received".format( fullStamp() ) )                             # [INFO] Status update
        break                                                                               # ...

time.sleep(0.50)                                                                            # Sleep for stability!

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #
print( fullStamp() + " Disconnecting devices " )
print( fullStamp() + " Disconnecting bluetooth devices " )
for i in range(0, N_smarthandles):
    time.sleep(0.50)
    stopDataStream( smarthandle_bt_object[i], 20, '\n' )                                    # Stop streaming data
    smarthandle_bt_object[i].close()                                                        # Closing bluetooth port

print( fullStamp() + " Disconnecting usb devices " )
if( smartholder_usb_object.is_open ):
    smartholder_usb_object.close()

# ========================================================================================= #
# Output
# ========================================================================================= #
print( fullStamp() + " Writing data to file " )

outDir = consDir + "output/"
if( path.exists( outDir ) == False ):
    print( fullStamp() + " Output directory not present " )
    print( fullStamp() + " Generating output directory " )
    makedirs( outDir )
else:
    print( fullStamp() + " Found output directory " )

stampedDir = outDir + fullStamp() + "/"
if( path.exists( stampedDir ) == False ):
    print( fullStamp() + " Time-stamped directory not present " )
    print( fullStamp() + " Generating time-stamped directory " )
    makedirs( stampedDir )
else:
    print( fullStamp() + " Found time-stamped directory " )

# ----------------------------------------------------------------------------------------- #
# END
# ----------------------------------------------------------------------------------------- #
print( fullStamp() + " Program completed " )
