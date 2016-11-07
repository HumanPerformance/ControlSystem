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
import bluetooth
"""
        Implementation of the "bluetooth" module may require the installation of the python-bluez package
        >> sudp apt-get install python-bluez
"""
import os
import serial
import time
from timeStamp import *
import protocolDefinitions as definitions


# Find RF Device
#   This function uses the hardware of the peripheral device or control system to scan/find bluetooth enabled devices
#   This function does not differenciate among found devices
#   Input   ::  None
#   Output  ::  {array, list} "availableDeviceNames", "availableDeviceBTAddresses"
def findDevices():
    print fullStamp() + " findDevices()"
    devices = bluetooth.discover_devices(
        duration=20,                                                                        # Search timeout
        lookup_names=True)                                                                  # Search and acquire names of antennas
    Ndevices = len(devices)                                                                 # Number of detected devices
    availableDeviceNames = []                                                               # Initialized arrays/lists for device names...
    availableDeviceBTAddresses = []                                                         # ...and their bluetooth addresses
    for i in range(0,Ndevices):                                                             # Populate device name and bluetooth address arrays/lists with a for-loop
        availableDeviceNames.append(devices[i][1])
        availableDeviceBTAddresses.append(devices[i][0])
    print fullStamp() + " Devices found (names): " + str(availableDeviceNames)              # Print the list of devices found
    print fullStamp() + " Devices found (addresses): " + str(availableDeviceBTAddresses)    # Print the list of addresses for the devices found
    return availableDeviceNames, availableDeviceBTAddresses                                 # Return arrays/lists of devices and bluetooth addresses

# Identify Smart Devices
#   This function searches through the list of detected devices and...
#   Input   ::  {string}     "smartDeviceIdentifier"
#           ::  {array/list} "availableDeviceNames", "availableDeviceBTAddresses"
#   Output  ::  {array/list} "smartDeviceNames", "smartDeviceBTAddresses"
def findSmartDevices(smartDeviceIdentifier, availableDeviceNames, availableDeviceBTAddresses):
    print fullStamp() + " findSmartDevices()"
    Ndevices = len(availableDeviceNames)
    smartDeviceNames = []
    smartDeviceBTAddresses = []
    for i in range(0,Ndevices):
        deviceIdentifier = availableDeviceNames[i][0:4]
        if deviceIdentifier == smartDeviceIdentifier:
            smartDeviceNames.append(availableDeviceNames[i])
            smartDeviceBTAddresses.append(availableDeviceBTAddresses[i])
    print fullStamp() + " Smart Devices found (names): " + str(smartDeviceNames)
    print fullStamp() + " Smart Devices found (addresses): " + str(smartDeviceBTAddresses)
    return smartDeviceNames, smartDeviceBTAddresses

# Create RFComm Ports
#   This function creates radio-frquency (bluetooth) communication ports for specific devices, using their corresponding address
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"
def createPorts(deviceName, deviceBTAddress):
    Ndevices = len(deviceName)                                                              # Determines the number of devices listed
    rfObject = []                                                                           # Create RF object variable/list (in case of multiple devices)
    for i in range(0,Ndevices):     
        portRelease("rfcomm",i)                                                             # The program performs a port-release to ensure that the desired rf port is available
        portBind("rfcomm",i,deviceBTAddress[i])
        rfObject.append(serial.Serial("/dev/rfcomm" + str(i),115200))                       # Create and append RFComm port to the RFObject structure
        #triggerRFInstrument(arduRFObj[i], instrumentNames[i])                              # Trigger data collection on instruments
    return rfObject                                                                         # Return RFObject or list of objects

# Create RFComm Port
def createPort(deviceName,deviceBTAddress):
    portRelease("rfcomm",0)                                                             # The program performs a port-release to ensure that the desired rf port is available
    portBind("rfcomm",0,deviceBTAddress[0])
    rfObject = serial.Serial(
        port = "/dev/rfcomm" + str(0),
        baudrate = 115200,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        timeout = 5)
    return rfObject   

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

