"""
thermometerProtocol.py

The following module has been created to manage the device-specific interface between the thermometer and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

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
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def statusEnquiry(rfObject, timeout, iterCheck):
        print " "
        print fullStamp() + " statusEnquiry()"                                                                  # Print function name
        outByte = definitions.ENQ                                                                               # Send ENQ / Status Enquiry command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device READY"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"                                                     # NAK, in this case, translates to DEVICE NOT READY

# System Check
#       This function commands the connected thermometer to perform a "systems check", which may consist on a routine verification of remote features
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def systemCheck(rfObject, timeout, iterCheck):
        print " "
        print fullStamp() + " systemCheck()"                                                                    # Print function name
        outByte = definitions.CHK                                                                               # Send CHK / System Check command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT Ready"                                                     # NAK, in this case, translates to DEVICE NOT READY

# Start Simulation
#       This function starts simulation
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startSIM_000(rfObject, timeout, iterCheck):
        print " "
        print fullStamp() + " Command Sent..."                                                                  # Print function name
        outByte = definitions.SIM                                                                               # Send SIM / Start Simulation - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " Acknowledged! Starting Simulation"
                outByte = definitions.SIM_000                                                                   # Send SIM_000 / Simulate Scenario 1 - see protocolDefinitions.py
                inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)
                if inByte == definitions.ACK:
                        print fullStamp() + " Simulation 1 Running"
                elif inByte == definitions.NAK:
                        print fullStamp() + " Device NOT responding"

        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"


def startSIM_001(rfObject, timeout, iterCheck):
        print " "
        print fullStamp() + " Command Sent..."                                                                  # Print function name
        outByte = definitions.SIM                                                                               # Send SIM / Start Simulation - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " Acknowledged! Starting Simulation"
                outByte = definitions.SIM_001                                                                   # Send SIM_001 / Simulate Scenario 2 - see protocolDefinitions.py
                inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)
                if inByte == definitions.ACK:
                        #do something
                        print fullStamp() + " Simulation 2 Running"
                elif inByte == definitions.NAK:
                        #do something else
                        print fullStamp() + " Device NOT responding"

        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"

def normalOP(rfObject, timeout, iterCheck):
        print " "
        print fullStamp() + " Command Sent..."                                                                  # Print function name
        outByte = definitions.NRMOP                                                                             # Send SIM / Start Simulation - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device READY"                                                         # ACK, in this case, translates to DEVICE READY
                print fullStamp() + " Acknowledged! Normal Operation ON"

        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"
