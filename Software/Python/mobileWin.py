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
from stethoscopeProtocol import startPlayback
from stethoscopeProtocol import normalHBPlayback
from stethoscopeProtocol import earlyHMPlayback

# Functions

# Find Stethoscope
def connect2Stethoscope(portName,deviceName,deviceBTAddress):
    print fullStamp() + " findStethoscope()"
    global rfObject
    rfObject = createPort(portName,deviceName,deviceBTAddress)
    rfObject.close()

def sdCardCheckCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    sdCardCheck(rfObject)
    rfObject.close()

def startPlaybackCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startPlayback(rfObject)
    rfObject.close()

def normalHBPlaybackCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    normalHBPlayback(rfObject)
    rfObject.close()

def earlyHMPlaybackCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    earlyHMPlayback(rfObject)
    rfObject.close()

def stopPlaybackCallback():
    if rfObject.isOpen() == False:
        rfObject.open()
    stopPlaying(rfObject)
    rfObject.close()

# Graphical User Interface (GUI)

gui = Tk()                                              # Initialization of the window under object name "root"
gui.title("mobile.py")                                  # Title of the window
gui.geometry('450x450+200+200')                         # Window dimensions in pixels + the distance from the top-left corner of your screen

# Labels
# Information Label
infoLabel = Label(text="SMART STETHOSCOPE")
infoLabel.place(x=10,y=10)
infoLabel.config(height=1,width=20)

# Normal Hear Beat 
startPlayNormalLabel = Label(text="NORMAL HEART BEAT")
startPlayNormalLabel.place(x=5,y=175)
startPlayNormalLabel.config(height=1,width=20)

# Action Buttons
# Find Smart Device Button
searchDevicesButton = Button(text="Find Stethoscope", command=lambda: connect2Stethoscope("COM71","RNBT-76E6","00:06:66:86:76:E6"))
searchDevicesButton.place(x=10,y=50)
searchDevicesButton.config(height=1,width=20)

# SD Card Check
sdCardCheckButton = Button(text="SD Card Check", command=lambda: sdCardCheckCallback(rfObject))
sdCardCheckButton.place(x=10,y=100)
sdCardCheckButton.config(height=1,width=20)

# Playback - Normal Sound (Play)
startPlayNormalButton = Button(text="Play NHB", command=lambda: normalHBPlaybackCallback(rfObject))
startPlayNormalButton.place(x=10,y=200)
startPlayNormalButton.config(height=1,width=20)

# Playback - Normal Sound (Stop)
startStopNormalButton = Button(text="Stop NHB", command=lambda: stopPlaybackCallback())
startStopNormalButton.place(x=200,y=200)
startStopNormalButton.config(height=1,width=20)

# Playback - Early Systolic Mumur
startPlaybackMurmurButton = Button(text="ES Mumur", command=lambda: earlyHMPlaybackCallback(rfObject))
startPlaybackMurmurButton.place(x=10,y=250)
startPlaybackMurmurButton.config(height=1,width=20)

gui.mainloop()

