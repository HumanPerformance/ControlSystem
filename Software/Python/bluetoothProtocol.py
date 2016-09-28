"""
bluetoothProtocol.py

The following module has been created to manage the bluetooth interface between the control system and the connected devices

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016


List of functions ::

X - Look for bluetooth device
X - Pair bluetooth device
X - Add paired device to the instrument list
X.X - Connect to paired device
    X.X - Create rfcomm port
    X.X - Bind rfcomm port
    X.X - Release rfcomm port

"""

# Import Libraries and/or Modules
import os
import serial
import time
from timeStamp import *
import protocolDefinitions as definitions

# Create RFComm Ports
#   This function creates radio-frquency (bluetooth) communication ports for specific devices, using their corresponding address
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"
def createPort(deviceName, deviceBTAddress):
    Ndevices = len(deviceName)                                                              # Determines the number of devices listed
    rfObject = []                                                                           # Create RF object variable/list (in case of multiple devices)
    for i in range(0,Ndevices):     
        portRelease("rfcomm",i)                                                             # The program performs a port-release to ensure that the desired rf port is available
        portBind("rfcomm",i,deviceBTAddress[i])
        rfObject.append(serial.Serial("/dev/rfcomm" + str(i),115200))                       # Create and append RFComm port to the RFObject structure
        #triggerRFInstrument(arduRFObj[i], instrumentNames[i])                              # Trigger data collection on instruments
    return rfObject                                                                         # Return RFObject or list of objects


# Port Bind
#   This function binds the specified bluetooth device to a rfcomm port
#   Input   ::  {string} port type, {int} port number, {string} bluetooth address of device
#   Output  ::  None -- Terminal messages
def portBind(portType, portNumber, deviceBTAddress):
    print fullStamp() + " Connecting device to " + portType + str(portNumber)                    # Terminal message, program status
    os.system("sudo " + portType + " bind /dev/" + portType + str(portNumber) + " " + deviceBTAddress)     # Bind bluetooth device to control system

# Port Release
#   This function releases the specified communication port (serial) given the type and the number
#   Input   ::  {string} "portType", {int} "portNumber"
#   Output  ::  None -- Terminal messages
def portRelease(portType, portNumber):
    print fullStamp() + " Releasing " + portType + str(portNumber)                               # Terminal message, program status
    os.system("sudo " + portType + " release " + str(portNumber))                           # Releasing port through terminal commands

# Port Message Check
#   Reads serial port and checks for a specific input message
#   Input   ::  {string} "inString" -- String to be compared

# Send Until ReaD
#       This function sends an input command through the rfcomm port to the remote device
#       The function sends such command persistently until a timeout or iteration check are met
#       Input   ::      rfObject                {object}        serial object
#                       outByte                 {chr}           command in characters/bytes
#                       timeout                 {int}           maximum wait time for serial communication
#                       iterCheck               {int}           maximum number of iterations for serial communication
#       Output  ::      inByte                  {chr}           response from remote device in characters/bytes
#                       terminal messages       {string}        terminal messages for logging      
def sendUntilRead(rfObject, outByte, timeout, iterCheck):
    print fullStamp() + " sendUntilRead()"                                                                  # Printing program name
    iterCount = 0
    startTime = time.time()                                                                                 # Initial time, instance before entering "while loop"
    while (time.time() - startTime) < timeout and iterCount <= iterCheck:                                   # While loop - will continue until either timeout or iteration check is reached
        print fullStamp() + " Communication attempt " + str(iterCount) + "/" + str(iterCheck)
        print fullStamp() + " Time = " + str(time.time()-startTime)
        rfObject.write(outByte)                                                                             # Send CHK / System Check request
        inByte = rfObject.read()                                                                            # Read response from remote device
        if inByte == definitions.ACK:                                                                       # If response equals ACK / Positive Acknowledgement
            # print fullStamp() + " ACK"                                                                    # Print terminal message, device READY / System Check Successful                                                                             
            return inByte                                                                                   # Return the byte read from the port
            break                                                                                           # Break out of the "while loop"
        elif inByte == definitions.NAK:                                                                     # If response equals NAK / Negative Acknowledgement
            # print fullStamp() + " NAK"                                                                    # Print terminal message, device NOT READY / System Check Failed
            return inByte                                                                                   # Return the byte read from the port
            break                                                                                           # Break out of the "while loop"

# Timed Read
#   This function reads information from the serial port for a given amount of time
#   Input   ::  {object} serial object, {int} time in seconds
#   Output  ::  None - terminal printsouts  
def timedRead(rfObject, timeout):
    startTime = time.time()
    while (time.time() - startTime) < timeout:
        print "Time = " + str(time.time() - startTime)
        inString = rfObject.read()
        if inString == chr(0x05):
            print "ENQ"
            break
        elif inString == chr(0x06):
            print "ACK"
            break

# Connect to paired device
#   Connects to the bluetooth devices specified by the scenario configuration file
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"

