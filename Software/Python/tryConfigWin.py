
# Import
import sys
import os
from os.path import expanduser
import serial
from bluetoothProtocolWin import createPort

# =========
# OPERATION
# =========

#deviceName, deviceBTAddress = pullInstruments(tree, root)   # pull instrument information from configuration file
deviceName = ["hola"]
deviceBTAddress = ["00:06:66:86:76:E6"]
portName = "COM70"
rfObject = createPort(portName,deviceName,deviceBTAddress)

sdCardCheck(rfObject)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection
