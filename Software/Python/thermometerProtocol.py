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
from bluetoothProtocol import *
import thermometerDefinitions as definitions

# State Enquiry
#       This function requests the status of the thermometer
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def statusEnquiry(rfObject):
        print " "
        print fullStamp() + " statusEnquiry()"                                          # Print function name
        outByte = definitions.ENQ                                                       # Send ENQ / Status Enquiry command - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                   # Check for ACK / NAK response
                print fullStamp() + " ACK Device READY"                                 # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                 # Check for ACK / NAK response
                print fullStamp() + " NAK Device NOT READY"                             # NAK, in this case, translates to DEVICE NOT READY

# System Check
#       This function commands the connected thermometer to perform a "systems check", which may consist on a routine verification of remote features
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def systemCheck(rfObject):
        print " "
        print fullStamp() + " systemCheck()"                                            # Print function name
        outByte = definitions.CHK                                                       # Send CHK / System Check command - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                   # Check for ACK / NAK response
                print fullStamp() + " ACK Device Ready"                                 # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                 # Check for ACK / NAK response
                print fullStamp() + " NAK Device NOT Ready"                             # NAK, in this case, translates to DEVICE NOT READY

# Start Simulation
#       This function starts simulation
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startSIM_000(rfObject):
        print " "
        print fullStamp() + " Command Sent..."
        outByte = definitions.SIM                                                       # Send SIM / Start Simulation - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:   
                print fullStamp() + " Acknowledged! Starting Simulation"
                outByte = definitions.SIM_000                                           # Send SIM_000 / Simulate Scenario 1 - see thermometerDefinitions.py
                rfObject.write(outByte)
                inByte = rfObject.read(size=1)
                if inByte == definitions.ACK:
                        print fullStamp() + " Simulation 1 Running"
                elif inByte == definitions.NAK:
                        print fullStamp() + " Device NOT responding"

        elif inByte == definitions.NAK: 
                print fullStamp() + " NAK Device NOT READY"


def startSIM_001(rfObject):
        print " "
        print fullStamp() + " Command Sent..."
        outByte = definitions.SIM                                                       # Send SIM / Start Simulation - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                   # Check for ACK / NAK response
                print fullStamp() + " Acknowledged! Starting Simulation"
                outByte = definitions.SIM_001                                           # Send SIM_001 / Simulate Scenario 2 - see thermometerDefinitions.py
                rfObject.write(outByte)
                inByte = rfObject.read(size=1)
                if inByte == definitions.ACK:
                        print fullStamp() + " Simulation 2 Running"
                elif inByte == definitions.NAK:
                        print fullStamp() + " Device NOT responding"

        elif inByte == definitions.NAK:                                                 # Check for ACK / NAK response
                print fullStamp() + " NAK Device NOT READY"

def normalOP(rfObject):
        print " "
        print fullStamp() + " Command Sent..."
        outByte = definitions.NRMOP                                                     # Send NRMOP / Normal Operation - see thermometerDefinitions.py
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:
                print fullStamp() + " Acknowledged! Normal Operation ON"

        elif inByte == definitions.NAK:
                print fullStamp() + " NAK Device NOT READY"
