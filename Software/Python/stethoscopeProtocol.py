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
import serial
from timeStamp import *
from configurationProtocol import *
from bluetoothProtocol import *
import protocolDefinitions as definitions

# State Enquiry
#       This function requests the status of then stethoscope
#       Input   ::      None (uses ENQ 0x05)
#       Output  ::      Stethoscope Status
def statusEnquiry(rfObject):
        iterCount = 0
        iterCheck = 5                                                                   # Maximum number of iterations or connection trials
        timeout = 5                                                                   # Maximum amount of time before message is re-sent
        startTime = time.time()
        while (time.time() - startTime) < timeout and iterCount <= iterCheck:
                print "Communication attempt " + str(iterCount) + "/" + str(iterCheck)
                rfObject.write(definitions.ENQ)                                          # Write message to serial port
                startTime = time.time()
                inString = rfObject.read()
                if inString == chr(0x05):
                        print "ENQ"
                elif inString == chr(0x06):
                        print "ACK"
                        break
        #iterCount = iterCount + 1
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
        
