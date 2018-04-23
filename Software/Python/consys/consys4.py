"""
consys4.py

Latest version of the control system execution software
            
Fluvio L. Lobo Fenoglietto 04/18/2018
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
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


# ==============================================
# Variables
# ==============================================

# ----------------------------------------------
# Devices
# ----------------------------------------------

otoscope_bt_address         = "00:06:66:83:89:6D"
ophthalmoscope_bt_address   = "00:06:66:80:8C:08"

"""
SOH             = chr(0x01)                                         # Start of Header
ENQ		= chr(0x05)                                         # Enquiry
ACK             = chr(0x06)                                         # Positive Acknowledgement
NAK             = chr(0x15)                                         # Negative Acknowledgement
"""

# ----------------------------------------------
# Timers
# ----------------------------------------------
executionTimeStamp  = fullStamp()
simDuration         = 40                            # seconds

# ==============================================
# Operation
# ==============================================

# Device connection 


print fullStamp() + " OPERATION "
print fullStamp() + " Begin device configuration "

# the following section must be changed to use the old .XML scheme ---- #
smarthandle_bt_address = ([otoscope_bt_address,
                           ophthalmoscope_bt_address])
# --------------------------------------------------------------------- #
port = 0
baud = 115200
timeout = 1
notReady = True

print fullStamp() + " Connecting to panel devices "

N_smarthandles = 1
smarthandle_bt_object = []
for i in range(0, N_smarthandles):
    smarthandle_bt_object.append( createBTPort( smarthandle_bt_address[i], 1 ) )            # Connecting to bluetooth handle
    startDataStream( smarthandle_bt_object[i], 20, '\n' )                                   # Starting data streaming

"""
try:
    smartholder_usb_object  = createUSBPort( port, baud, timeout )
except:
    smartholder_usb_object  = createACMPort( port, baud, timeout )

if smartholder_usb_object.is_open:
    pass
else:
    smartholder_usb_object.open()

while( notReady ):                                                  # Loop until we receive SOH
    inData = smartholder_usb_object.read( size=1 )                                      # ...
    if( inData == SOH ):                                            # ...
        print( "{} [INFO] SOH Received".format( fullStamp() ) )     # [INFO] Status update
        break                                                       # ...

time.sleep(0.50)                                                    # Sleep for stability!


while( notReady ):                                                  # Loop until we are ready to start simulation
    
    inData = "{}".format( smartholder_usb_object.readline() )                           # Read until timeout is reached
    if( inData == '' ):                                             # Skip empty lines
        pass                                                        # ...

    else:                                                           # Else, read incoming data
        split_line = inData.split()                               # Split line contents

        formatted = ( "{} {} {}".format( fullStamp(), split_line[1], split_line[2] ) )     # Construct string
        print( formatted.strip('\n') )                              # [INFO] Status update

        if( split_line[1] == '1:' and split_line[2] == '0' ):                                 # If device is not on holder
            print( "Device ready for simulation scenario" )         # ...
            break                                                   # Break out of loop!
"""
# triggering device
# startDataStream( smarthandle_bt_object, 20, '\n' )


# data collection
simStartTime        = time.time()
simCurrentTime      = 0                             # seconds
simStopTime         = simDuration                   # seconds
simStopOne          = simDuration/2.0
simStopTwo          = simDuration

dataStream          = []
dataStreamOne       = []
dataStreamTwo       = []

while( simCurrentTime < simStopOne):

    dataStreamOne.append( ["%.02f" %simCurrentTime, readDataStream( smarthandle_bt_object[0], '\n' )] )

    simCurrentTime = time.time() - simStartTime

#while( (simCurrentTime > simStopOne) and (simCurrentTime < simStopTwo)):

#    dataStreamTwo.append( ["%.02f" %simCurrentTime, readDataStream( smarthandle_bt_object[1], '\n' )] )

#    simCurrentTime = time.time() - simStartTime

for i in range(0, N_smarthandles):
    time.sleep(0.50)
    stopDataStream( smarthandle_bt_object[i], 20, '\n' )                                    # Stop streaming data
    smarthandle_bt_object[i].close()                                                        # Closing bluetooth port
    
#print dataStream


# ==============================================
# Output
# ==============================================

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

otoscope_output_file        = "oto.txt"
ophthalmoscope_output_file  = "ophtho.txt"

N_lines_one = len( dataStreamOne )
N_lines_two = len( dataStreamTwo )

for i in range(0, N_lines_one):
    if( i == 0 ):
        with open(otoscope_output_file, 'a') as dataFile:
            dataFile.write( fullStamp() + " Smart Handle = " + "otoscope" + '\n' )
            dataFile.write( fullStamp() + " Bluetooth Address = " + otoscope_bt_address + '\n')
    with open(otoscope_output_file, 'a') as dataFile:
        dataFile.write( dataStreamOne[i][0] + "," + dataStreamOne[i][1] + '\n' )

for i in range(0, N_lines_two):
    if( i == 0 ):
        with open(ophthalmoscope_output_file, 'a') as dataFile:
            dataFile.write( fullStamp() + " Smart Handle = " + "ophthalmoscope" + '\n' )
            dataFile.write( fullStamp() + " Bluetooth Address = " + ophthalmoscope_bt_address + '\n')
    with open(ophthalmoscope_output_file, 'a') as dataFile:
        dataFile.write( dataStreamTwo[i][0] + "," + dataStreamTwo[i][1] + '\n' )
