"""
RFConnection.py

Fluvio L. Lobo Fenoglietto 06/29/2016
"""

import os
import serial
from timeStamp import *


def createRFPort(instrumentNames, instrumentBTAddress):

    Ndevices = len(instrumentNames)
    arduRFObj = []
    for i in range(0,Ndevices):
        # Pre-release of RFCOMM port
        print fullStamp() + " Releasing RFCOMM" + str(i)
        portRelease("rfcomm",i)
        # Open RFCOMM port for device
        print fullStamp() + " Connecting device to RFCOMM" + str(i)
        os.system("sudo rfcomm bind /dev/rfcomm" + str(i) + " " + instrumentBTAddress[i])
        # Create Arduino RF-Serial Object
        rfcommPort = "/dev/rfcomm" + str(i)
        RFObj = serial.Serial(rfcommPort,115200) # Need error handle for the case in which the device is not available
        arduRFObj.append(RFObj)
        # Trigger data collection on instruments
        triggerRFInstrument(arduRFObj[i], instrumentNames[i])

    return arduRFObj

def connect2InstrumentBLUE(instrumentNames, instrumentBTAddress):
    
    # Using Object Information to Create RFCOMM Ports
    Ndevices = len(instrumentNames)
    #print Ndevices
    for i in range(0, Ndevices):
        # Pre-releasing serial port
        portRelease("rfcomm",i)
        # Connecting instrument to available port
        terminalStringOne = "Connecting to " + instrumentNames[i]
        #print terminalStringOne
        terminalStringTwo = "sudo rfcomm bind /dev/rfcomm" + str(i) + " " + instrumentBTAddress[i]
        os.system(terminalStringTwo)

    # Creating Arduino serial object
    arduSerialObj = []
    for i in range(0, Ndevices):
        rfcommPort = "/dev/rfcomm" + str(i)
        serialObj = serial.Serial(rfcommPort,115200)
        arduSerialObj.append(serialObj)# Create RFCOMM Ports

        # Verification of connected device
        checkInstrument(arduSerialObj[i], instrumentNames[i])

    # Return variables
    return arduSerialObj


def portRelease(portType, portNum):
    
    terminalStringZero = "Releasing " + portType + " port " + str(portNum)
    # print terminalStringZero
    terminalStringOne = "sudo " + portType + " release " + str(portNum)
    # print terminalStringOne
    os.system(terminalStringOne)

def checkRFInstrument(arduSerialObj, instrumentName):

    iterCheck = 50 # Number of iterations for device searching
    for j in range(0,iterCheck):
        inString = arduSerialObj.readline()
        print inString[:-1]
        if inString[:-1] == instrumentName:
            print "Connected to " + instrumentName
            arduSerialObj.write('g') # trigger data collection
            break
        elif (inString != instrumentName) and (j == iterCheck):
            print instrumentName + " not found"

def triggerRFInstrument(arduRFObj, instrumentName):
    # arduRFObj.flushInput()
    iterCheck = 20
    for i in range(0,iterCheck):
        inString = arduRFObj.readline()
        print inString + ", " + instrumentName 
        if inString[:-1] == instrumentName:
            arduRFObj.write('g') # trigger data collection, exit idle state
            # inString = arduRFObj.readline()
            break

def triggerRFInstruments(arduRFObj, instrumentNames):
    Ndevices = len(instrumentNames)
    for i in range(0,Ndevices):
        inString = ""
        while inString[:-1] != instrumentNames[i]:
            arduRFObj[i].write('g') # trigger data collection, exit idle state
            inString = arduRFObj[i].readline()
            print inString

def stopRFInstrument(arduRFObj, instrumentName):
    inString = ""
    while inString[:-1] != instrumentName:
        arduRFObj.write('s') # t stop data collection, trigger idle state
        inString = arduRFObj.readline()
        print inString

def stopRFInstruments(arduRFObj, instrumentNames):
    Ndevices = len(instrumentNames)
    for i in range(0,Ndevices):
        inString = ""
        while inString[:-1] != instrumentNames[i]:
            arduRFObj[i].write('s') # stop data collection, trigger idle state
            inString = arduRFObj[i].readline()
            print inString

"""
References
1- String Comparison in Python - http://stackoverflow.com/questions/2988017/string-comparison-in-python-is-vs
"""
