"""
stethoscopeProtocol.py

The following module has been created to manage the device-specific interface between the stethoscope and the control system modules

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/01/2016

Modified by : Mohammad Odeh
Date        : Nov. 15th, 2017, Year of Our Lord

Changes:-
    MODIFIED: protocol uses PyBluez instead of PySerial
    ADDED   : cleaned up code and added extra functions
    
"""

# Import Libraries and/or Modules
from    configurationProtocol       import  *
from    bluetoothProtocol_teensy32  import  *
from    timeStamp                   import  fullStamp
import  stethoscopeDefinitions      as      definitions
import  os, sys, serial
import  random


def systemCheck( rfObject ):
    """
    System Check:
    This function commands the connected stethoscope to perform
    a "systems check", which may consist on a routine verification
    of remote features.
    """
    
    print( fullStamp() + " systemCheck()" )                                                             # Print function name

    outByte = definitions.SDCHECK                                                                           # Send CHK / System Check command - see protocolDefinitions.py                     
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                                                                           # Check for response

    if inByte == definitions.ACK:                                                                       # Check for ACK / NAK response found through sendUntilRead()
        print( fullStamp() + " ACK SD Card Check Passed" )                                              # If the SD card check is successful, the remote device sends a ACK
        print( fullStamp() + " ACK Device Ready" )                                                      # ACK, in this case, translates to DEVICE READY

    elif inByte == definitions.NAK:                                                                     # Check for ACK / NAK response found through sendUntilRead()
        print( fullStamp() + " NAK SD Card Check Failed" )                                              # If the SD card check fails, the remote device sends a NAK
        print( fullStamp() + " NAK Device NOT Ready" )                                                  # NAK, in this case, translates to DEVICE NOT READY

#
# Diagnostic Functions
#       These functions deal with the status of the hardware
#

def deviceID( rfObject ):
    """
    Device Identification:
    This function requests the identification of the connected device.
    """
    
    outBytes = [definitions.DC1, definitions.DC1_DEVICEID]                                              # Store the sequence of bytes associated with the operation, function, feature
    inBytes = []
    for i in range(0,len(outBytes)):                                                                    # For loop for the sequential delivery of bytes using the length of the sequence for the range
        rfObject.send(outBytes[i])
        if i == (len(outBytes) - 1):                                                                    # On the last byte, the program reads the response
            for i in range(0,3):
                inBytes.append(rfObject.recv(1))

    print inBytes

#
# Generate Rand. String
#
def genRandString( length ):
    """
    Generate Rand. String
    This function generates a random string to use as filename
    """

    print( fullStamp() + " genRandString() " )

    #options = 'abcdefghijklmnopqrstuvwxyz'
    options = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randString = ''.join( random.choice( options ) for i in range( length ) )

    return randString


#
# Parse String
#
def parseString( rfObject, outString ):
    """
    Parse String
    This function passes a string over bluetooth
    """

    print( fullStamp() + " parseString()" )

    outByte = definitions.PSTRING
    rfObject.send( outByte )
    
    rfObject.send( outString )
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device READY" )
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device NOT READY" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


#
# SD Card Check
#
def sdCardCheck( rfObject ):
    """
    SD Card Check:
    This function commands the connected stethoscope
    to perform a check on the connected SD card.
    """
    
    print( fullStamp() + " sdCardCheck()" )

    outBytes = [definitions.DC1, definitions.DC1_SDCHECK]

    for i in range( 0, len(outBytes) ):
        rfObject.send( outBytes[i] )
        if i == (len(outBytes) - 1):
            inByte = rfObject.recv(1)

    if inByte == definitions.ACK:
        print( fullStamp() + " ACK SD Card Check Passed" )
        print( fullStamp() + " ACK Device Ready" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK SD Card Check Failed" )
        print( fullStamp() + " NAK Device NOT Ready" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def statusEnquiry( rfObject ):
    """
    State Enquiry:
    This function requests the status of the stethoscope.
    """
    
    print( fullStamp() + " statusEnquiry()" )

    outByte = definitions.ENQ                    
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device READY" )
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device NOT READY" )

    elif inByte == definitions.STARTREC:
        print( fullStamp() + " Device RECORDING" )

    elif inByte == definitions.STARTPLAYING:
        print( fullStamp() + " Device PLAYING" )

    elif inByte == definitions.STARTHBMONITORING:
        print( fullStamp() + " Device MONITORING" )

    elif inByte == definitions.STARTBLENDING:
        print( fullStamp() + " Device BLENDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

#
# set to idle
def setToIdle( rfObject ):
    """
    Set to Idle
    Sets the stethoscope to IDLE mode
    """
    
    print( fullStamp() + " setToIdle()" )                                                             # Print function name

    outByte = definitions.SETIDLE                                                                           # Send CHK / System Check command - see protocolDefinitions.py                     
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                                                                           # Check for response

    if inByte == definitions.ACK:                                                                       # Check for ACK / NAK response found through sendUntilRead()
        print( fullStamp() + " ACK Stethoscope Set to IDLE" )                                              # If the SD card check is successful, the remote device sends a ACK
        print( fullStamp() + " ACK Device Ready" )                                                      # ACK, in this case, translates to DEVICE READY

    elif inByte == definitions.NAK:                                                                     # Check for ACK / NAK response found through sendUntilRead()
        print( fullStamp() + " NAK Stethoscope CANNOT be set to IDLE" )                                              # If the SD card check fails, the remote device sends a NAK
        print( fullStamp() + " NAK Device NOT Ready" )   

#
# Operational Functions
#       These functions deal with the normal operation of the device
#

def sendRaw( rfObject ):
    """
    Send Raw
    This function requests the retrieval of raw data from the SD card.
    """
    
    print( fullStamp() + " sendRaw()" )

    #outByte = definitions.SENDRAW
    outByte = definitions.SENDWAV 
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device READY" )
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device NOT READY" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

#
# Device-Specific Functions
#       These functions deal with the device-specific operation or features
#

#
# Set Recording Mode
#
def setRecordingMode( rfObject, recMode ):
    """
    Parse/Set Recording Mode
    This function passes a string that will set the recording mode of the stethoscope
    """

    print( fullStamp() + " setRecordingMode()" )

    outByte = definitions.RECMODE
    rfObject.send( outByte )

    outString = str( recMode )
    rfObject.send( outString )
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device RECEIVED RECORDING MODE" )
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device DID NOT RECEIVE RECORDING MODE" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

def startRecording( rfObject ):
    """
    Start Recording:
    This function commands the connected stethoscope to begin recording audio.
    """
    
    print( fullStamp() + " startRecording()" )

    outByte = definitions.STARTCREC                  
    rfObject.send(outByte)
    inByte = rfObject.recv(1)
    
    if inByte == definitions.ACK:                   
        print( fullStamp() + " ACK Stethoscope will START RECORDING" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START RECORDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

def startCustomRecording( rfObject, outString ):
    """
    Start Custom Recording
    Begins recording to be saved undr a custom filename
    """

    print( fullStamp() + " startCustomRecording()" )
    print( fullStamp() + " Parsing STARTCREC Byte" )
    outByte = definitions.STARTCREC
    rfObject.send( outByte )

    #print( fullStamp() + " Parsing custom recording string = " + outString )
    rfObject.send( outString )
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device will START RECORDING" )
        print( fullStamp() + " ACK Device will RECORD under the " + outString + " filename")
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT START RECORDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

def startMultiChannelRecording( rfObject, outString ):
    """
    Start Multi Channel Recording
    Begins recording to be saved undr a custom filename
    """

    print( fullStamp() + " startCustomRecording()" )
    print( fullStamp() + " Parsing STARTMREC Byte" )
    outByte = definitions.STARTMREC
    rfObject.send( outByte )
    
    #print( fullStamp() + " Parsing custom recording string = " + outString )
    rfObject.send( outString )
    inByte = rfObject.recv(1)                      

    if inByte == definitions.ACK:                     
        print( fullStamp() + " ACK Device will START RECORDING" )
        print( fullStamp() + " ACK Device will RECORD under the " + outString + " filename")
        return True
    
    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT START RECORDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

def stopRecording( rfObject ):
    """
    Stop Recording:
    This function commands the connected stethoscope to stop recording audio.
    """
    
    print( fullStamp() + " stopRecording()" )

    outByte = definitions.STOPREC                     
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                          

    if inByte == definitions.ACK:                               
        print( fullStamp() + " ACK Stethoscope will STOP RECORDING" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT STOP RECORDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def startMicStream( rfObject ):
    """
    Start Microphone Streaming:
    This function commands the connected stethoscope to begin
    streaming audio from the microphone to the connected speakers.
    """
    
    print( fullStamp() + " startMicStream()" )

    outBytes = [definitions.DC3, definitions.DC3_STARTSTREAM]

    for i in range(0,len(outBytes)):
        rfObject.send(outBytes[i])
        if i == (len(outBytes) - 1):
            inByte = rfObject.recv(1)

    if inByte == definitions.ACK:
        print( fullStamp() + " ACK Stethoscope will START STREAMING" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START STREAMING" )


def startTrackingMicStream( rfObject ):
    """
    Start Tracking Microphone Stream for Peaks:
    This function commands the connected stethoscope to stop streaming
    audio from the microphone and find/detect peaks.
    """
    
    print( fullStamp() + " startTrackingMicStream()" )     

    outByte = definitions.STARTTRACKING      
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                  

    if inByte == definitions.ACK:                  
        print( fullStamp() + " ACK Device will START Tracking" )  

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT START Tracking" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def stopTrackingMicStream( rfObject ):
    """
    Stop Tracking Microphone Stream for Peaks:
    This function commands the connected stethoscope to
    stop finding/detecting peaks.
    """
    
    print( fullStamp() + " stopTrackingMicStream()" )           

    outByte = definitions.STOPTRACKING                 
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                       

    if inByte == definitions.ACK:                                    
        print( fullStamp() + " ACK Device will STOP Tracking" )    

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Device CANNOT STOP Tracking" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

#
# Simulation Functions
#       These functions deal with the simulations corresponding to the connected device
#

def normalHBPlayback( rfObject ):
    """
    Normal Heart Beat Playback:
    This function triggers the playback of a normal heart beat.
    """
    
    print( fullStamp() + " normalHBPlayback()" )       

    outByte = definitions.NORMALHB                   
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                           

    if inByte == definitions.ACK:                
        print( fullStamp() + " ACK Stethoscope will START PLAYBACK of NORMAL HEARTBEAT" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START PLAYBACK of NORMAL HEARTBEAT" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def earlyHMPlayback( rfObject ):
    """
    Early Systolic Heart Murmur:
    This function triggers the playback of an early systolic heart mumur.
    """
    
    print( fullStamp() + " earlyHMPlayback()" )    

    outByte = definitions.ESHMURMUR 
    rfObject.send(outByte)
    inByte = rfObject.recv(1)  

    if inByte == definitions.ACK:       
        print( fullStamp() + " ACK Stethoscope will START PLAYBACK of EARLY SYSTOLIC HEART MUMUR" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START PLAYBACK of EARLY SYSTOLIC HEART MUMUR" ) 

    else:
        print( fullStamp() + " Please troubleshoot device" )


def stopPlayback( rfObject ):
    """
    Stop Playback:
    This function commands the connected stethoscope to stop
    playing an audio file stored within the SD card.
    """
    
    print( fullStamp() + " stopPlayback()" )      

    outByte = definitions.STOPPLAY          
    rfObject.send(outByte)
    inByte = rfObject.recv(1)          

    if inByte == definitions.ACK:               
        print( fullStamp() + " ACK Stethoscope will STOP PLAYBACK" )                                                       

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT STOP PLAYBACK" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def earlyHMBlending( rfObject ):
    """
    Early Systolic Heart Murmur:
    This function triggers the playback of an early systolic heart mumur.
    """
    
    print( fullStamp() + " earlyHMBlending()" )

    outByte = definitions.STARTBLEND    
    rfObject.send(outByte)
    inByte = rfObject.recv(1)             

    if inByte == definitions.ACK:           
        print( fullStamp() + " ACK Stethoscope will START BLENDING of EARLY SYSTOLIC HEART MUMUR" )                                                       

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START BLENDING of EARLY SYSTOLIC HEART MUMUR" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def startBlending( rfObject, fileByte ):
    """
    Start Blending:
    This function starts blending of audio file.
    """
    
    print( fullStamp() + " startBlending()" )         

    outByte = fileByte                                  
    rfObject.send(outByte)
    inByte = rfObject.recv(1)              

    if inByte == definitions.ACK:               
        print( fullStamp() + " ACK Stethoscope will START BLENDING" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START BLENDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


def stopBlending( rfObject ):
    """
    Stop Blending:
    This function stops blending of audio file.
    """
    
    print( fullStamp() + " stopBlending()" )              

    outByte = definitions.STOPBLEND                     
    rfObject.send(outByte)
    inByte = rfObject.recv(1)                                 

    if inByte == definitions.ACK:                   
        print( fullStamp() + " ACK Stethoscope will STOP BLENDING" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT STOP BLENDING" )

    else:
        print( fullStamp() + " Please troubleshoot device" )


#
# Start Simulation
#
def startSimulation( rfObject ):
    """
    Start Simulation:
    This function starts a scripted simulation in the augmented stethoscope.
    """
    
    print( fullStamp() + " startSimulating()" )         

    # check for simulation function call
    outByte = definitions.STARTSIM                                 
    rfObject.send(outByte)
    inByte = rfObject.recv(1)

    if inByte == definitions.ACK:               
        print( fullStamp() + " ACK Stethoscope will START SIMULATING scenario 0" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT START SIMULATING scenario 0" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

    # check for recording function call
    byteCheck( rfObject, 1, 5.0 )

    # check for blending function call
    byteCheck( rfObject, 1, 5.0 )    


# -------------------------------------------------------- #
# Special Function
#
# Byte Check

def byteCheck( rfObject, size, timeout ):

    start_time      = time.time()
    current_time    = 0
    while current_time < timeout :
        inByte = rfObject.recv( size )
        print( fullStamp() + " Received " + inByte.decode( "utf-8" ) )
        if inByte == definitions.ACK:               
            print( fullStamp() + " ACK " )
            break

        elif inByte == definitions.NAK:
            print( fullStamp() + " NAK " )
            break

        current_time = time.time() - start_time
        print( fullStamp() + " Time elapsed = " + str( current_time ) + " sec." )

    if current_time >= timeout :
        print( fullStamp() + " Please troubleshoot device " )

# -------------------------------------------------------- #

#
# Start Simulation
#
def stopSimulation( rfObject ):
    """
    Start Simulation:
    This function starts a scripted simulation in the augmented stethoscope.
    """
    
    print( fullStamp() + " startSimulating()" )         

    outByte = definitions.STOPSIM                                 
    rfObject.send(outByte)
    inByte = rfObject.recv(1)              

    if inByte == definitions.ACK:               
        print( fullStamp() + " ACK Stethoscope will STOP SIMULATING scenario 0" )

    elif inByte == definitions.NAK:
        print( fullStamp() + " NAK Stethoscope CANNOT STOP SIMULATING scenario 0" )

    else:
        print( fullStamp() + " Please troubleshoot device" )

    # check for the STOP recording function call
    byteCheck( rfObject, 1, 5.0 )

    # check for the STOP blending function call
    byteCheck( rfObject, 1, 5.0 )  
