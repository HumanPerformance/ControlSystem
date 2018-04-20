"""
consys4P3.py

Version to be executed on Python 3+
Latest version of the control system execution software
            
Fluvio L. Lobo Fenoglietto 04/19/2018
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
shan    = "smarthandle"
shol    = "smartholder"
stet    = "stethoscope"
homeDir, pythonDir, shanDir = definePaths(shan)
homeDir, pythonDir, sholDir = definePaths(shol)
homeDir, pythonDir, stetDir = definePaths(stet)

response = addPaths(pythonDir)
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
# Timers
# ----------------------------------------------
executionTimeStamp  = fullStamp()
simDuration         = 20                            # seconds

# ==============================================
# Operation
# ==============================================

# Device connection 


print( fullStamp() + " OPERATION " )
print( fullStamp() + " Begin device configuration " )

# the following section must be changed to use the old .XML scheme ---- #
smarthandle_bt_address = (["00:06:66:83:89:5F",
                           "00:06:66:83:89:5F"])
# --------------------------------------------------------------------- #

print( fullStamp() + " Connecting to panel devices " )

smarthandle_bt_object   = createBTPort( smarthandle_bt_address[0], 1 )

try:
    smartholder_usb_object  = createUSBPort( 0, 115200, 1 )
except:
    smartholder_usb_object  = createACMPort( 0, 115200, 1 )

if( smartholder_usb_object.is_open() ):
    pass
else:
    smartholder_usb_object.open()

inData = smartholder_usb_object.read(1)
print( inData )

# triggering device
startDataStream( smarthandle_bt_object, 20 )


# data collection
simStartTime        = time.time()
simCurrentTime      = 0                             # seconds
simStopTime         = simDuration                   # seconds

dataStream          = []

while( simCurrentTime < simStopTime ):

    dataStream.append( ["%.02f" %simCurrentTime, readDataStream( smarthandle_bt_object, '\n' )] )

    simCurrentTime = time.time() - simStartTime

stopDataStream( smarthandle_bt_object, 20 )

print( dataStream )

smarthandle_bt_object.close()



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
