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

# Functions ----------------------------------------------------------------------------------------------- # Function Comments

def variableDefinitions():                                                                                  # Function to define global variables needed throughout the code
    global trackingflag                                                                                     # "trackingflag" will be used to trigger the continued reading of data from the serial port
    trackingflag = 0
    global refreshTimer                                                                                     # "refreshTimer" will be used to set the refresh rate for data reading and displaying
    refreshTimer = 500
variableDefinitions()                                                                                       # The variableDefinitions() function is called immediately to define the variables

# Find Stethoscope
def connect2Stethoscope(portName,deviceName,deviceBTAddress,baudrate,timeout):
    print fullStamp() + " findStethoscope()"
    global rfObject
    try:
        rfObject = createPort(portName,deviceName,deviceBTAddress,baudrate,timeout)
        rfObject.close()
        updateConnectionStatus(1)
    except serial.SerialException:
        updateConnectionStatus(2)

def setFilterCallback(rfObject):
    try:
        frequencyValue = int(cornerFrequency.get())
        print frequencyValue
        print chr(frequencyValue)
    except ValueError:
        pass

def startTrackingMicStreamCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    global trackingflag
    trackingflag = 1
    startTrackingMicStream(rfObject)
    updateTrackingData()
    rfObject.close()

def stopTrackingMicStreamCallback(rfObject):
    if rfObject.isOpen() == False:
        rfObject.open()
    global trackingflag
    trackingflag = 2
    stopTrackingMicStream(rfObject)
    updateTrackingData()
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

def updateTrackingData():
    if trackingflag == 0:
        pass
    elif trackingflag == 1:
        if rfObject.isOpen() == False:
            rfObject.open()
        inString = rfObject.readline()
        print inString
        audioTrackingData.configure(text=inString)
    elif trackingflag == 2:
        audioTrackingData.configure(text="NA")
    gui.after(refreshTimer, updateTrackingData)

# Graphical User Interface (GUI) ------------------------------------------------------------------------------ # GUI Callback Comments

gui = Tk()                                                                                                      # Initialization of the window under object name "root"
gui.title("mobile.py")                                                                                          # Title of the window
gui.geometry('450x800+200+200')                                                                                 # Window dimensions in pixels + the distance from the top-left corner of your screen

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

# Stethoscope Signal Filtering
filterSetLabel = Label(text="SET FILTER (Hz)",
                       anchor = W,
                       justify=LEFT)
filterSetLabel.place(x=5,y=150)                                                                                 
filterSetLabel.config(height=1,width=20)                                                                        

# Stethoscope tracking
audioTrackingLabel = Label(text="HEART BEAT TRACKING",
                            anchor=W,                                                                           
                            justify=LEFT)                                                                       
audioTrackingLabel.place(x=5,y=275)                                                                            
audioTrackingLabel.config(height=1,width=20)                                                               

# Tracking Data
audioTrackingData = Label(text="NA",
                          anchor=W,
                          justify=LEFT)
audioTrackingData.place(x=200,y=325)
audioTrackingData.config(height=1,width=20)

# Stethoscope recording
startRecordingLabel = Label(text="AUDIO RECORDING",
                            anchor=W,                                                                           
                            justify=LEFT)                                                                       
startRecordingLabel.place(x=5,y=475)                                                                            
startRecordingLabel.config(height=1,width=20)                                                                 

# Normal Hear Beat 
startPlaybackNormalLabel = Label(text="NORMAL HEART BEAT",
                                 anchor=W,
                                 justify=LEFT)                                                                  
startPlaybackNormalLabel.place(x=5,y=575)                                                                       
startPlaybackNormalLabel.config(height=1,width=20)                                                             

# Early Systolic Murmur
startPlaybackMurmurLabel = Label(text="EARLY SYSTOLIC MURMUR",
                                 anchor=W,
                                 justify=LEFT)                                                                  
startPlaybackMurmurLabel.place(x=5,y=675)                                                                       
startPlaybackMurmurLabel.config(height=1,width=50)                                                             

# Action Buttons ---------------------------------------------------------------------------------------------------------- # Buttons Commnets
# Find Smart Device Button
searchDevicesButton = Button(text="Find Stethoscope",                                                                       # Button text
                             #command=lambda: connect2Stethoscope("COM15","RNBT-76E6","00:06:66:86:76:E6"))                 # Button action command (Fluvio's PC)
                             command=lambda: connect2Stethoscope("COM71","RNBT-76E6","00:06:66:86:76:E6",115200,25))        # Button action command (Lab's PC)
searchDevicesButton.place(x=10,y=50)                                                                                        # Button location
searchDevicesButton.config(height=1,width=20)                                                                               # Button dimensions

# Set Filter
filterSetButton = Button(text="Apply",                                                                        
                           command=lambda: setFilterCallback(rfObject))                                         
filterSetButton.place(x=10,y=200)                                                                               
filterSetButton.config(height=1,width=20)                                                                      

# Start Tracking
startTrackingMicStreamButton = Button(text="Start Tracking",                                                                                 
                               command=lambda: startTrackingMicStreamCallback(rfObject))                        
startTrackingMicStreamButton.place(x=10,y=300)                                                                  
startTrackingMicStreamButton.config(height=1,width=20)                                                        

# Stop Tracking
stopTrackingMicStreamButton = Button(text="Stop Tracking",                                                                                
                               command=lambda: stopTrackingMicStreamCallback(rfObject))                       
stopTrackingMicStreamButton.place(x=10,y=350)                                                                 
stopTrackingMicStreamButton.config(height=1,width=20)                                                           

# Start Recording
startRecordingButton = Button(text="Start REC",                                                                                           
                               command=lambda: startRecordingCallback(rfObject))                                
startRecordingButton.place(x=10,y=500)                                                                          
startRecordingButton.config(height=1,width=20)                                                                  

# Stop Recording
stopRecordingButton = Button(text="Stop REC",                                                                                            
                               command=lambda: stopRecordingCallback(rfObject))                                
stopRecordingButton.place(x=200,y=500)                                                                          
stopRecordingButton.config(height=1,width=20)                                                                 

# Playback - Normal Sound (Play)
startPlaybackNormalButton = Button(text="Play NHB",                                                                                       
                               command=lambda: normalHBPlaybackCallback(rfObject))                             
startPlaybackNormalButton.place(x=10,y=600)                                                                    
startPlaybackNormalButton.config(height=1,width=20)                                                            

# Playback - Normal Sound (Stop)
stopPlaybackNormalButton = Button(text="Stop NHB",
                               command=lambda: stopPlaybackCallback())
stopPlaybackNormalButton.place(x=200,y=600)
stopPlaybackNormalButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Play)
startPlaybackMurmurButton = Button(text="Play ES Mumur",
                                   command=lambda: earlyHMPlaybackCallback(rfObject))
startPlaybackMurmurButton.place(x=10,y=700)
startPlaybackMurmurButton.config(height=1,width=20)

# Playback - Early Systolic Mumur (Stop)
stopPlaybackMurmurButton = Button(text="Stop ES Mumur",
                                   command=lambda: stopPlaybackCallback())
stopPlaybackMurmurButton.place(x=200,y=700)
stopPlaybackMurmurButton.config(height=1,width=20)

# Data Entry -------------------------------------------------------------------------------------------------- # Entry Comments
# Set filter
cornerFrequency = StringVar()
filterSetEntry = Entry(textvariable=cornerFrequency)
filterSetEntry.place(x=10,y=175)
filterSetEntry.config(width=24)

# Continuos Calls
gui.after(refreshTimer, updateTrackingData)
gui.mainloop()

