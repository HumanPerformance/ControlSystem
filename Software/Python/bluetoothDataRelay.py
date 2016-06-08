"""
bluetoothDataRelay.py

Fluvio L. Lobo Fenoglietto 06/07/2016
"""

# Import Modules
import os
from os.path import expanduser
import serial

# Variable Definitions
## General Directories
homeDir = expanduser("~")
rootDir = "/root"
if homeDir == rootDir:
          homeDir = "/home/pi"
          # This check and correction is needed for raspbian
consysPyDir = homeDir + "/csec/repos/ControlSystem/Software/Python"
consysPyDataDir = consysPyDir + "/data"
## Instruments Directory
instrumentsConfigFilePath = consysPyDataDir + "/instruments"
instrumentsConfigFileName = "/instrumentconfig.txt"
instrumentsConfigFile = instrumentsConfigFilePath + instrumentsConfigFileName

# Creating Bluetooth Serial Objects
## Identifying Objects from Instruments List
with open(instrumentsConfigFile,'r+') as instrumentsConfigFileObj:
    lines = instrumentsConfigFileObj.readlines()
    #print lines
Nlines = len(lines)
instrumentNames = []
instrumentBTAddress = []
for i in range(0, Nlines-1):
    if lines[i][0] != "#": # This comparison allows for the code to skip the comments within the configuration file
        if lines[i][:10] == "Instrument":
            instrumentNames.append(lines[i].split(";")[1][:-1])
        elif lines[i][:16] == "BluetoothAddress":
            instrumentBTAddress.append(lines[i].split(";")[1][:-1])
print instrumentNames
print instrumentBTAddress
## Using Object Information to Create RFCOMM Ports
Ndevices = len(instrumentNames)
#for i in range(0,Ndevices):
    
## PORTS
#port = "rfcomm0"
## Device Address
#address = "00:06:66:7D:98:58"
## Talking to the terminal
#cmd = "sudo rfcomm bind /dev/" + port + " " + address
## Sending command
#os.system(cmd)

#arduObj = serial.Serial('/dev/rfcomm1',115200)


#arduState = 'unpaired'

#
# unpaired state loop (idle state loop)
#
#while arduState == 'unpaired':
 #   inString = arduObj.readline()
 #   print inString

