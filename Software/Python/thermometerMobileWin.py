"""
mobileWin.py

The following function has been designed to create a small graphical user interface for PD3D's smart devices

Author: Fluvio L Lobo Fenoglietto
11/09/2016

Modified by: Mohammad Odeh
Adapted to the Smart Thermometer device
Nov. 28th, 2016

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

from thermometerProtocol import statusEnquiry
from thermometerProtocol import systemCheck
from thermometerProtocol import normalOP
from thermometerProtocol import startSIM_000
from thermometerProtocol import startSIM_001

# Functions ----------------------------------------------------------------------------------------------- # Function Comments

# Find Thermometer
def connect2Thermometer(portName,deviceName,deviceBTAddress):
    print fullStamp() + " findThermometer()"
    global rfObject
    rfObject = createPort(portName,deviceName,deviceBTAddress)
    rfObject.close()

def statusEnquiryCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    statusEnquiry(rfObject, 5, 5)
    rfObject.close()

def systemCheckCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    systemCheck(rfObject, 5, 5)
    rfObject.close()

def normalOPCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    normalOP(rfObject, 5, 5)
    rfObject.close()

def startSIM_000Callback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startSIM_000(rfObject, 5, 5)
    rfObject.close()

def startSIM_001Callback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startSIM_001(rfObject, 5, 5)
    rfObject.close()
    
# Graphical User Interface (GUI) ------------------------------------------------------------------ # GUI Callback Comments

gui = Tk()                                                                                          # Initialization of the window under object name "root"
gui.title("mobile.py")                                                                              # Title of the window
gui.geometry('450x450+200+200')                                                                     # Window dimensions in pixels + the distance from the top-left corner of your screen

# Labels ------------------------------------------------------------------------------------------ # Labels Comments
# Information Label
infoLabel = Label(text="SMART Thermometer",                                                         # Label title
                  anchor=W,                                                                         # Label anchor
                  justify=LEFT)                                                                     # Text justification
infoLabel.place(x=10,y=10)                                                                          # Label location
infoLabel.config(height=1,width=20)                                                                 # Label dimensions

# Operation Modes Lable
operationModesLabel = Label(text="Operation Modes",
                       anchor = W,
                       justify=LEFT)
operationModesLabel.place(x=5,y=275)                                                                # ...
operationModesLabel.config(height=1,width=20)                                                       # ...

# System Check Lable
systemCheckLabel = Label(text="System Check",
                            anchor=W,                                                               # ...
                            justify=LEFT)                                                           # ...
systemCheckLabel.place(x=5,y=375)                                                                   # ...
systemCheckLabel.config(height=1,width=20)                                                          # ...

# Action Buttons ---------------------------------------------------------------------------------- # Buttons Commnets

# Start Simulation 1
startSIM_000Button = Button(text="Simulation 1 (Fever)",                                            # Button text                           
                               command=lambda: startSIM_000Callback(rfObject))                      # Button action command
startSIM_000Button.place(x=70,y=300)                                                                # Button location
startSIM_000Button.config(height=1,width=20)                                                        # Button dimensions

# Start Simulation 2
startSIM_001Button = Button(text="Simulation 2 (Hypothermia)",                                      # ...                           
                               command=lambda: startSIM_001Callback(rfObject))                      # ...
startSIM_001Button.place(x=230,y=300)                                                               # ...
startSIM_001Button.config(height=1,width=20)

# Start Normal Operation
normalOPButton = Button(text="Normal Opeartion",                                                    # ...
                           command=lambda: normalOPCallback(rfObject))                              # ...
normalOPButton.place(x=150,y=335)                                                                   # ...
normalOPButton.config(height=1,width=20)                                                            # ...

# Status Enquiry
statsEnquiryButton = Button(text="Status Enquiry",                                                  # ...
                           command=lambda: statusEnquiryCallback(rfObject))                         # ...
statsEnquiryButton.place(x=30,y=400)                                                                # ...
statsEnquiryButton.config(height=1,width=15)                                                        # ...

#System Check
systemCheckButton = Button(text="System Check",                                                     # ...
                           command=lambda: systemCheckCallback(rfObject))                           # ...
systemCheckButton.place(x=170,y=400)                                                                # ...
systemCheckButton.config(height=1,width=15)                                                         # ...

# Find Smart Device Button
searchDevicesButton = Button(text="Find Thermometer",
                             command=lambda: connect2Thermometer("COM7","RNBT-76C5","00:06:66:86:76:C5"))
searchDevicesButton.place(x=310,y=400)
searchDevicesButton.config(height=1,width=15)

gui.mainloop()

