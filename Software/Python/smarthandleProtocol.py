"""
smarthandleProtocol.py

The following module has been created to manage the interface between the smart handle module and the control system

Fluvio L Lobo Fenoglietto
11/21/2016

"""

# Import Libraries and/or Modules
import os
import os.path
from os.path import expanduser
import sys
import serial
from timeStamp import *
from configurationProtocol import *
from bluetoothProtocol import *
import smarthandleDefinitions as definitions

# Functions - Byte-based

# Status Enquiry
#   This function requests the status of the bluetooth device
def statusEnquiry(rfObject, timeout, iterCheck):
        print fullStamp() + " statusEnquiry()"                                                                  # Print function name
        outByte = definitions.ENQ                                                                               # Send ENQ / Status Enquiry command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device READY"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"

def startStreaming(rfObject):
    print fullStamp() + " startStreaming()"                                                                    # Print function name
    outBytes = [definitions.DC3, definitions.DC3_STARTSTREAM]
    inBytes = []
    for i in range(0,len(outBytes)):                                                                        # For loop for the sequential delivery of bytes using the length of the sequence for the range
        rfObject.write(outBytes[i])
        time.sleep(1)
        inBytes.append(rfObject.read(size=1))                                                          # The read is limited to a single byte (timeout predefined in the createPort() function)
    if inBytes[len(outBytes)-1] == definitions.ACK:
        print fullStamp() + " ACK SD Card Check Passed"                                                 # If the SD card check is successful, the remote device sends a ACK
        print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
    elif inBytes[len(outBytes)-1] == definitions.NAK:
        print fullStamp() + " NAK SD Card Check Failed"                                                 # If the SD card check fails, the remote device sends a NAK
        print fullStamp() + " NAK Device NOT Ready"

def readStream(rfObject):
    #print fullStamp() + " readStream()"
    inString = rfObject.readline()
    print inString

def stopStreaming(rfObject):
    print fullStamp() + " stopStreaming()"                                                                    # Print function name
    outBytes = [definitions.DC3, definitions.DC3_STOPSTREAM]
    inBytes = []
    for i in range(0,len(outBytes)):                                                                        # For loop for the sequential delivery of bytes using the length of the sequence for the range
        rfObject.write(outBytes[i])
        time.sleep(1)
        inBytes.append(rfObject.read(size=1))                                                          # The read is limited to a single byte (timeout predefined in the createPort() function)
    if inBytes[len(outBytes)-1] == definitions.ACK:
        print fullStamp() + " ACK SD Card Check Passed"                                                 # If the SD card check is successful, the remote device sends a ACK
        print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
    elif inBytes[len(outBytes)-1] == definitions.NAK:
        print fullStamp() + " NAK SD Card Check Failed"                                                 # If the SD card check fails, the remote device sends a NAK
        print fullStamp() + " NAK Device NOT Ready"

# Functions - String-based

# Trigger Device
#   This function triggers the data recording of the smart handle
def triggerDevice(rfObject,deviceName,iterCheck):
    for i in range(0,iterCheck):
        inString = rfObject.readline()
        if inString[:-1] == deviceName:
            print "Triggering device..."
            rfObject.write('g')
            break

# Stop Device
# This function stops the data collection process of the smart handle
def stopDevice(rfObject, deviceName, iterCheck):
    for i in range(0,iterCheck):
        inString = rfObject.readline()
        if inString[:-1] != deviceName:
            print "Stopping device..."
            rfObject.write('s')
            break

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
    
"""
References
1 - Print String to File - http://stackoverflow.com/questions/5214578/python-print-string-to-text-file
2 - File Modes - https://docs.python.org/2/tutorial/inputoutput.html
3 - Check for file existence - http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
4 - Print on a new line - http://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-everytime
5 - Check for Existance and Create Directory - http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
"""
