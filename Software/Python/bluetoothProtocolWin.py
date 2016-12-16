"""
bluetoothProtocolWin.py

The following module has been created to manage the bluetooth interface between the control system (with a Windows OS) and the connected devices

Fluvio L Lobo Fenoglietto
11/08/2016

"""

# Import Libraries and/or Modules
import bluetooth
"""
        Implementation of the "bluetooth" module may require the installation of the python-bluez package
        >> sudp apt-get install python-bluez
"""
import os
import serial
import serial.tools.list_ports
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
        # Print a list of devices' names and addresses
        print fullStamp() + " Device (name, address): (" + str(availableDeviceNames[i]) + ", " + str(availableDeviceBTAddresses[i]) + ")"
    print "\n"
    return availableDeviceNames, availableDeviceBTAddresses                                 # Return arrays/lists of devices and bluetooth addresses

# Identify Smart Devices - General
#   This function searches through the list of detected devices and finds the smart devices corresponding to the input identifier
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

# Identify Smart Device - Specific
#   This function searches through the list of detected devices and finds the specific smart device corresponding to the input name
#   Input   ::  {string}     "smartDeviceName"
#           ::  {array/list} "availableDeviceNames", "availableDeviceBTAddresses"
#   Output  ::  {array/list} "smartDeviceNames", "smartDeviceBTAddresses"
def findSmartDevice(smartDeviceName, availableDeviceNames, availableDeviceBTAddresses):
    print fullStamp() + " findSmartDevices()"
    Ndevices = len(availableDeviceNames)
    smartDeviceNames = []
    smartDeviceBTAddresses = []
    for i in range(0,Ndevices):
        deviceName = availableDeviceNames[i]
        if deviceName == smartDeviceName:
            smartDeviceNames.append(availableDeviceNames[i])
            smartDeviceBTAddresses.append(availableDeviceBTAddresses[i])
    print fullStamp() + " Smart Devices found (names): " + str(smartDeviceNames)
    print fullStamp() + " Smart Devices found (addresses): " + str(smartDeviceBTAddresses)
    return smartDeviceNames, smartDeviceBTAddresses

# Search Available Serial Ports
#   This function was designed to find available virtual serial communication ports on a windows computer
#   The program simply looks for the available ports and adds a port to the list
#   Input   ::  None
#   Output  ::  {String}    "portName"
def nextAvailablePort():
    usedPorts = serial.tools.list_ports.comports()                                                          # Import information about COM ports from the system
    lastPort, description, hwid = usedPorts[len(usedPorts)-1]                                               # Extract the port name, among other parameters, from the last found port
    lastPortNumber = int(lastPort[3:len(lastPort)])                                                         # Based on the port name of the last detected port (assumed to be in use), the program creates a new port
    nextAvailablePort = "COM" + str(lastPortNumber + 1)                                                     # ...
    return nextAvailablePort                                                                                # Returns the full string defining the new port                                                                      # Return RFObject or list of objects

def nextAvailableBTPort():
    print fullStamp() + " nextAvailableBTPort()"                                                            # Terminal message signaling execution of the function
    usedPorts = serial.tools.list_ports.comports()                                                          # ...
    for i in range(0,len(usedPorts)):                                                                       # Loop through found ports...
        port, description, hwid = usedPorts[i]                                                              # Read port-name, description, and hwid from each found port...
        comType = "Bluetooth"                                                                               # String that will be used to find Bluetooth ports by string comparison
        if description[21:30] == comType:                                                                   # If match found...
            portNumber = int(port[3:len(port)])
            availableBTPort = "COM" + str(portNumber)                                                       # An available bluetooth port is said to be found
            break
    print fullStamp() + " Available Bluetooth Port: " + availableBTPort "\n"                                # Terminal message signaling the finding of the available port
    return availableBTPort                                                                                  # Return available port

# Create RFComm Port
def createPort(portName,deviceName,deviceBTAddress,baudrate,timeout):
    #print fullStamp() + " createPort()"
    rfObject = serial.Serial(
        port = portName,
        baudrate = baudrate,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = timeout)
    time.sleep(1)
    outByte = definitions.SOH                                                                               # Send SOH (Start of Heading) byte - see protocolDefinitions.py
    rfObject.write(outByte)
    inByte = rfObject.read(size=1)
    if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response
        print fullStamp() + " Connection Established\n"
        return rfObject
    elif inByte == definitions.NAK:
        print fullStamp() + " NAK device NOT READY\n"

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

