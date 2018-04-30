"""
status4.3bpc.py

...
            
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
import  pexpect
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs
from    threading                   import Thread
from    Queue                       import Queue

# PD3D modules
from    configurationProtocol                   import *
cons    = "consys"
shan    = "smarthandle"
shol    = "smartholder"
stet    = "stethoscope"
bpcu    = "bloodpressurecuff"

homeDir, pythonDir, consDir = definePaths(cons)
homeDir, pythonDir, shanDir = definePaths(shan)
homeDir, pythonDir, sholDir = definePaths(shol)
homeDir, pythonDir, stetDir = definePaths(stet)
homeDir, pythonDir, bpcuDir = definePaths(bpcu)

response = addPaths(pythonDir)
response = addPaths(consDir)
response = addPaths(shanDir)
response = addPaths(sholDir)
response = addPaths(stetDir)
response = addPaths(bpcuDir)

from    timeStamp                   import fullStamp
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *
from    stethoscopeProtocol         import *


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
stethoscope_name        = "Stethoscope"
stethoscope_bt_address  = (["00:06:66:D0:E4:94"])


SOH             			= chr(0x01)                                         # Start of Header
ENQ					= chr(0x05)                                         # Enquiry
ACK             			= chr(0x06)                                         # Positive Acknowledgement
NAK             			= chr(0x15)                                         # Negative Acknowledgement


# ========================================================================================= #
# Operation
# ========================================================================================= #

# ----------------------------------------------------------------------------------------- #
# Device Configuration, Connection and Activation
# ----------------------------------------------------------------------------------------- #
print fullStamp() + " OPERATION: System Status Check "
print fullStamp() + " Begin device configuration "

# connecting to panel devices
print( fullStamp() + " Connecting to panel devices " )

# connecting to stethoscope --------------------------------------------------------------- #
print( fullStamp() + " Connecting to stethoscope " )
try:
    stethoscope_bt_object = createBTPort( stethoscope_bt_address[0], 1 )                        # using bluetooth protocol commands
except bluetooth.btcommon.BluetoothError as bluetoothError:
    print( fullStamp() + " Stethoscope unavailable " )
    statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
    status_filename = stampedDir + "log.txt"
    write_status_to_file( status_filename, serialError )
    sys.exit( fullStamp() + " ERROR: Device missing " )

# connecting to smart holders ------------------------------------------------------------- #
print( fullStamp() + " Connecting to smart holders " )
port = 0
baud = 115200
timeout = 1
notReady = True

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
        print( "{} [INFO] SOH Received".format( fullStamp() ) )                             # [INFO] Status update
        break                                                                               # ...

time.sleep(0.50)                                                                            # Sleep for stability!


# start blood pressure cuff and digital dial ---------------------------------------------- #
"""
print( fullStamp() + " Connecting to blood pressure cuff " )
q_pressure_meter = Queue( maxsize=0 )                                                   # Define queue
t_pressure_meter = Thread( target=readGauge, args=( True, q_pressure_meter, ) )# Define thread
t_pressure_meter.daemon = True
t_pressure_meter.start()                                                                # Start thread

pexpectChild = q_pressure_meter.get()
"""
# ----------------------------------------------------------------------------------------- #
# Data Gathering
# ----------------------------------------------------------------------------------------- #
# Variables
scenario            = 0                                                                     # scenario type

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #
#print( fullStamp() + " Closing blood pressure cuff connection " )
#pexpectChild.close()

print( fullStamp() + " Disconnecting bluetooth devices " )
if( scenario == 0 ):
    statusEnquiry( stethoscope_bt_object ) # replace with stop recording
elif( scenario == 1 ):
    statusEnquiry( stethoscope_bt_object ) # replace with stop recording and blending
elif( scenario == 2 ):
    statusEnquiry( stethoscope_bt_object )

stethoscope_bt_object.close()

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
print( fullStamp() + " " + "AOK" )
