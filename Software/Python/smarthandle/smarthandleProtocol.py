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

def startDataStream(rfObject):
    for i in range(0, 100):
        time.sleep(0.10)
        inString = rfObject.recv(32)
        if inString == definitions.ID:
            rfObject.send( definitions.START )
            print fullStamp() + " Trigger sent to smart handle "
        elif i = 99:
            print fullStamp() + " Triggering complete "


def stopDataStream(rfObject):
    for i in range(0, 100):
        rfObject.send( definitions.STOP )
        print fullStamp() + " Stop sent to smart handle "
        time.sleep(0.10)
        inString = rfObject.recv(32)
        if inString == definitions.ID:
            print fullStamp() + " Device stopped successfully "

