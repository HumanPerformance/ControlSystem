"""
smarthandleProtocol.py

The following module has been created to manage the interface between the smart handle module and the control system

Fluvio L Lobo Fenoglietto
11/21/2016

"""

# Import Libraries and/or Modules
import  os
import  os.path
import  sys
import  serial
import  smarthandleDefinitions      as definitions
from    os.path                     import expanduser
from    timeStamp                   import *
from    configurationProtocol       import *
from    bluetoothProtocol           import *


# Functions - Byte-based
#   As we developed more sofisticated hardware and software, our devices will communicate by sending/receiving bytes

# Status Enquiry
#   The following function requests the status of the smart-handle module
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages
def statusEnquiry(rfObject,attempts):
    print fullStamp() + " statusEnquiry()"
    if rfObject.isOpen() == False:
        rfObject.open()
    outByte = definitions.ENQ
    rfObject.write(outByte)
    time.sleep(1)
    inByte = rfObject.read(size=1)
    if inByte == definitions.ACK:
        print fullStamp() + " ACK Device READY"
    elif inByte == definitions.NAK:
        print fullStamp() + " NAK Device NOT READY"
    else:
        rfObject.close()
        if attempts is not 0:
            return statusEnquiry(rfObject,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Attempts limit reached"
    rfObject.close()

# Start Streaming
#   The following function allows the smart handle module to stream the data from the on-board sensors through the serial port
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages

def startStreaming(rfObject,attempts):
    print fullStamp() + " startStreaming()"
    if rfObject.isOpen() == False:
        rfObject.open()
    outByte = definitions.DC2
    rfObject.write(outByte)
    time.sleep(1)
    inByte = rfObject.read(size=1)
    if inByte == definitions.ACK:
        print fullStamp() + " ACK Device STARTED STREAMING data"
    elif inByte == definitions.NAK:
        print fullStamp() + " NAK Device CANNOT START STREAMING data"
    else:
        rfObject.close()
        if attempts is not 0:
            return startStreaming(rfObject,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Attempts limit reached"
    rfObject.close()

# Read Stream
#   The following function reads the string-based data stream coming from the serial port
#   Input   ::  {object}    serial object
#   Output  ::  {string}    data string

def readStream(rfObject):
    inString = rfObject.readline()
    return inString

# Stop Streaming
#   The following function interrupts the streaming of data from the smart-handle module
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages

def stopStreaming(rfObject,attempts):
    print fullStamp() + " stopStreaming()"
    if rfObject.isOpen() == False:
        rfObject.open()
    outByte = definitions.DC3
    rfObject.write(outByte)
    time.sleep(1)
    inByte = rfObject.read(size=1)
    if inByte == definitions.ACK:
        print fullStamp() + " ACK Device STOPPED STREAMING data"
    elif inByte == definitions.NAK:
        print fullStamp() + " NAK Device CANNOT STOP STREAMING data"
    else:
        rfObject.close()
        if attempts is not 0:
            return stopStreaming(rfObject,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Attempts limit reached"
    rfObject.close()

# Functions - String-based
#   The original and robust method of communication consisted of character-based communication

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
