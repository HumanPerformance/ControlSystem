"""
stethoscopeProtocol.py

The following module has been created to manage the device-specific interface between the stethoscope and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

List of functions ::




List of commands ::

Command Type    Definition
------------------------------------------------------------------------
SAREC     {string} Start Recording
SOREC     {string} Stop Recording


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
#       Input   ::      None (uses ENQ 0x05)
#       Output  ::      Stethoscope Status
def statusEnquiry(rfObject, timeout, iterCheck):
        print fullStamp() + " statusEnquiry() "                                                                 # Printing program status messages - helpful for debugging
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

# System Check
#       This function commands the connected stethoscope to perform a "systems check", which may consist on a routine verification of remote features
#       Input   ::      rfObject                {object}        serial object
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      terminal messages       {string}        terminal messages for logging
def systemCheck(rfObject, timeout, iterCheck):
        print fullStamp() + " systemCheck() "                                                                   # Printing program status messages - helpful for debugging
        iterCount = 0
        startTime = time.time()                                                                                 # Initial time, instance before entering "while loop"
        while (time.time() - startTime) < timeout and iterCount <= iterCheck:                                   # While loop - will continue until either timeout or iteration check is reached 
                print fullStamp() + "  Communication attempt " + str(iterCount) + "/" + str(iterCheck)
                print fullStamp() + "  Time = " + str(time.time()-startTime)
                rfObject.write(definitions.CHK)                                                                 # Send CHK / System Check request
                inByte = rfObject.read()                                                                        # Read response from remote device
                if inByte == definitions.ACK:                                                                   # If response equals ACK / Positive Acknowledgement
                        print fullStamp() + "  ACK :: Device Ready"                                             # Print terminal message, device READY / System Check Successful                                                                             
                        break                                                                                   # Break out of the "while loop"
                elif inByte == definitions.NAK:                                                                 # If response equals NAK / Negative Acknowledgement
                        print fullStamp() + "  NAK :: Device NOT Ready"                                         # Print terminal message, device NOT READY / System Check Failed
                        break                                                                                   # Break out of the "while loop"

"""        
        for h in range(0,iterCheck):                                                    # 1st Loop {for-loop} controls the number of communication attempts
                print "Communication attempt " + str(h) + "/" + str(iterCheck)
                rfObject.write(definitions.ENQ)                                          # Write message to serial port
                startTime = time.time()
                while (time.time() - startTime) < timeout:                              # 2nd Loop {while-loop} creates a wait for receiver to response to message sent
                        print "Time = " + str(startTime - time.time())
                        inString = rfObject.read()
                        if inString == chr(0x05):
                                print "ENQ"
                                break
                        elif inString == chr(0x06):
                                print "ACK"
                                h = iterCheck
                                break
                                """
                                

# Begin Recording
#       This function will trigger the recording and storing of an audio signal by the Teensy board
#       Input   ::      None
#       Output  ::      None
def beginRecord(rfObject):
        outString = "REC"
        
