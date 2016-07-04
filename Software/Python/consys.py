"""
consys.py

Control System --Python

The following program has been designed to control the following processes:
1.0 - Read and follow instruction from server
    1.1 - Instructions are passed as terminal inputs
        Note: The program currently handles one (1) input - scalable
2.0 - Load configuration file based on server instructions or input
    Note: Configuration file currently located locally - can be switched to the server
    2.1 - Define path of configuration file based on user input
    2.2 - Load configuration file
    2.3 - Save loaded data into program variables
3.0 - Write loaded variables into downstream configuration file for parallel applications
    Note: Dowstream parallel applications currently include:
            - countdown.pde (Processing)
    3.1 - Define path of configuration file
    3.2 - Write configuration file
4.0 - Execution of downstream parallel applications
    Note: Dowstream parallel applications currently include:
            - countdown.pde (Processing)
            
Fluvio L. Lobo Fenoglietto 05/19/2016
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
# Python modules
import sys
import os
from os.path import expanduser
import serial
import time
# Functions
from doubleDigitCorrection import doubleDigitCorrection
from pullInstruments import pullInstruments
from connect2InstrumentBLUE import connect2InstrumentBLUE
from instrumentDataAcquisition import dataRead

# ==============================================
# Variables
# ==============================================

# ----------------------------------------------
# A) Path/Directory Variables
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
# The exact scenario name is determined using the terminal input (Operation :: 1.0-2.0)
# .../Python/data/instruments
instrumentsConfigFilePath = consysPyDataDir + "/instruments"
instrumentsConfigFileName = "/instrumentconfig.txt"
instrumentsConfigFile = instrumentsConfigFilePath + instrumentsConfigFileName
# .../Processing/.../countdown
countdownDir = homeDir + "/csec/repos/ControlSystem/Software/Processing/countdown/build/armv6hf"
# .../Processing/.../countdown/.../data
countdownDataDir = countdownDir + "/data"
countdownConfigFilePath = countdownDataDir
countdownConfigFileName = "/countdownInit.txt"
countdownConfigFile = countdownConfigFilePath + countdownConfigFileName

# ==============================================
# Operation
# ==============================================

# ----------------------------------------------
# 1.0 - Read Terminal (local or SSH) Input
# ----------------------------------------------
inputArg = sys.argv
selectedScenario = int(sys.argv[1])
outString = "User Executed " + inputArg[0] + ", scenario #" + inputArg[1]
print outString

# ----------------------------------------------
# 2.0 - Load Configuration File
# ----------------------------------------------
# Loading configuration file using terminal input
scenarioNumberString = doubleDigitCorrection(inputArg[1])
scenarioConfigFileName = "/sc" + scenarioNumberString + ".txt"
scenarioConfigFile = scenarioConfigFilePath + scenarioConfigFileName
with open(scenarioConfigFile,'r+') as scenarioConfigFileObj:
    lines = scenarioConfigFileObj.readlines()

# Save loaded data into program variables
Nlines = len(lines)
scenarioConfigVariables = []
scenarioConfigValues = []
for i in range(0, Nlines-1):
    scenarioConfigVariables.append(lines[i].split(":")[0])
    scenarioConfigValues.append(lines[i].split(":")[1])
# print scenarioConfigVariables
# print int(scenarioConfigValues[1])

# ----------------------------------------------
# X.0 - Write Configuration File
# ----------------------------------------------
# Write configuration file for downstream parallel applications
with open(countdownConfigFile, 'r+') as countdownConfigFileObj:
    # Note: For the countdown application, only two inputs are currently needed: StartTime and WarningTime
    countdownConfigFileObj.write(scenarioConfigVariables[1] + ":" + str(scenarioConfigValues[1]))
    countdownConfigFileObj.write(scenarioConfigVariables[2] + ":" + str(scenarioConfigValues[2]))

# ----------------------------------------------
# X.0 - Connect Instrument(s)
# ----------------------------------------------
# Pull instrument information from the instrument configuration file
Ndevices, instrumentNames, instrumentBTAddress = pullInstruments(instrumentsConfigFile)
# Connect to instruments by creating bluetooth-serial (RFCOMM) ports
arduSerialObj = connect2InstrumentBLUE(instrumentNames, instrumentBTAddress)

# ----------------------------------------------
# X.0 - Execute Parallel Application(s)
# ----------------------------------------------
print "User may execute countdown application now"
#countdownExeFilePath = countdownDir
#countdownExeFileName = "/countdown"
#terminalCommand = "DISPLAY=:0.0; " + countdownExeFilePath + countdownExeFileName + " &"
#os.system(terminalCommand)
time.sleep(5)

# ----------------------------------------------
# X.0 - Data Acquisition Timed-Loop
# ----------------------------------------------
startTime = time.time()
currentTime = 0
stopTime = 10 # seconds

while currentTime < stopTime:
        #
        # Operation

        # Loop through all devices
        for i in range(0,Ndevices):

            # Read data from device
            dataRead(arduSerialObj[i])
            

        # Update time
        currentTime = time.time() - startTime
        # print currentTime

print "Program Concluded"

"""
References
1- Defining Functions in Python - http://www.tutorialspoint.com/python/python_functions.htm
2- Calling Functions from other Python scripts - http://stackoverflow.com/questions/20309456/how-to-call-a-function-from-another-file-in-python
3- "       "         "    "     "      "       - http://stackoverflow.com/questions/7701646/how-to-call-a-function-from-another-file
4- Returning multiple variables from python function/script - http://stackoverflow.com/questions/354883/how-do-you-return-multiple-values-in-python
5- Writing to Serial on Python - http://playground.arduino.cc/Interfacing/Python
"""
