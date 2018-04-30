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

executionTimeStamp  = fullStamp()

# ========================================================================================= #
# Functions
# ========================================================================================= #
def create_status_directories( consDir, executionTimeStamp ):
    print( fullStamp() + " Writting status to file " )

    statusDir = consDir + "status/"
    if( path.exists( statusDir ) == False ):
        print( fullStamp() + " Status directory not present " )
        print( fullStamp() + " Generating status directory " )
        makedirs( statusDir )
    else:
        print( fullStamp() + " Found status directory " )

    stampedDir = statusDir + executionTimeStamp + "/"
    if( path.exists( stampedDir ) == False ):
        print( fullStamp() + " Time-stamped directory not present " )
        print( fullStamp() + " Generating time-stamped directory " )
        makedirs( stampedDir )
    else:
        print( fullStamp() + " Found time-stamped directory " )

    return statusDir, stampedDir

def write_status_to_file( status_filename, message ):
    with open( status_filename, 'a' ) as dataFile:
        dataFile.write( fullStamp() + " " + message )

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


SOH             	    = chr(0x01)                                         # Start of Header
ENQ			    = chr(0x05)                                         # Enquiry
ACK             	    = chr(0x06)                                         # Positive Acknowledgement
NAK             	    = chr(0x15)                                         # Negative Acknowledgement

# ========================================================================================= #
# Operation
# ========================================================================================= #

# ----------------------------------------------------------------------------------------- #
# Device Configuration, Connection and Activation
# ----------------------------------------------------------------------------------------- #
print fullStamp() + " OPERATION: System Status Check "
print fullStamp() + " Begin device configuration "

port = 0
baud = 115200
timeout = 1
notReady = True

# connecting to panel devices ------------------------------------------------------------- #
print( fullStamp() + " Connecting to panel devices " )

# connecting to smart handles ------------------------------------------------------------- #
print( fullStamp() + " Connecting to smart handles " )
N_smarthandles = 2
smarthandle_bt_object = []
for i in range(0, N_smarthandles):

    try:
        smarthandle_bt_object.append( createBTPort( smarthandle_bt_address[i], 1 ) )        # Connecting to bluetooth handle
    except bluetooth.btcommon.BluetoothError as bluetoothError:
        print( fullStamp() + " Stethoscope unavailable " )
        statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
        status_filename = stampedDir + "log.txt"
        write_status_to_file( status_filename, serialError )
        sys.exit( fullStamp() + " ERROR: Device missing " )

# connecting to smart holders ------------------------------------------------------------- #
print( fullStamp() + " Connecting to smart holders " )

try:
    smartholder_usb_object  = createUSBPort( port, baud, timeout )                          # test USB vs ACM port issue
except serial.serialutil.SerialException as serialError:
    print( fullStamp() + " Cannot find serial COM Port, testing ACM Port... " )
    try:
        smartholder_usb_object  = createACMPort( port, baud, timeout )
    except serial.serialutil.SerialException as serialError:
        print( fullStamp() + " Smart Holder unavailable " )
        statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
        status_filename = stampedDir + "log.txt"
        write_status_to_file( status_filename, serialError )
        sys.exit( fullStamp() + " ERROR: Device missing " )

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
    smarthandle_bt_object[i].close()                                                        # Closing bluetooth port

print( fullStamp() + " Disconnecting usb devices " )
if( smartholder_usb_object.is_open ):
    smartholder_usb_object.close()

# ----------------------------------------------------------------------------------------- #
# END
# ----------------------------------------------------------------------------------------- #
print( fullStamp() + " Status check completed successfully... Ready to Go! " )
statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
status_filename = stampedDir + "log.txt"
write_status_to_file( status_filename, " System CHECKS! " )
