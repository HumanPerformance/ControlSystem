
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

deviceName, deviceBTAddress = pullInstruments(tree, root)   # pull instrument information from configuration file
#deviceName = ["hola"]
#deviceBTAddress = ["00:06:66:7D:80:CD"]
rfObject = createPort(deviceName, deviceBTAddress)          # create rfObjects/ports

#sendUntilRead(rfObject[0],0x05)

#statusEnquiry(rfObject[0])
systemCheck(rfObject[0])

#timedRead(rfObject[0],5)

#for i in range(0,50):
#    rfObject[0].write(chr(0x05))
#    print str(i)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection
