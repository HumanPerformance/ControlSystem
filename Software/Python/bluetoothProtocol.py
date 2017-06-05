"""
bluetoothProtocol.py

The following module has been created to manage the bluetooth interface between the control system and the connected devices

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

Modified by : Mohammad Odeh
Date        : May 31st, 2017
Changes     : Modified protocol to use PyBluez instead of PySerial

NOTE: Switch from PySerial to PyBluez is still NOT complete.
"""

# Import Libraries and/or Modules
import  bluetooth, os, time, serial
"""
        Implementation of the "bluetooth" module may require the installation of the python-bluez package
        >> sudp apt-get install python-bluez
"""
import  protocolDefinitions as      definitions
from    timeStamp           import  fullStamp

# *************************************************************************
# ======================> PyBluez Dependant Functions <====================
# *************************************************************************

# Create BlueTooth Socket
#   Arguments   :: {string, int}    BT device address, port #
#   Return      :: [object}         BT Socket
def createSocket( bt_addr, port ):
    print( fullStamp() + " createSocket()" )
    if bluetooth.is_valid_address(bt_addr) is True:                 # Check if address is valid
        socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )      # Create a BT socket
        socket.connect( (bt_addr, port) )                           # Connect to socket
        time.sleep(1)
        if socketCheck( socket ) == True:
            return socket
        else:
            print( fullStamp() + " Could NOT instantiate socket" )
            return 0

    else:
        print( fullStamp() + " Invalid BT address" )
        return 0


# BlueTooth Socket Connection Check
#   Arguments   :: {object} BT Socket
#   Return      :: ACK=1 || NAK=0 || OTHER= -1
def socketCheck( socket ):
    outByte = definitions.ENQ
    socket.send(outByte)
    inByte = socket.recv(1)     # recv(buffersize)

    if inByte == definitions.ACK:
        print( fullStamp() + " ACK Connection Established" )
        return 1
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK device NOT READY" )
        return 0

    else:
        print( fullStamp() + " Please troubleshoot device" )
        return -1


# BlueTooth Socket Read Line
#   Read incoming data until EOL character is reached
#   Arguments   :: {object, string} BT Socket, (OPTIONAL)EOL
#   Return      :: {string}         Data transmitted over BlueTooth
def bt_recv_end( socket, EOL=None ):
    inData, inChar = 'null', 'null'
    firstReading = True
    
    if EOL is None:
        # Get rid of any chopped/truncated data
        while inData != ('\n' or '\r' or '\0'):
            inData = socket.recv(1)

        # Read into buffer as long EOL is not reached
        while inChar != ('\n' or '\r' or '\0'):
            # If first reading, store reading directly to buffer
            if firstReading:
                buff = socket.recv(1)
                firstReading = False

            # Else, store reading into inChar then append to buffer
            else:
                inChar = socket.recv(1)
                buff += inChar

        # Return buffer
        return buff.strip('\n')

    else:
        # Get rid of any chopped/truncated data
        while inData != (EOL):
            inData = socket.recv(1)

        # Read into buffer as long EOL is not reached
        while inChar != (EOL):
            # If first reading, store reading directly to buffer
            if firstReading:
                buff = socket.recv(1)
                firstReading = False

            # Else, store reading into inChar then append to buffer
            else:
                inChar = socket.recv(1)
                buff += inChar

        # Return buffer
        return buff.strip(EOL)


# [BETA] A More Robust BlueTooth Socket Read Line
#   [BETA] Read incoming data until an endmarker is reached
#   [BETA] Arguments   :: {object, string} BT Socket, Endmarker (i.e '$5%!d')
#   [BETA] Return      :: {string}         Data transmitted over BlueTooth
'''
def recv_end( socket, EOL ):
    buff = []
    inData = 'null'
    
    while True:
        inData = socket.recv( 8192 )
        
        if EOL in inData:
            buff.append( inData[:inData.find(EOL)] )
            break

        buff.append(inData)
        
        if len(buff) > 1:
            #check if EOL was split
            last_pair = buff[-2] + buff[-1]
            
            if EOL in last_pair:
                buff[-2] = last_pair[:last_pair.find(EOL)]
                buff.pop()
                break
                
    return ''.join(buff)
'''

# Close BlueTooth Socket (Really unnecessary, but why not?)
#   Arguments   :: {object} BT Socket
#   Return      :: -
def closeSocket( socket ):
    print( fullStamp() + " closeBTPort()" )
    socket.close()
    return 1




# ================
# SH Specific Fxns
# ================

#   Create Port
def createSocket_SH( bt_addr, port, deviceName ):
    print( fullStamp() + " createBTPort()" )
    if bluetooth.is_valid_address(bt_addr) is True:                 # Check if address is valid
        socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )      # Create a BT socket
        socket.connect( (bt_addr, port) )                           # Connect to socket
        time.sleep(1)
        socketCheck_SH( socket, deviceName )
        return( socket )
    else:
        print( fullStamp() + " Invalid BT address" )
        return 0

#   Connection Check
def socketCheck_SH( socket, deviceName ):
    inString = socket.recv( len(deviceName) )     # recv(buffersize)
    if inString == deviceName:
        print( fullStamp() + " Connection successfully established with %s" %deviceName )
    else:
        print( fullStamp() + " Sending Stopping Message" )
        print( fullStamp() + " Please troubleshoot devices" )
        socket.send( 's' )
        closeSocket( socket )    


# *************************************************************************
# =====================> PySerial Dependant Functions <====================
# *************************************************************************

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

# Create RFComm Ports
#   This function creates radio-frquency (bluetooth) communication ports for specific devices, using their corresponding address
#   Input   ::  {array/list} "deviceName", "deviceBTAddress"
#   Output  ::  {array/list} "btObjects"
def createPorts(deviceNames, deviceBTAddresses, baudrate, timeout):
    Ndevices = len(deviceNames)                                                              # Determines the number of devices listed
    rfObjects = []                                                                           # Create RF object variable/list (in case of multiple devices)
    for i in range(0,Ndevices):
        portRelease("rfcomm",i)                                                             # The program performs a port-release to ensure that the desired rf port is available
        portBind("rfcomm",i,deviceBTAddresses[i])
        rfObjects.append(serial.Serial(
            port = "/dev/rfcomm" + str(i),
            baudrate = baudrate,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = timeout))
        time.sleep(1)
    return rfObjects

# Create Ports v2
#   This variation of the original create ports function creates multiple ports and verifies connectivity
def createPorts2(deviceNames, deviceBTAddresses, baudrate, timeout, attempts):
    print fullStamp() + " createPorts2()"
    Ndevices = len(deviceNames)
    print fullStamp() + " Connecting to " + str(Ndevices) + " device"
    rfObjects = []
    for i in range(0,Ndevices):
        portNumber = i
        portRelease('rfcomm',portNumber)
        portBind("rfcomm",portNumber,deviceBTAddresses[i])
        rfObjects.append(serial.Serial(
            port = "/dev/rfcomm" + str(portNumber),
            baudrate = baudrate,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = timeout))
        time.sleep(1)
        connectionCheck2(rfObjects,i,rfObjects[i],deviceNames[i],deviceBTAddresses[i],baudrate,timeout,attempts)
        rfObjects[i].close()
    return rfObjects


# Add Port
#   Solution to the dileman of connection checks. In its recursive call, this function only adds the port being checked
def addPort(rfObjects, index, deviceName, deviceBTAddress, baudrate, timeout, attempts):
    print fullStamp() + " addPort()"
    portNumber = index
    portRelease('rfcomm',portNumber)
    portBind("rfcomm",portNumber,deviceBTAddress)
    rfObjects.append(serial.Serial(
        port = "/dev/rfcomm" + str(portNumber),
        baudrate = baudrate,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = timeout))
    time.sleep(1)
    connectionCheck2(rfObjects,index,rfObjects[index],deviceName,deviceBTAddress,baudrate,timeout,attempts)
    rfObjects[i].close()
    return rfObjects

# Connection Check v2
#   Working alternative to connection checks and add port functions
def connectionCheck2(rfObjects,index,rfObject,deviceName,deviceBTAddress,baudrate,timeout,attempts):
    print fullStamp() + " connectionCheck2()"
    if rfObject.isOpen == False:
        rfObject.open()
    inString = rfObject.readline()[:-1]
    if inString == deviceName:
        print fullStamp() + " Connection successfully established with " + deviceName
    else:
        rfObject.close()
        if attempts is not 0:
            return addPort(rfObjects,index,deviceName,deviceBTAddress,baudrate,timeout,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Connection Attempts Limit Reached"
            print fullStamp() + " Please troubleshoot " + deviceName

# Create RFComm Port
#   This function establishes a RF serial communication port
#   Input   ::  {string}    device name
#           ::  {string}    device bluetooth address
#           ::  {int}       baudrate
#           ::  {int}       timeout
#   Output  ::  {object}    serial object

def createPort(deviceName,deviceBTAddress,baudrate,timeout,attempts):
    portRelease("rfcomm",0)                                                             # The program performs a port-release to ensure that the desired rf port is available
    portBind("rfcomm",0,deviceBTAddress)
    rfObject = serial.Serial(
        port = "/dev/rfcomm" + str(0),
        baudrate = baudrate,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = timeout)
    time.sleep(2)
    outByte = definitions.ENQ                                                                               # Send SOH (Start of Heading) byte - see protocolDefinitions.py
    rfObject.write(outByte)
    inByte = rfObject.read(size=1)
    if inByte == definitions.ACK:                                                                           # Check for ACK / NAK response
        print fullStamp() + " ACK Connection Established"
        rfObject.close()
        return rfObject
    elif inByte == definitions.NAK:
        print fullStamp() + " NAK device NOT READY"
    else:
        rfObject.close()
        if attempts is not 0:
            return createPort(deviceName,deviceBTAddress,baudrate,timeout,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Attempts limit reached"
            print fullStamp() + " Please troubleshoot devices"

# Create Port 2
#   This function is a variation of the standard create port function, which establishes a RF serial communication port
#   This variation performs a character or string-based verification with the control system
#   Input   ::  {string}    device name
#           ::  {string}    device bluetooth address
#           ::  {int}       baudrate                        --Communication speed, bits per minute (bpm)
#           ::  {int}       timeout                         --Connection timeout
#           ::  {int}       attempts                        --Number of recursive connection attempts the program will execute
#   Output  ::  {object}    serial object

def createPort2(deviceName,deviceBTAddress,baudrate,timeout,attempts):
    portRelease("rfcomm",0)
    portBind("rfcomm",0,deviceBTAddress)
    rfObject = serial.Serial(
        port = "/dev/rfcomm" + str(0),
        baudrate = baudrate,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = timeout)
    time.sleep(1)
    connectionCheck(rfObject,deviceName,deviceBTAddress,baudrate,timeout,attempts)
    rfObject.close()
    return rfObject

# Create Port -Simple
#   Simplest varient of the create port function
def createPortS(deviceName,portNumber,deviceBTAddress,baudrate,attempts):
    print fullStamp() + " createPortS()"
    portRelease("rfcomm",portNumber)
    portBind("rfcomm",portNumber,deviceBTAddress)
    rfObject = serial.Serial(
        port = "/dev/rfcomm" + str(portNumber),
        baudrate = baudrate)
    time.sleep(1)
    connectionCheckS(rfObject,deviceName,portNumber,deviceBTAddress,baudrate,attempts)
    rfObject.close()
    return rfObject

# Connection Check
#   The following function verifies the connection to the desired device.
#   The current iteration of this function uses character/string communication between the control system and the connected device.
#   Input   ::  {object}    serial object
#           ::  {string}    device name
#           ::  {int}       attempts
#   Output  ::  {string}    terminal messages

def connectionCheck(rfObject,deviceName,deviceBTAddress,baudrate,timeout,attempts):
    print fullStamp() + " connectionCheck()"
    inString = rfObject.readline()[:-1]
    if inString == deviceName:
        print fullStamp() + " Connection successfully established with " + deviceName
    else:
        rfObject.close()
        if attempts is not 0:
            return createPort2(deviceName,deviceBTAddress,baudrate,timeout,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Connection Attempts Limit Reached"
            print fullStamp() + " Please troubleshoot " + deviceName

# Connection Check -Simple
#   Simplest variant of the connection check functions
def connectionCheckS(rfObject,deviceName,portNumber,deviceBTAddress,baudrate,attempts):
    print fullStamp() + " connectionCheck()"
    inString = rfObject.readline()[:-1]
    if inString == deviceName:
        print fullStamp() + " Connection successfully established with " + deviceName
    else:
        if rfObject.is_open == False:
            rfObject.open()
        print fullStamp() + " Sending Stopping Message"
        rfObject.write('s')
        rfObject.close()
        if attempts is not 0:
            return createPortS(deviceName,portNumber,deviceBTAddress,baudrate,attempts-1)
        elif attempts is 0:
            print fullStamp() + " Connection Attempts Limit Reached"
            print fullStamp() + " Please troubleshoot " + deviceName


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

