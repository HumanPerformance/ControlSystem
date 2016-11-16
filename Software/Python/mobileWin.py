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
from stethoscopeProtocol import stopPlayback
from stethoscopeProtocol import startRecording
from stethoscopeProtocol import stopRecording
from stethoscopeProtocol import startTrackingMicStream
from stethoscopeProtocol import stopTrackingMicStream

# Functions ----------------------------------------------------------------------------------------------- # Function Comments

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

def startTrackingMicStreamCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startTrackingMicStream(rfObject)
    rfObject.close()

def stopTrackingMicStreamCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    stopTrackingMicStream(rfObject)
    rfObject.close()

def startRecordingCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startRecording(rfObject)
    rfObject.close()

def stopRecordingCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    stopRecording(rfObject)
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
    stopPlayback(rfObject)
    rfObject.close()

# Graphical User Interface (GUI) ------------------------------------------------------------------------------ # GUI Callback Comments

gui = Tk()                                                                                                      # Initialization of the window under object name "root"
gui.title("mobile.py")                                                                                          # Title of the window
gui.geometry('450x550+200+200')                                                                                 # Window dimensions in pixels + the distance from the top-left corner of your screen

# Labels ------------------------------------------------------------------------------------------------------ # Labels Comments
# Information Label
infoLabel = Label(text="SMART STETHOSCOPE",                                                                     # Label title
                  anchor=W,                                                                                     # Label anchor
                  justify=LEFT)                                                                                 # Text justification
infoLabel.place(x=10,y=10)                                                                                      # Label location
infoLabel.config(height=1,width=20)                                                                             # Label dimensions

# Stethoscope recording
startStreamingLabel = Label(text="AUDIO STREAMING",
                            anchor=W,                                                                           # ...
                            justify=LEFT)                                                                       # ...
startStreamingLabel.place(x=5,y=175)                                                                            # ...
startStreamingLabel.config(height=1,width=20)                                                                   # ...

# Stethoscope recording
startRecordingLabel = Label(text="AUDIO RECORDING",
                            anchor=W,                                                                           # ...
                            justify=LEFT)                                                                       # ...
startRecordingLabel.place(x=5,y=275)                                                                            # ...
startRecordingLabel.config(height=1,width=20)                                                                   # ...

# Normal Hear Beat 
startPlaybackNormalLabel = Label(text="NORMAL HEART BEAT",
                                 anchor=W,
                                 justify=LEFT)                                                                  # ...
startPlaybackNormalLabel.place(x=5,y=375)                                                                       # ...
startPlaybackNormalLabel.config(height=1,width=20)                                                              # ...

# Early Systolic Murmur
startPlaybackMurmurLabel = Label(text="EARLY SYSTOLIC MURMUR",
                                 anchor=W,
                                 justify=LEFT)                                                                  # ...
startPlaybackMurmurLabel.place(x=5,y=475)                                                                       # ...
startPlaybackMurmurLabel.config(height=1,width=50)                                                              # ...

# Action Buttons ---------------------------------------------------------------------------------------------- # Buttons Commnets
# Find Smart Device Button
searchDevicesButton = Button(text="Find Stethoscope",                                                           # Button text
                             command=lambda: connect2Stethoscope("COM15","RNBT-76E6","00:06:66:86:76:E6"))      # Button action command (Fluvio's PC)
                             #command=lambda: connect2Stethoscope("COM71","RNBT-76E6","00:06:66:86:76:E6"))     # Button action command (Lab's PC)
searchDevicesButton.place(x=10,y=50)                                                                            # Button location
searchDevicesButton.config(height=1,width=20)                                                                   # Button dimensions

# SD Card Check
sdCardCheckButton = Button(text="SD Card Check",                                                                # ...
                           command=lambda: sdCardCheckCallback(rfObject))                                       # ...
sdCardCheckButton.place(x=10,y=100)                                                                             # ...
sdCardCheckButton.config(height=1,width=20)                                                                     # ...

# Start Streaming
startTrackingMicStreamButton = Button(text="Start Stream",                                                      # ...                           
                               command=lambda: startTrackingMicStreamCallback(rfObject))                        # ...
startTrackingMicStreamButton.place(x=10,y=200)                                                                  # ...
startTrackingMicStreamButton.config(height=1,width=20)                                                          # ...

# Stop Streaming
stopTrackingMicStreamButton = Button(text="Stop Stream",                                                        # ...                           
                               command=lambda: stopTrackingMicStreamCallback(rfObject))                         # ...
stopTrackingMicStreamButton.place(x=200,y=200)                                                                  # ...
stopTrackingMicStreamButton.config(height=1,width=20)                                                           # ...

# Start Recording
startRecordingButton = Button(text="Start REC",                                                                 # ...                           
                               command=lambda: startRecordingCallback(rfObject))                                # ...
startRecordingButton.place(x=10,y=300)                                                                          # ...
startRecordingButton.config(height=1,width=20)                                                                  # ...

# Stop Recording
stopRecordingButton = Button(text="Stop REC",                                                                   # ...                           
                               command=lambda: stopRecordingCallback(rfObject))                                 # ...
stopRecordingButton.place(x=200,y=300)                                                                          # ...
stopRecordingButton.config(height=1,width=20)                                                                   # ...

# Playback - Normal Sound (Play)
startPlaybackNormalButton = Button(text="Play NHB",                                                                 # ...                           
                               command=lambda: normalHBPlaybackCallback(rfObject))                              # ...
startPlaybackNormalButton.place(x=10,y=400)                                                                         # ...
startPlaybackNormalButton.config(height=1,width=20)                                                                 # ...

# Playback - Normal Sound (Stop)
stopPlaybackNormalButton = Button(text="Stop NHB",
                               command=lambda: stopPlaybackCallback())
stopPlaybackNormalButton.place(x=200,y=400)
stopPlaybackNormalButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Play)
startPlaybackMurmurButton = Button(text="Play ES Mumur",
                                   command=lambda: earlyHMPlaybackCallback(rfObject))
startPlaybackMurmurButton.place(x=10,y=500)
startPlaybackMurmurButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Stop)
stopPlaybackMurmurButton = Button(text="Stop ES Mumur",
                                   command=lambda: stopPlaybackCallback())
stopPlaybackMurmurButton.place(x=200,y=500)
stopPlaybackMurmurButton.config(height=1,width=20)

gui.mainloop()

