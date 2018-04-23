"""
smarthandleProtocol.py

Fucntions for the operation of the smart handle prototypes

Fluvio L Lobo Fenoglietto 04/18/2018
"""

# Import Libraries and/or Modules
import os
import sys
import serial
import time
from timeStamp import *

import smarthandleDefinitions as definitions


# Functions

# startDataStream -v.2.0
def startDataStream( socket, count, EOL=None):
    for i in range(0, count):
        buff = readDataStream( socket, EOL=None )
        print( buff )
        if buff == definitions.ID:
            socket.send( definitions.START )
            print( fullStamp() + " Trigger sent to smart handle " )
        elif i == ( count -1 ):
            print( fullStamp() + " Triggering complete " )

"""
startDataStream -v.1.0
def startDataStream(rfObject, count):
    for i in range(0, count):
        time.sleep(0.10)
        inString = rfObject.recv(32).replace('\n','')
        print inString
        if inString == definitions.ID:
            rfObject.send( definitions.START )
            print fullStamp() + " Trigger sent to smart handle "
        elif i == (count - 1):
            print fullStamp() + " Triggering complete "
"""

def readDataStream( socket, EOL=None ):
    inData, inChar = 'null', 'null'
    firstReading = True
    
    if EOL is None:
        # Get rid of any chopped/truncated data
        while inData != ('\n' or '\r' or '\0'):
            inData = socket.recv(1)

        # Read into buffer as long EOL is not reached
        while inChar != ('\n' or '\r' or '\0'):
            # If first reading, store reading directly to buffer
            if firstReading:
                buff = socket.recv(1)
                firstReading = False

            # Else, store reading into inChar then append to buffer
            else:
                inChar = socket.recv(1)
                buff += inChar

        # Return buffer
        return buff.strip('\n')

    else:
        # Get rid of any chopped/truncated data
        while inData != (EOL):
            inData = socket.recv(1)

        # Read into buffer as long EOL is not reached
        while inChar != (EOL):
            # If first reading, store reading directly to buffer
            if firstReading:
                buff = socket.recv(1)
                firstReading = False

            # Else, store reading into inChar then append to buffer
            else:
                inChar = socket.recv(1)
                buff += inChar

        # Return buffer
        return buff.strip(EOL)   


def stopDataStream(rfObject, count):
    print fullStamp() + " Stop sent to smart handle "
    for i in range(0, count):
        rfObject.send( definitions.STOP )
        time.sleep(0.10)
        inString = rfObject.recv(32)
        print inString
        if inString == definitions.ID:
            print fullStamp() + " Device stopped successfully "

