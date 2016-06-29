"""
connect2InstrumentBLUE.py

Fluvio L. Lobo Fenoglietto 06/29/2016
"""

import os
import serial

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

        # Brief test connection with Arduino-powered instrument
        #for i in range(0,20):
        #        inString = arduSerialObj[0].readline()
        #        print inString

    # Return variables
    return arduSerialObj


def portRelease(portType, portNum):
    
    terminalStringZero = "Releasing " + portType + " port " + str(portNum)
    print terminalStringZero
    terminalStringOne = "sudo " + portType + " release " + str(portNum)
    print terminalStringOne
    os.system(terminalStringOne)
