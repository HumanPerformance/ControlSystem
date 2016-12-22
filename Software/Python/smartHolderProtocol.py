"""
thermometerProtocol.py

The following module has been created to manage the device-specific interface between the thermometer and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

Modified by: Mohammad Odeh
Date: Nov. 29th, 2016
Adapted protocol to be compatible with the Smart Thermometer Project

"""

# Import Libraries and/or Modules
import os
import sys
import serial
import time
from timeStamp import *
from configurationProtocol import *
from usbProtocol import *
import thermometerDefinitions as definitions

# Path/Directoy Variables
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
# .../Python/data/output
outputFilePath = consysPyDataDir + "/output"


# State Enquiry
#       This function requests the status of the thermometer
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def statusEnquiry(rfObject):
        print fullStamp() + " statusEnquiry()"                                          # Print function name
        outByte = definitions.ENQ                                                       # Send ENQ / Status Enquiry command - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                   # Check for ACK / NAK response
                print fullStamp() + " ACK Device READY\n"                               # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                 # Check for ACK / NAK response
                print fullStamp() + " NAK Device NOT READY\n"                           # NAK, in this case, translates to DEVICE NOT READY

def debugModeON(rfObject):
        print fullStamp() + " debugModeON()"                                            # Print function name
        outByte = definitions.DC1                                                       # Send DC1 / Device Control 1 command - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                   # Check for ACK / NAK response
                print fullStamp() + " ACK Device READY"                                 # ACK, in this case, translates to DEVICE READY
                outByte = definitions.DC1_DEBUGON                                       # Send DEBUGON / debugMode ON - see thermometerDefinitions.py
                rfObject.write(outByte)
                inByte = rfObject.read(size=1)
                if inByte == definitions.ACK:
                        print fullStamp() + " DEBUG MODE ON\n"
                elif inByte != definitions.ACK:
                        print fullStamp() + " Device NOT responding\n"
        
        elif inByte == definitions.NAK:                                                 # Check for ACK / NAK response
                print fullStamp() + " NAK Device NOT READY\n"                           # NAK, in this case, translates to DEVICE NOT READY


# Data Read
#   This function captures the data written to the serial port
def dataRead(rfObject):
    inString = rfObject.readline()
    print inString
    return inString

# Data Write
#   This function writes the data read from serial to an output file
def dataWrite(executionTimeStamp, currentTime, outputFilePath, instrumentName, inString):
    dataFileDir = outputFilePath + "/" + executionTimeStamp

    if os.path.exists(dataFileDir) == False:
        createDataFolder(dataFileDir)
    
    dataFileName = "/" + instrumentName + ".txt"
    dataFilePath = dataFileDir + dataFileName

    if os.path.isfile(dataFilePath) == False:
        createDataFile(dataFilePath, instrumentName)
    
    with open(dataFilePath, "a") as dataFile:
        timePrefix = "TIM," + str(currentTime) + ","
        dataFile.write(timePrefix + inString)
        

# Create Data File
#   Creates the output/text file
def createDataFile(dataFilePath, instrumentName):
    with open(dataFilePath, "a") as dataFile:
        dataFile.write("===================== \n")
        dataFile.write("Scenario =  \n")
        dataFile.write("Instrument = " + instrumentName + "\n")
        dataFile.write("This is a header line \n")
        dataFile.write("===================== \n")

# Create Data Folder
#   Creates the output/text file's directory/folder
def createDataFolder(dataFileDir):
    os.makedirs(dataFileDir)
