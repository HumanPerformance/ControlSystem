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

"""
        print fullStamp() + " statusEnquiry() "                                                                 # Printing program name
        iterCount = 0
        startTime = time.time()                                                                                 # Initial time, instance before entering "while loop"
        while (time.time() - startTime) < timeout and iterCount <= iterCheck:                                   # While loop - will continue until either timeout or iteration check is reached 
                print fullStamp() + "  Communication attempt " + str(iterCount) + "/" + str(iterCheck)
                print fullStamp() + "  Time = " + str(time.time()-startTime)
                rfObject.write(definitions.ENQ)                                                                 # Send CHK / System Check request
                inByte = rfObject.read()                                                                        # Read response from remote device
                if inByte == definitions.ACK:                                                                   # If response equals ACK / Positive Acknowledgement
                        print fullStamp() + "  ACK :: Device Ready"                                             # Print terminal message, device READY / System Check Successful                                                                             
                        break                                                                                   # Break out of the "while loop"
                elif inByte == definitions.NAK:                                                                 # If response equals NAK / Negative Acknowledgement
                        print fullStamp() + "  NAK :: Device NOT Ready"                                         # Print terminal message, device NOT READY / System Check Failed
                        break                                                                                   # Break out of the "while loop"
"""

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
                
"""
        print fullStamp() + " systemCheck() "                                                                   # Printing program name
        iterCount = 0
        startTime = time.time()                                                                                 # Initial time, instance before entering "while loop"
        while (time.time() - startTime) < timeout and iterCount <= iterCheck:                                   # While loop - will continue until either timeout or iteration check is reached 
                print fullStamp() + "  Communication attempt " + str(iterCount) + "/" + str(iterCheck)
                print fullStamp() + "  Time = " + str(time.time()-startTime)
                rfObject.write(definitions.CHK)                                                                 # Send CHK / System Check request
                inByte = rfObject.read()                                                                        # Read response from remote device
                if inByte == definitions.ACK:                                                                   # If response equals ACK / Positive Acknowledgement
                        print fullStamp() + "  ACK :: SD Card Check Passed"                                     # CHK triggers an SD card check on the remote device
                        print fullStamp() + "  ACK :: Device Ready"                                             # Print terminal message, device READY / System Check Successful                                                                             
                        break                                                                                   # Break out of the "while loop"
                elif inByte == definitions.NAK:                                                                 # If response equals NAK / Negative Acknowledgement
                        print fullStamp() + "  NAK :: SD Card Check Failed"                                     # If the SD card check fails, the remote device sends a NAK
                        print fullStamp() + "  NAK :: Device NOT Ready"                                         # Print terminal message, device NOT READY / System Check Failed
                        break                                                                                   # Break out of the "while loop"          
"""

# Start Recording
#       This function commands the connected stethoscope to begin recording audio
#       The recorded audio is then stored in the local SD
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def startRecording(rfObject):
        print fullStamp() + " systemCheck()"                                                                    # Print function name
        outByte = definitions.CHK                                                                               # Send CHK / System Check command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK SD Card Check Passed"                                                 # If the SD card check is successful, the remote device sends a ACK
                print fullStamp() + " ACK Device Ready"                                                         # ACK, in this case, translates to DEVICE READY
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK SD Card Check Failed"                                                 # If the SD card check fails, the remote device sends a NAK
                print fullStamp() + " NAK Device NOT Ready"                                                     # NAK, in this case, translates to DEVICE NOT READY
           
# Stop Recording
#       This function commands the connected stethoscope to stop recording audio
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def stopRecording(rfObject):
        print fullStamp() + " stopRecording()"                                                                  # Print function name
        outByte = definitions.DC2_STPREC                                                                        # Send DC2_STPREC / Stop Recording command - see protocolDefinitions.py
        inByte = sendUntilRead(rfObject, outByte, timeout, iterCheck)                                           # Execute sendUntilRead() from bluetoothProtocol.py
        if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " ACK Stethoscope will STOP recording"                                      # If ACK, the stethoscope will STOP recording
        elif inByte == definitions.NAK:                                                                         # Check for ACK / NAK response found through sendUntilRead()
                print fullStamp() + " NAK Stethoscope CANNOT STOP recording"                                    # NAK, in this case, translates to CANNOT STOP RECORDING
                # need to add error handles
                #       - Why will this error appear?
 
