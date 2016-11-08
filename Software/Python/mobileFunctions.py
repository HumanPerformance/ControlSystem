"""
mobileFunctions.py

This module has been created to contain all of the functions to be called by the mobile script

Fluvio L Lobo Fenoglietto
07/11/2016
"""

# Import Modules
from timeStamp import fullStamp
import protocolDefinitions
from bluetoothProtocol import findDevices
from bluetoothProtocol import findSmartDevices
from bluetoothProtocol import createPorts
from bluetoothProtocol import portRelease
from stethoscopeProtocol import deviceID
from stethoscopeProtocol import sdCardCheck


# Functions

# Find Stethoscope
#   Function designed to find a smart stethoscope in range
#   This function coordinates several functions from various imported protocols
#   Input   ::  None
#   Output  ::  {array/list}
def findStethoscope():
    print fullStamp() + " findStethoscope()"
    availableDeviceNames, availableDeviceBTAddresses = findDevices()
    smartDeviceNames, smartDeviceBTAddresses = findSmartDevices("RNBT",availableDeviceNames, availableDeviceBTAddresses)
    #rfObject = createPort(smartDeviceNames, smartDeviceBTAddresses)
    #deviceID(rfObject[0])
    #sdCardCheck(rfObject)
    #portRelease('rfcomm',0)
