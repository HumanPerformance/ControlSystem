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
simDuration         = 20                            # seconds

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

N_smarthandles = 2
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

dataStream          = []

while simCurrentTime < simStopTime:

    dataStream.append( ["%.02f" %simCurrentTime, readDataStream( smarthandle_bt_object[1], '\n' )] )

    simCurrentTime = time.time() - simStartTime

for i in range(0, N_smarthandles):
    stopDataStream( smarthandle_bt_object[i], 20, '\n' )                                    # Stop streaming data
    smarthandle_bt_object[i].close()                                                        # Closing bluetooth port
    
print dataStream





"""
rfObject = createPortS(deviceTypes[1],1,deviceAddresses[1],115200,5)

# triggering device
time.sleep(1)
triggerDevice2(rfObject,"SH")

# openning device
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()



configStartTime = time.time()
configCurrentTime = 0
configStopTime = 20 #timers[0]
configLoopCounter = 0
print fullStamp() + " Starting Configuration Loop, time = " + str(configStopTime) + " seconds"
while configCurrentTime < configStopTime:

    # Connect to listed devices...
    if configLoopCounter == 0:
        print fullStamp() + " Connecting smart devices"
        rfObject = createPortS(deviceTypes[0], deviceAddresses[0], 115200, 5)

        time.sleep(1)
        print fullStamp() + " Triggering smart devices"
        triggerDevice2(rfObject,deviceTypes[0])
        
        print fullStamp() + " Opening smart device communication"
        time.sleep(1)
        if rfObject.isOpen() == False:
            rfObject.open()
    
    configCurrentTime = time.time() - configStartTime
    configLoopCounter = configLoopCounter + 1

# End of Configuration Loop
"""
"""
# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

simStartTime = time.time()
simCurrentTime = 0
simStopTime = 30
# simLoopCounter = 0
dataStream = []
print fullStamp() + " Starting Simulation Loop, time = " + str(simStopTime) + " seconds"

try:
    while simCurrentTime < simStopTime:

        # Handles
        dataStream.append("%.02F"%simCurrentTime + "," + rfObject.readline()[:-1])

        simCurrentTime = time.time() - simStartTime
        print fullStamp() + " Current Simulation Time = " + str(simCurrentTime)
        # simLoopCounter = simLoopCounter + 1;

        # End of Simulatio Loop
        
except Exception as instance:
    print fullStamp() + " Exception or Error Caught"
    print fullStamp() + " Error Type " + str(type(instance))
    print fullStamp() + " Error Arguments " + str(instance.args)
    print fullStamp() + " Closing Open Ports"
    time.sleep(1)
    if rfObject.isOpen() == True:
        rfObject.close()

# print dataStream

time.sleep(0.25)
if rfObject.isOpen() == True:
    rfObject.close()
time.sleep(0.25)
stopDevice2(rfObject,deviceTypes[0])

"""
