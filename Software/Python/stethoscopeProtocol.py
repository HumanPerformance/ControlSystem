"""
stethoscopeProtocol.py

The following module has been created to manage the device-specific interface between the stethoscope and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

"""

# Import Libraries and/or Modules
import os
import sys
import serial
from timeStamp import *
from configurationProtocol import *
from bluetoothProtocol import *
import protocolDefinitions as definitions

# State Enquiry
#       This function requests the status of then stethoscope
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def statusEnquiry(rfObject, timeout, iterCheck):
        print fullStamp() + " statusEnquiry()"                                                                  # Print function name
        outByte = definitions.ENQ                                                                               # Send ENQ / Status Enquiry command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Device READY"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Device NOT READY"                                                     # NAK, in this case, translates to DEVICE NOT READY

# System Check
#       This function commands the connected stethoscope to perform a "systems check", which may consist on a routine verification of remote features
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def systemCheck(rfObject, timeout, iterCheck):
        print fullStamp() + " systemCheck()"                                                                    # Print function name
        outByte = definitions.CHK                                                                               # Send CHK / System Check command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK SD Card Check Passed"                                                 # If the SD card check is successful, the remote device sends a ACK
                print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK SD Card Check Failed"                                                 # If the SD card check fails, the remote device sends a NAK
                print fullStamp() + " NAK Device NOT Ready"                                                     # NAK, in this case, translates to DEVICE NOT READY


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

# SD Card Check
#       This function commands the connected stethoscope to perform a check on the connected sd card
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def sdCardCheck(rfObject):
        print fullStamp() + " sdCardCheck()"                                                                    # Print function name
        outBytes = [definitions.DC1, definitions.DC1_SDCHECK]                                                   # Store the sequence of bytes associated with the operation, function, feature
        for i in range(0,len(outBytes)):                                                                        # For loop for the sequential delivery of bytes using the length of the sequence for the range
                rfObject.reset_output_buffer()
                rfObject.write(outBytes[i])
                if i == (len(outBytes) - 1):                                                                  # On the last byte, the program reads the response
                        inByte = rfObject.read(size=1)                                                          # The read is limited to a single byte (timeout predefined in the createPort() function)
        if inByte == definitions.ACK:
                print fullStamp() + " ACK SD Card Check Passed"                                                 # If the SD card check is successful, the remote device sends a ACK
                print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:
                print fullStamp() + " NAK SD Card Check Failed"                                                 # If the SD card check fails, the remote device sends a NAK
                print fullStamp() + " NAK Device NOT Ready"                                                     # NAK, in this case, translates to DEVICE NOT READY

# Operational Functions
#       These functions deal with the normal operation of the device


# Device-Specific Functions
#       These functions deal with the device-specific operation or features

# Start Recording
#       This function commands the connected stethoscope to begin recording audio
#       The recorded audio is then stored in the local SD
#       Input   ::      rfObject                {object}        serial object
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startRecording(rfObject):
        print fullStamp() + " startRecording()"                                                                 # ...
        outBytes = [definitions.DC3, definitions.DC3_STARTREC]                                                  # ...
        for i in range(0,len(outBytes)):                                                                        # ...
                rfObject.write(outBytes[i])                                                                     # ...
                if i == (len(outBytes) - 1):                                                                    # ...
                        inByte = rfObject.read(size=1)                                                          # ...
        if inByte == definitions.ACK:                                                                           # ...
                print fullStamp() + " ACK Stethoscope will START RECORDING"                                     # ACK, in this case, translates to device START RECORDING
        elif inByte == definitions.NAK:                                                                         # ...
                print fullStamp() + " NAK Stethoscope CANNOT START RECORDING"                                   # NAK, in this case, translates to device CANNOT START RECORDING
           
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

# Start Playback
#       This function commands the connected stethoscope to play an audio filed stored within the SD card
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startPlayback(rfObject, timeout, iterCheck):
        print fullStamp() + " startPlayback()"                                                                  # Print function name
        outByte = definitions.DC3_STRTPLY                                                                       # Send DC3_STRTPLY / Start Playback command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Stethoscope will START PLAYBACK"                                      # If ACK, the stethoscope will START PLAYBACK
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Stethoscope CANNOT START PLAYBACK"                                    # NAK, in this case, translates to CANNOT START PLAYBACK

# Stop Playback
#       This function commands the connected stethoscope to stop playing an audio filed stored within the SD card
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def stopPlayback(rfObject, timeout, iterCheck):
        print fullStamp() + " stopPlayback()"                                                                   # Print function name
        outByte = definitions.DC4_STPPLY                                                                        # Send DC4_STPPLY / Start Playback command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Stethoscope will STOP PLAYBACK"                                       # If ACK, the stethoscope will STOP PLAYBACK
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Stethoscope CANNOT STOP PLAYBACK"                                     # NAK, in this case, translates to CANNOT STOP PLAYBACK
