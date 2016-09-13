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

# Send until Read
#   Function sends message through serial port until a response is sent
#   The function uses a timer and an iteration check to handle failed communication attempts
def sendUntilRead(rfObject,outString):
    inString = []
    iterCheck = 5                                             # Maximum number of iterations or connection trials
    timeout = 5                                               # Maximum amount of time before message is re-sent 
    comStatus = 0
    for h in range(0,iterCheck):                                # 1st Loop {for-loop} controls the number of communication attempts
        print "Communication attempt " + str(h) + "/" + str(iterCheck)
        rfObject.write(chr(outString))                          # Write message to serial port
        #rfObject.write("\n")                                     # Write newline character to separate messages
        #inChar = rfObject.read(rfObject.inWaiting())
        #print inChar
        startTime = time.time()
        while comStatus == 0 and (time.time() - startTime) < timeout:       # 2nd Loop {while-loop} creates a wait for receiver to response to message sent
            print "Time = " + str(startTime - time.time())
            inString = rfObject.readline(rfObject.inWaiting())
            print inString
            if inString == "F":
                print "ENQ"
                loopStatus = 1
            elif inString == chr(0x06):
                print "ACK"
                loopStatus = 1

# Connect to paired device
#   Connects to the bluetooth devices specified by the scenario configuration file
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"

