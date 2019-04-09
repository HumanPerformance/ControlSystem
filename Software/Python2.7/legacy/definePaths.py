"""
definePaths.py

The following function has been designed to list the folder and file paths that are of importance to the consys.py function

Fluvio L. Lobo Fenoglietto 06/16/2016
"""
import os
from os.path import expanduser

def definePaths():
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
        #scenarioConfigFilePath = consysPyDataDir + "/scenarios"
        # .../Python/instruments
        instrumentsConfigFilePath = consysPyDataDir + "/instruments"
        #instrumentsConfigFileName = "/instrumentconfig.txt"
        #instrumentsConfigFile = instrumentsConfigFilePath + instrumentsConfigFileName
        # .../Processing/.../consys.sh
        #countdownDir = homeDir + "/csec/repos/ControlSystem/Software/Processing/countdown/build/armvh6f"
        # .../Processing/.../consys/data
        #countdownDataDir = countdownDir + "/data"
        return consysPyDataDir instrumentsConfigFilePath
