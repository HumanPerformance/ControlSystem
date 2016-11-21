"""
smarthandleProtocol.py

The following module has been created to manage the interface between the smart handle module and the control system

Fluvio L Lobo Fenoglietto
11/21/2016

"""

# Import Libraries and/or Modules
import os
import sys
import serial
from timeStamp import *
from configurationProtocol import *
from bluetoothProtocol import *
import protocolDefinitions as definitions

# Standard Functions
#       These functions are standard from the ASCii communication table

# State Enquiry
#       This function requests the status of then stethoscope
#       Input   ::      rfObject                {object}        serial object                      iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def statusEnquiry(rfObject):
        print fullStamp() + " statusEnquiry()"                                                                  # Print function name
        outByte = definitions.ENQ
        rfObject.write(outByte)
        inByte = rfObject.read(size=1)
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device READY"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"                                                     # NAK, in this case, translates to DEVICE NOT READY

# Diagnostic Functions
#       These functions deal with the status of the hardware

# Device Identification
#       This function requests the identification of the connected device
#       Input   ::      {object}                rfObject                serial object
#       Output  ::      {string}                terminal message        terminal message
def deviceID(rfObject):
        outBytes = [definitions.DC1, definitions.DC1_DEVICEID]                                                  # Store the sequence of bytes associated with the operation, function, feature
        inBytes = []
        for i in range(0,len(outBytes)):                                                                        # For loop for the sequential delivery of bytes using the length of the sequence for the range
                rfObject.write(outBytes[i])
                if i == (len(outBytes) - 1):                                                                    # On the last byte, the program reads the response
                        for i in range(0,3):
                                inBytes.append(rfObject.read(size=1))
        print inBytes
