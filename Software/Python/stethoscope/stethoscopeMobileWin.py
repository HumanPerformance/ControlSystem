"""
mobileWin.py

The following function has been designed to create a small graphical user interface for PD3D's smart devices

Fluvio L Lobo Fenoglietto
11/09/2016
"""

# Import Libraries and/or Modules
from Tkinter import *                                   # GUI design libraries
import time
from timeStamp import fullStamp
import stethoscopeDefinitions as definitions
import serial
from serial import SerialException
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

import ttk
import sys

# Functions ----------------------------------------------------------------------------------------------- # Function Comments                                                                                   # The variableDefinitions() function is called immediately to define the variables

def connect2Stethoscope(portName,deviceName,deviceBTAddress,baudrate,timeout):
    print fullStamp() + " findThermometer()"
    global rfObject
    try:
        rfObject = createPort(portName,deviceName,deviceBTAddress,baudrate,timeout)
        rfObject.close()
        updateConnectionStatus(1)
    except serial.SerialException:
        updateConnectionStatus(2)
"""
def setFilterCallback(rfObject):
    try:
        frequencyValue = int(cornerFrequency.get())
        print frequencyValue
        print chr(frequencyValue)
    except ValueError:
        pass
"""
def startTrackingMicStreamCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    startTrackingMicStream(rfObject)
    continueTracking()
    rfObject.close()

def continueTracking():
    if rfObject.isOpen() == False:
        rfObject.open()
    inString = rfObject.readline()
    print inString + " bpm"
    rfObject.close()
    gui.after(200, continueTracking)

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

def updateConnectionStatus(flag):
    if flag == 1:
        connectionStatus.configure(text="Device found, Port created")
    elif flag == 2:
        connectionStatus.configure(text="Cannot Connect - Reboot!")

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        if not exit_thread:
            self.widget.insert(END,string)
            self.widget.see(END)

# Graphical User Interface (GUI) ------------------------------------------------------------------------------ # GUI Callback Comments

gui = Tk()                                                                                                      # Initialization of the window under object name "root"
gui.title("mobile.py")                                                                                          # Title of the window
gui.geometry('450x700+200+200')                                                                                # Window dimensions in pixels + the distance from the top-left corner of your screen

exit_thread = False
root = Tk()
text = Text(root)
text.pack()
sys.stdout = Std_redirector(text)

# Labels ------------------------------------------------------------------------------------------------------ # Labels Comments
# Information Label
infoLabel = Label(text="SMART STETHOSCOPE",                                                                     # Label title
                  anchor=W,                                                                                     # Label anchor
                  justify=LEFT)                                                                                 # Text justification
infoLabel.place(x=10,y=10)                                                                                      # Label location
infoLabel.config(height=1,width=20)                                                                             # Label dimensions

# Connection Status
connectionStatus = Label(text="NA",
                         anchor=W,
                         justify=LEFT)
connectionStatus.place(x=200,y=55)
connectionStatus.config(height=1,width=100) 
"""
# Stethoscope Signal Filtering
filterSetLabel = Label(text="SET FILTER (Hz)",
                       anchor = W,
                       justify=LEFT)
filterSetLabel.place(x=5,y=150)                                                                                 
filterSetLabel.config(height=1,width=20)                                                                        
"""
# Stethoscope tracking
audioTrackingLabel = Label(text="HEART BEAT TRACKING",
                            anchor=W,                                                                           
                            justify=LEFT)                                                                       
audioTrackingLabel.place(x=5,y=175)                                                                            
audioTrackingLabel.config(height=1,width=20)                                                               
"""
# Tracking Data
audioTrackingData = Label(text="NA",
                          anchor=W,
                          justify=LEFT)
audioTrackingData.place(x=200,y=325)
audioTrackingData.config(height=2,width=20)
audioTrackingData.config(font=("Arial",24))
"""
# Stethoscope recording
startRecordingLabel = Label(text="AUDIO RECORDING",
                            anchor=W,                                                                           
                            justify=LEFT)                                                                       
startRecordingLabel.place(x=5,y=375)                                                                            
startRecordingLabel.config(height=1,width=20)                                                                 

# Normal Heart Beat 
startPlaybackNormalLabel = Label(text="NORMAL HEART BEAT",
                                 anchor=W,
                                 justify=LEFT)                                                                  
startPlaybackNormalLabel.place(x=5,y=475)                                                                       
startPlaybackNormalLabel.config(height=1,width=20)                                                             

# Early Systolic Murmur
startPlaybackMurmurLabel = Label(text="EARLY SYSTOLIC MURMUR",
                                 anchor=W,
                                 justify=LEFT)                                                                  
startPlaybackMurmurLabel.place(x=5,y=575)                                                                       
startPlaybackMurmurLabel.config(height=1,width=50)                                                             

# Action Buttons ---------------------------------------------------------------------------------------------------------- # Buttons Commnets
# Find Smart Device Button
searchDevicesButton = Button(text="Find Stethoscope",
                             command=lambda: connect2Stethoscope("COM86","RNBT-76E6","00:06:66:86:60:8C",115200,25))
searchDevicesButton.place(x=10,y=50)
searchDevicesButton.config(height=1,width=20)
"""
# Set Filter
filterSetButton = Button(text="Apply",                                                                        
                           command=lambda: setFilterCallback(rfObject))                                         
filterSetButton.place(x=10,y=200)                                                                               
filterSetButton.config(height=1,width=20)                                                                      
"""
# Start Tracking
startTrackingMicStreamButton = Button(text="Start Tracking",                                                                                 
                               command=lambda: startTrackingMicStreamCallback(rfObject))                        
startTrackingMicStreamButton.place(x=10,y=200)                                                                  
startTrackingMicStreamButton.config(height=1,width=20)                                                        

# Stop Tracking
stopTrackingMicStreamButton = Button(text="Stop Tracking",                                                                                
                               command=lambda: stopTrackingMicStreamCallback(rfObject))                       
stopTrackingMicStreamButton.place(x=200,y=200)                                                                 
stopTrackingMicStreamButton.config(height=1,width=20)                                                           

# Start Recording
startRecordingButton = Button(text="Start REC",                                                                                           
                               command=lambda: startRecordingCallback(rfObject))                                
startRecordingButton.place(x=10,y=400)                                                                          
startRecordingButton.config(height=1,width=20)                                                                  

# Stop Recording
stopRecordingButton = Button(text="Stop REC",                                                                                            
                               command=lambda: stopRecordingCallback(rfObject))                                
stopRecordingButton.place(x=200,y=400)                                                                          
stopRecordingButton.config(height=1,width=20)                                                                 

# Playback - Normal Sound (Play)
startPlaybackNormalButton = Button(text="Play NHB",                                                                                       
                               command=lambda: normalHBPlaybackCallback(rfObject))                             
startPlaybackNormalButton.place(x=10,y=500)                                                                    
startPlaybackNormalButton.config(height=1,width=20)                                                            

# Playback - Normal Sound (Stop)
stopPlaybackNormalButton = Button(text="Stop NHB",
                               command=lambda: stopPlaybackCallback())
stopPlaybackNormalButton.place(x=200,y=500)
stopPlaybackNormalButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Play)
startPlaybackMurmurButton = Button(text="Play ES Mumur",
                                   command=lambda: earlyHMPlaybackCallback(rfObject))
startPlaybackMurmurButton.place(x=10,y=600)
startPlaybackMurmurButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Stop)
stopPlaybackMurmurButton = Button(text="Stop ES Mumur",
                                   command=lambda: stopPlaybackCallback())
stopPlaybackMurmurButton.place(x=200,y=600)
stopPlaybackMurmurButton.config(height=1,width=20)

# Data Entry -------------------------------------------------------------------------------------------------- # Entry Comments
"""
# Set filter
cornerFrequency = StringVar()
filterSetEntry = Entry(textvariable=cornerFrequency)
filterSetEntry.place(x=10,y=175)
filterSetEntry.config(width=24)
"""
# Continuos Calls
gui.after(200, continueTracking)
gui.mainloop()

