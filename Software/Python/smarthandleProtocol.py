"""
smarthandleProtocol.py

The following module has been created to manage the interface between the smart handle module and the control system

Fluvio L Lobo Fenoglietto
11/21/2016

Modified by : Mohammad Odeh
Date        : May 31st, 2017
Changes     : Modified protocol to use PyBluez instead of PySerial
"""

# Import Libraries and/or Modules
import  os, os.path, sys, time
import  serial
import  smarthandleDefinitions      as      definitions
from    os.path                     import  expanduser
from    timeStamp                   import  fullStamp
from    configurationProtocol       import  *
from    bluetoothProtocol           import  *

# ======================================================================
# ======================> BT REDEFINED FUNCTIONS <======================
# ======================================================================

# ***************************************************
# Functions - Byte-based
#   As we developed more sofisticated hardware and
#   software, our devices will communicate by
#   sending/receiving bytes.
# ***************************************************


# Status Enquiry
#   The following function requests the status of the smart-handle module
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages
def statusEnquiry( socket ):
    print( fullStamp() + " statusEnquiry()" )
    
    outByte = definitions.ENQ
    socket.send(outByte)
    inByte = socket.recv(1)
    
    if inByte == definitions.ACK:
        print( fullStamp() + " ACK Device READY" )
        return 1

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device NOT READY" )
        return 0

    else:
        print( fullStamp() + " Please troubleshoot device" )
        return -1


# Start Streaming
#   The following function allows the smart handle module to stream the data from the on-board sensors through the serial port
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages
def startStreaming( socket ):
    print( fullStamp() + " startStreaming()" )

    outByte = definitions.DC2
    socket.send(outByte)
    inByte = socket.recv(1)
    
    if inByte == definitions.ACK:
        print( fullStamp() + " ACK Device STARTED STREAMING data" )
        return 1

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT START STREAMING data" )
        return 0

    else:
        print( fullStamp() + " Please troubleshoot device" )
        return -1


# Stop Streaming
#   The following function interrupts the streaming of data from the smart-handle module
#   Input   ::  {object}    serial object
#   Output  ::  {string}    terminal messages
def stopStreaming( socket ):
    print fullStamp() + " stopStreaming()"

    outByte = definitions.DC3
    socket.send(outByte)
    inByte = socket.recv(1)
    
    if inByte == definitions.ACK:
        print( fullStamp() + " ACK Device STOPPED STREAMING data" )
        return 1
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT STOP STREAMING data" )
        return 0
    
    else:
        print( fullStamp() + " Please troubleshoot device" )
        return -1


# ***************************************************
# Functions - String-based
#   The original and robust method of communication
#   consisted of character-based communication.
# ***************************************************


# Trigger Device
#   This function triggers the data recording of the smart handle
def triggerDevice( socket, deviceName ):
    inString = deviceName
    print( fullStamp() + " Triggering Device" )
    socket.send('g')
    
    while inString == deviceName:
        inString = bt_recv_end( socket, EOL='\n' )

    print( inString, len(inString) )
    print( fullStamp() + ' Device Triggered' )


# Stop Device
#   This function stops the data collection process of the smart handle
def stopDevice( socket, deviceName ):
    inString = 'null'
    print( fullStamp() + " Stopping Device" )
    socket.send('s')
    
    while inString != deviceName:
        inString = bt_recv_end( socket, EOL='\n' )
        
    print( inString, len(inString) )
    print( fullStamp() + ' Stopped' )


# Data Read
#   This function captures data from the stream
def readStream( socket ):
    return bt_recv_end( socket, EOL='\n' )


# Data Write
#   This function writes the read data to an output file
def dataWrite(executionTimeStamp, currentTime, outputDir, instrumentName, inString):
    dataFileDir = outputDir + "/" + executionTimeStamp

    if os.path.exists(dataFileDir) == False:
        createDataFolder(dataFileDir)
    
    dataFileName = "/" + instrumentName + ".txt"
    dataFilePath = dataFileDir + dataFileName

    if os.path.isfile(dataFilePath) == False:
        createDataFile(dataFilePath, instrumentName)
    
    with open(dataFilePath, "a") as dataFile:
        #timePrefix = "TIM," + str(currentTime) + ","
        #dataFile.write(timePrefix + inString)
        dataFile.write(inString + "\n")


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

# ======================================================================
# =========================> PYSERIAL FUNCTIONS <=======================
# ======================================================================

# Read Stream
#   The following function reads the string-based data stream coming from the serial port
#   Input   ::  {object}    serial object
#   Output  ::  {string}    data string

# Functions - String-based
#   The original and robust method of communication consisted of character-based communication

def triggerDevices(rfObjects,deviceNames):
    print fullStamp() + " triggerDevices()"
    Ndevices = len(rfObjects)
    print fullStamp() + " Triggering " + str(Ndevices) + " devices"
    for i in range(0,Ndevices):
        if rfObjects[i].isOpen() == False:
            rfObjects[i].open()
        inString = deviceNames[i]
        while inString == deviceNames[i]:
            print fullStamp() + " Triggering " + deviceNames[i] + " device..."
            rfObjects[i].write('g')
            time.sleep(1)
            inString = rfObjects[i].readline()[:-1]
            if inString != deviceNames[i]:
                print fullStamp() + " Successfully triggered " + deviceNames[i] + " device"
            elif inString == deviceNames[i]:
                print fullStamp() + " Failed to trigger " + deviceNames[i] + " device"
        rfObjects[i].close()
        time.sleep(1)


def stopDevices(rfObjects,deviceNames):
    print fullStamp() + " stopDevices()"
    Ndevices = len(rfObjects)
    print fullStamp() + " Stopping " + str(Ndevices) + " devices"
    for i in range(0,Ndevices):
        if rfObjects[i].isOpen() == False:
            rfObjects[i].open()
        inString = rfObjects[i].readline()
        while inString != deviceNames[i]:
            print fullStamp() + " Stopping " + deviceNames[i] + " device"
            rfObjects[i].write('s')
            time.sleep(1)
            inString = rfObjects[i].readline()[:-1]
            if inString == deviceNames[i]:
                print fullStamp() + " Successfully stopped " + deviceNames[i] + " device"
            elif inString != deviceNames[i]:
                print fullStamp() + " Failed to stop " + deviceNames[i] + " device"
        rfObjects[i].close()
        time.sleep(1)

def dataReadStreams(rfObjects, Nstreams):
    dataStream = []
    for i in range(0,Nstreams):
        dataStream.append(rfObjects[i].readline())
        time.sleep(0.5)
    return dataStream
