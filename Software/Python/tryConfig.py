
# Import
import sys
import os
from os.path import expanduser
from configurationProtocol import *
from bluetoothProtocol import *

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
#deviceBTAddress = ["00:06:66:7D:81:7D"]
rfObject = createPort(deviceName, deviceBTAddress)          # create rfObjects/ports

#sendUntilRead(rfObject[0],0x05)

timedRead(rfObject[0],5)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection
