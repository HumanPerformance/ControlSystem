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
from timeStamp import fullStamp
from bluetoothProtocolWin import findDevices
from bluetoothProtocolWin import findSmartDevice
from bluetoothProtocolWin import nextAvailableBTPort
from bluetoothProtocolWin import createPort

from thermometerProtocol import statusEnquiry
#from thermometerProtocol import systemCheck
from thermometerProtocol import debugModeON
from thermometerProtocol import debugModeOFF
from thermometerProtocol import normalOP
from thermometerProtocol import startSIM_000
from thermometerProtocol import startSIM_001

import ttk                                              # ...
import protocolDefinitions
import sys

# Functions ----------------------------------------------------------------------------------------------- # Function Comments

def findDevicesCallback():
    findDevices()

def nextAvailableBTPortCallback():
    nextAvailableBTPort()

# Find Thermometer
def connect2Thermometer(portName,deviceName,deviceBTAddress,baudrate,timeout):
    print fullStamp() + " findThermometer()"
    global rfObject
    rfObject = createPort(portName,deviceName,deviceBTAddress,baudrate,timeout)
    rfObject.close()

def statusEnquiryCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    statusEnquiry(rfObject)
    rfObject.close()

'''
def systemCheckCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    systemCheck(rfObject)
    rfObject.close()
'''

def debugModeONCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    debugModeON(rfObject)
    rfObject.close()

def debugModeOFFCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    debugModeOFF(rfObject)
    rfObject.close()

def normalOPCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    normalOP(rfObject)
    rfObject.close()

def startSIM_000Callback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startSIM_000(rfObject)
    rfObject.close()

def startSIM_001Callback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startSIM_001(rfObject)
    rfObject.close()

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        if not exit_thread:
            self.widget.insert(END,string)
            self.widget.see(END)

    
# Graphical User Interface (GUI) ------------------------------------------------------------------ # GUI Callback Comments

gui = Tk()                                                                                          # Initialization of the window under object name "root"
gui.title("SMART Thermometer")                                                                              # Title of the window
gui.geometry('450x450+200+200')                                                                     # Window dimensions in pixels + the distance from the top-left corner of your screen

exit_thread= False
root = Tk()
text = Text(root)
text.pack()
sys.stdout = Std_redirector(text)

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
operationModesLabel.place(x=5,y=225)                                                                # ...
operationModesLabel.config(height=1,width=20)                                                       # ...

# System Check Lable
systemCheckLabel = Label(text="System Check",
                            anchor=W,                                                               # ...
                            justify=LEFT)                                                           # ...
systemCheckLabel.place(x=5,y=340)                                                                   # ...
systemCheckLabel.config(height=1,width=20)                                                          # ...

# Action Buttons ---------------------------------------------------------------------------------- # Buttons Commnets

# Start Simulation 1
startSIM_000Button = Button(text="Simulation 1 (Fever)",                                            # Button text                           
                               command=lambda: startSIM_000Callback(rfObject))                      # Button action command
startSIM_000Button.place(x=70,y=250)                                                                # Button location
startSIM_000Button.config(height=1,width=20)                                                        # Button dimensions

# Start Simulation 2
startSIM_001Button = Button(text="Simulation 2 (Hypothermia)",                                      # ...                           
                               command=lambda: startSIM_001Callback(rfObject))                      # ...
startSIM_001Button.place(x=230,y=250)                                                               # ...
startSIM_001Button.config(height=1,width=20)

# Start Normal Operation
normalOPButton = Button(text="Normal Opeartion",                                                    # ...
                           command=lambda: normalOPCallback(rfObject))                              # ...
normalOPButton.place(x=150,y=285)                                                                   # ...
normalOPButton.config(height=1,width=20)                                                            # ...

# Status Enquiry
statsEnquiryButton = Button(text="Status Enquiry",                                                  # ...
                           command=lambda: statusEnquiryCallback(rfObject))                         # ...
statsEnquiryButton.place(x=30,y=365)                                                                # ...
statsEnquiryButton.config(height=1,width=15)                                                        # ...

# Find Devices
findDevicesButton = Button(text="Find Devices",                                                     # ...
                           command=lambda: findDevicesCallback())                                   # ...
findDevicesButton.place(x=170,y=365)                                                                # ...
findDevicesButton.config(height=1,width=15)

#Debug Mode ON
debugModeONButton = Button(text="Debug Mode ON",                                                    # ...
                           command=lambda: debugModeONCallback(rfObject))                           # ...
debugModeONButton.place(x=100,y=400)                                                                # ...
debugModeONButton.config(height=1,width=15) 

#Debug Mode OFF
debugModeOFFButton = Button(text="Debug Mode OFF",                                                  # ...
                           command=lambda: debugModeOFFCallback(rfObject))                          # ...
debugModeOFFButton.place(x=240,y=400)                                                               # ...
debugModeOFFButton.config(height=1,width=15) 

# Find Smart Device Button
searchDevicesButton = Button(text="Find Thermometer",
                             command=lambda: connect2Thermometer("COM22","SmartThermometer-7701","00:06:66:86:77:01", 115200, 5))   #Lab Computer
                             #command=lambda: connect2Thermometer("COM24","RNBT-7712","00:06:66:86:77:12", 115200, 5))   #Lab Computer
                             #command=lambda: connect2Thermometer("COM5","RNBT-76C5","00:06:66:86:76:C5", 115200, 5))   #Jack's Laptop
searchDevicesButton.place(x=310,y=365)
searchDevicesButton.config(height=1,width=15)

# Next Available BT Port
nextAvailableBTPortButton = Button(text="Next Available BT Port",                                   # ...
                           command=lambda: nextAvailableBTPortCallback())                           # ...
nextAvailableBTPortButton.place(x=160,y=120)                                                        # ...
nextAvailableBTPortButton.config(height=1,width=20)                                                 # ...


'''
#System Check
systemCheckButton = Button(text="System Check",                                                     # ...
                           command=lambda: systemCheckCallback(rfObject))                           # ...
systemCheckButton.place(x=160,y=120)                                                                # ...
systemCheckButton.config(height=1,width=15)                                                         # ...
'''


gui.mainloop()

