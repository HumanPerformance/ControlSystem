
# Import
import sys
import os
from os.path import expanduser
import serial
from configurationProtocol import *
from bluetoothProtocol import *
from stethoscopeProtocol import *

# Variables
# ----------------------------------------------
# B) Path/Directory Variables
# ----------------------------------------------
homeDir = expanduser("~")
rootDir = "/root"
if homeDir == rootDir:
          homeDir = "/home/pi"
          # This check and correction is needed for raspbian
# .../Python
consysPyDir = homeDir + "/csec/repos/ControlSystem/Software/Python"
# .../Python/data
consysPyDataDir = consysPyDir + "/data"
# .../Python/data/scenarios
scenarioConfigFilePath = consysPyDataDir + "/scenarios"

# Scenario File Name
scenarioFileName = "sc001.xml"

configFile = scenarioConfigFilePath + "/" + scenarioFileName
tree, root = readConfigFile(configFile)

# =========
# OPERATION
# =========

deviceName = "stet"
deviceBTAddress = "00:06:66:86:76:E6"                              # stethoscope prototype 
#deviceBTAddress = "00:06:66:7D:80:D0"                               # POV stethoscope
rfObject = createPort(deviceName, deviceBTAddress, 115200, 5)       # create rfObjects/ports

#statusEnquiry(rfObject)
#startTrackingMicStream(rfObject)

#while(1):
#    outString = rfObject.read(size=1)
#    print outString

stopTrackingMicStream(rfObject)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection
