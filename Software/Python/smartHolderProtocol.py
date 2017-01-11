"""
thermometerProtocol.py

The following module has been created to manage the device-specific interface between the thermometer and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

Modified by: Mohammad Odeh
Date: Nov. 29th, 2016
Protocol is NOT fully adapted for the SmartHolder project

"""

# Import Libraries and/or Modules
import os
import sys
import serial
import time
from timeStamp import *
from configurationProtocol import *
from usbProtocol import *
import smartHolderDefinitions as definitions


# Data Read
#   This function captures the data written to the serial port
def dataRead(rfObject):
    if rfObject.isOpen() is False:
        rfObject.open()
    dataAvailable = rfObject.in_waiting
    while dataAvailable is not 0:
        time.sleep(.15)
        inString = rfObject.readline()
        #dataAvailable = rfObject.in_waiting
        print inString
    rfObject.flush()
    rfObject.close()
    try:
        return inString
    except:
        print "No data to print"

def deviceID(usbObject,deviceName):
    print fullStamp() + " deviceID()"
    if usbObject.isOpen() is False:
        usbObject.open()
    print fullStamp() + " Identifying Device"
    inString = usbObject.readline()[:-1]
    while inString != deviceName:
        rfObject.flush()
        rfObject.reset_input_buffer()
        rfObject.reset_output_buffer()
        print fullStamp() + " Requesting Device Name"
        rfObject.write('n')
        time.sleep(1)
        inString = usbObject.readline()[:-1]
        print inString
    usbObject.close()   

def triggerDevice(rfObject,deviceName):
    if rfObject.isOpen() is False:
        rfObject.open()
    inString = deviceName
    print fullStamp() + " Triggering Device"
    while inString == deviceName:
        time.sleep(0.15)
        rfObject.write('s')
        time.sleep(1)
        if rfObject.in_waiting > 0:
                inString = rfObject.readline()[:-1]
                print fullStamp() + " Device Triggered Successfully"
                print deviceName
        else:
                print fullStamp() + " Device Failed to Trigger"
                print fullStamp() + " Reattempting..."
    rfObject.close()

def stopDevice(rfObject,deviceName):
    if rfObject.isOpen() is False:
        rfObject.open()

    inString = rfObject.readline()
    while inString != deviceName:
        rfObject.flush()
        rfObject.reset_input_buffer()
        rfObject.reset_output_buffer()
        print fullStamp() + " Stopping Device"
        rfObject.write('i')
        time.sleep(1)
        inString = rfObject.readline()[:-1]
        inString = deviceName
        print inString
    rfObject.close()

def dataReadStreams(rfObjects, Nstreams):
    dataStream = []
    for i in range(0,Nstreams):
        dataStream.append(rfObjects[i].readline())
        time.sleep(0.5)
    return dataStream

#   This function captures the data written to the serial port
def dataRead_interrupt(rfObject):
    if rfObject.isOpen() is False:
        rfObject.open()
    dataAvailable = rfObject.in_waiting
    i=0
    while dataAvailable is not 0:
        i = i+1
        print "(1)bytesAvailable: " + str(dataAvailable)
        print "loop # " + str(i)
        time.sleep(.15)
        inString = rfObject.readline()
        dataAvailable = rfObject.in_waiting
        print inString
        if i is 55:
            rfObject.flush()
            rfObject.reset_input_buffer()
            rfObject.reset_output_buffer()
            time.sleep(1.5)
            print "(2)bytesAvailable: " + str(dataAvailable)
            rfObject.write("i")
            time.sleep(.15)
            dataAvailable = rfObject.in_waiting
            while dataAvailable is not 0:
                print "(3)bytesAvailable: " + str(dataAvailable)
                time.sleep(.15)
                inString = rfObject.readline()
                dataAvailable = rfObject.in_waiting
                print inString
    rfObject.flush()
    rfObject.close()
    return inString

# Data Write
#   This function writes the data read from serial to an output file
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



'''
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

'''
