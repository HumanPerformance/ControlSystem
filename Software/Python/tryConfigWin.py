
# Import
import sys
import os
from os.path import expanduser
import serial
from bluetoothProtocolWin import createPort
from bluetoothProtocolWin import nextAvailableBTPort
from stethoscopeProtocol import sdCardCheck

# =========
# OPERATION
# =========

#deviceName, deviceBTAddress = pullInstruments(tree, root)   # pull instrument information from configuration file
deviceName = ["hola"]
deviceBTAddress = ["00:06:66:86:76:E6"]
rfObject = createPort("COM71",deviceName,deviceBTAddress)

print rfObject

sdCardCheck(rfObject)
