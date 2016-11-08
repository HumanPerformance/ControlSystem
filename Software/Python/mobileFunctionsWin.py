"""
mobileFunctions.py

This module has been created to contain all of the functions to be called by the mobile script

Fluvio L Lobo Fenoglietto
07/11/2016
"""

# Import Modules
from timeStamp import fullStamp
import protocolDefinitions
from bluetoothProtocolWin import findDevices
from bluetoothProtocolWin import findSmartDevice
from bluetoothProtocolWin import nextAvailablePort
from bluetoothProtocolWin import createPort


# Functions

# Find Stethoscope
#   Function designed to find a smart stethoscope in range
#   This function coordinates several functions from various imported protocols
#   Input   ::  None
#   Output  ::  {array/list}
def findStethoscope():
    print fullStamp() + " findStethoscope()"
    global smartDeviceName
    availableDeviceNames, availableDeviceBTAddresses = findDevices()
    smartDeviceName, smartDeviceBTAddress = findSmartDevice("RNBT-76E6",availableDeviceNames, availableDeviceBTAddresses)
    portName = nextAvailablePort()
    rfObject = createPort(portName,smartDeviceName,smartDeviceBTAddress)
    return smartDeviceName
