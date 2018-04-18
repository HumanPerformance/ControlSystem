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


def stopDataStream(rfObject, count):
    print fullStamp() + " Stop sent to smart handle "
    for i in range(0, count):
        rfObject.send( definitions.STOP )
        time.sleep(0.10)
        inString = rfObject.recv(32)
        print inString
        if inString == definitions.ID:
            print fullStamp() + " Device stopped successfully "

