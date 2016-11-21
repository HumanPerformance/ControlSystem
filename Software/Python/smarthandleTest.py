"""
smarthandleTest.py

The following script has been created to test/debug functions specific to the smart handle prototype

Fluvio L Lobo Fenoglietto
11/21/2016
"""

# Import
import sys
import os
from os.path import expanduser
import serial
from configurationProtocol import *
from bluetoothProtocol import *
from smarthandleProtocol import *

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

deviceName = ["smart-handle"]
deviceBTAddress = ["00:06:66:80:8C:AB"]
rfObject = createPort(deviceName, deviceBTAddress)          # create rfObjects/ports

deviceID(rfObject)

portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection

