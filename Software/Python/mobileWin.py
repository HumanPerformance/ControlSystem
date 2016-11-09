"""
mobileWin.py

The following function has been designed to create a small graphical user interface for PD3D's smart devices

Fluvio L Lobo Fenoglietto
11/09/2016
"""

# Import Libraries and/or Modules
from Tkinter import *                                   # GUI design libraries
import ttk                                              # ...
from timeStamp import fullStamp
import protocolDefinitions
from bluetoothProtocolWin import findDevices
from bluetoothProtocolWin import findSmartDevice
from bluetoothProtocolWin import nextAvailablePort
from bluetoothProtocolWin import createPort
from stethoscopeProtocol import sdCardCheck

# Functions

# Find Stethoscope
#   Function designed to find a smart stethoscope in range
#   This function coordinates several functions from various imported protocols
#   Input   ::  None
#   Output  ::  {array/list}
def findStethoscope():
    print fullStamp() + " findStethoscope()"
    global smartDeviceName
    global smartDeviceBTAddress
    global rfObject
    availableDeviceNames, availableDeviceBTAddresses = findDevices()
    smartDeviceName, smartDeviceBTAddress = findSmartDevice("RNBT-76E6",availableDeviceNames, availableDeviceBTAddresses)
    portName = nextAvailablePort()
    rfObject = createPort(portName,smartDeviceName,smartDeviceBTAddress)

def printDeviceInfo(smartDeviceName):
    print smartDeviceName

# Graphical User Interface (GUI)

gui = Tk()                                              # Initialization of the window under object name "root"
gui.title("mobile.py")                                  # Title of the window
gui.geometry('450x450+200+200')                         # Window dimensions in pixels + the distance from the top-left corner of your screen

# Information Label
infoLabel = Label(text="SMART STETHOSCOPE")
infoLabel.place(x=10,y=10)

# Action Buttons
# Find Smart Device Button
searchDevicesButton = Button(text="Find Stethoscope", command=findStethoscope)
searchDevicesButton.place(x=10,y=50)

# SD Card Check
searchDevicesButton = Button(text="SD Card Check", command= lambda: sdCardCheck(rfObject))
searchDevicesButton.place(x=10,y=200)


gui.mainloop()

