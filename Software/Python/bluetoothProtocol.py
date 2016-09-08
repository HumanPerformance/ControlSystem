"""
bluetoothProtocol.py

The following module has been created to manage the bluetooth interface between the control system and the connected devices

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016


List of functions ::

X - Look for bluetooth device
X - Pair bluetooth device
X - Add paired device to the instrument list
X - Connect to paired device

"""

# Import Libraries and/or Modules
import os
import serial
from timeStamp import *

# Create RFComm Ports
#   This function creates radio-frquency (bluetooth) communication ports for specific devices, using their corresponding address
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"
def createRFPort(deviceName, deviceBTAddress):
    Ndevices = len(deviceName) # Determines the number of devices listed
    RFObject = [] # Create RF object variable/list (in case of multiple devices)
    for i in range(0,Ndevices):
        
        print fullStamp() + " Releasing RFCOMM" + str(i) # Pre-release of RFCOMM port
        portRelease("rfcomm",i)
        # Open RFCOMM port for device
        print fullStamp() + " Connecting device to RFCOMM" + str(i)
        os.system("sudo rfcomm bind /dev/rfcomm" + str(i) + " " + instrumentBTAddress[i])
        # Create Arduino RF-Serial Object
        rfcommPort = "/dev/rfcomm" + str(i)
        RFObj = serial.Serial(rfcommPort,115200) # Need error handle for the case in which the device is not available
        arduRFObj.append(RFObj)
        # Trigger data collection on instruments
        triggerRFInstrument(arduRFObj[i], instrumentNames[i])

    return arduRFObj

# Connect to paired device
#   Connects to the bluetooth devices specified by the scenario configuration file
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"

