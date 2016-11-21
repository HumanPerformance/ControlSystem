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
import smarthandleProtocolDefinitions as definitions

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

# Device-Specific Functions
#       These functions deal with the device-specific operation or features

# Start Recording
#       This function commands the connected smart handle to begin recording/passing sensor data through the serial port
#       The recorded audio is then stored in the local SD
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startRecording(rfObject):
        print fullStamp() + " startRecording()"                                                                 # ...
        outBytes = [definitions.DC3, definitions.DC3_STARTREC]                                                  # ...
        for i in range(0,len(outBytes)):                                                                        # ...
                rfObject.write(outBytes[i])                                                                     # ...
                if i == (len(outBytes) - 1):                                                                    # ...
                        inByte = rfObject.read(size=1)                                                         # ...
        if inByte == definitions.ACK:                                                                           # ...
                print fullStamp() + " ACK SmartHandle will START RECORDING"                                     # ACK, in this case, translates to device START RECORDING
        elif inByte == definitions.NAK:                                                                         # ...
                print fullStamp() + " NAK SmartHandle CANNOT START RECORDING"                                   # NAK, in this case, translates to device CANNOT START RECORDING
           
# Stop Recording
#       This function commands the connected stethoscope to stop recording audio
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def stopRecording(rfObject):
        print fullStamp() + " stopRecording()"                                                                  # ...
        outBytes = [definitions.DC3, definitions.DC3_STOPREC]                                                   # ...
        for i in range(0,len(outBytes)):                                                                        # ...
                rfObject.write(outBytes[i])                                                                     # ...
                if i == (len(outBytes) - 1):                                                                    # ...
                        inByte = rfObject.read(size=1)                                                          # ...
        if inByte == definitions.ACK:                                                                           # ...
                print fullStamp() + " ACK Stethoscope will STOP RECORDING"                                      # If ACK, the stethoscope will STOP recording
        elif inByte == definitions.NAK:                                                                         # ...
                print fullStamp() + " NAK Stethoscope CANNOT STOP RECORDING"                                    # NAK, in this case, translates to CANNOT STOP RECORDING
