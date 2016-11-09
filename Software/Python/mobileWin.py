"""
mobile.py
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


# Functions

# Find Stethoscope
#   Function designed to find a smart stethoscope in range
#   This function coordinates several functions from various imported protocols
#   Input   ::  None
#   Output  ::  {array/list}
def findStethoscope():
    print fullStamp() + " findStethoscope()"
    global smartDeviceName
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
searchDevicesButton = Button(text="Find Stethoscope", command=findStethoscope)
searchDevicesButton.place(x=10,y=50)

# Action Buttons
searchDevicesButton = Button(text="Print Device Name", command= lambda: printDeviceInfo(smartDeviceName))
searchDevicesButton.place(x=10,y=200)


gui.mainloop()

