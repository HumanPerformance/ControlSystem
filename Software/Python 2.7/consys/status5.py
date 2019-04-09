"""
status4.3bpc.py

...
            
Fluvio L. Lobo Fenoglietto 04/29/2018
"""

# ========================================================================================= #
# Import Libraries and/or Modules
# ========================================================================================= #
# Python modules
import  sys
import  os
import  serial
import  time
import  pexpect
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs
from    threading                   import Thread
from    Queue                       import Queue

# PD3D modules
from    configurationProtocol                   import *

paths, pythonDir, consDir, stetDir, shanDir, sholDir, bpcuDir, outputDir, dataDir = definePaths()
response = addPaths(paths)

from    timeStamp                   import fullStamp as fS
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *
from    stethoscopeProtocol         import *


executionTimeStamp  = fS()

# ========================================================================================= #
# Functions
# ========================================================================================= #
def create_status_directories( consDir, executionTimeStamp ):
    print( "{} Writting status to file ".format(fS()) )

    statusDir = consDir + "status/"
    if( path.exists( statusDir ) == False ):
        print( "{} Status directory not present ".format(fS()) )
        print( "{} Generating status directory ".format(fS()) )
        makedirs( statusDir )
    else:
        print( "{} Found status directory ".format(fS()) )

    stampedDir = statusDir + executionTimeStamp + "/"
    if( path.exists( stampedDir ) == False ):
        print( "{} Time-stamped directory not present ".format(fS()) )
        print( "{} Generating time-stamped directory ".format(fS()) )
        makedirs( stampedDir )
    else:
        print( "{} Found time-stamped directory ".format(fS()) )

    return statusDir, stampedDir

def write_status_to_file( status_filename, message ):
    with open( status_filename, 'a' ) as dataFile:
        dataFile.write( fS() + " " + message )

def check_ST_holder( smartholder_STH, consDir, executionTimeStamp ):

    holder_data = "{}".format( smartholder_STH.readline() )                              # Read until timeout is reached

    if( holder_data == " " ):
        pass

    else:
        split_line = holder_data.split()                                                    # Split incoming data

        if( len(split_line) == 0 ):
            error_message = "{} Stethoscope NOT in holder ".format(fS())
            print( error_message )
            statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
            status_filename = stampedDir + "log.txt"
            write_status_to_file( status_filename, error_message )
            print( "{} ERROR: Device missing ".format(fS()) )                                    # this string is specific to ssh communication
            sys.exit( fS() + " " + "ERR" )

        elif( split_line[1] == '1:' and split_line[2] == '0' ):
            error_message = "{} Stethoscope NOT in holder ".format(fS())
            print( error_message )
            statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
            status_filename = stampedDir + "log.txt"
            write_status_to_file( status_filename, error_message )
            print( "{} ERROR: Device missing ".format(fS()) )                                    # this string is specific to ssh communication
            sys.exit( fS() + " " + "ERR" )

        elif( split_line[1] == '1:' and split_line[2] == '1' ):
            print( "{} Stethoscope in holder ".format(fS()) )                    # device one in the holder
    return

def check_SH_holder( smartholder_SHH, consDir, executionTimeStamp, smarthandle_name ):
    for i in range(0, 2):
        holder_data = "{}".format( smartholder_SHH.readline() )                              # Read until timeout is reached
        if( holder_data == " " ):
            pass
        else:
            split_line = holder_data.split()                                                    # Split incoming data
            if( len(split_line) == 0 ):
                error_message = "{} {} NOT in holder ".format(fS(), smarthandle_name[i])
                print( error_message )
                statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
                status_filename = stampedDir + "log.txt"
                write_status_to_file( status_filename, error_message )
                print( "{} ERROR: Device missing ".format(fS()) )                                    # this string is specific to ssh communication
                sys.exit( fS() + " " + "ERR" )

            elif( split_line[1] == '1:' and split_line[2] == '0' ):
                error_message = "{} {} NOT in holder ".format(fS(), smarthandle_name[0])
                print( error_message )
                statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
                status_filename = stampedDir + "log.txt"
                write_status_to_file( status_filename, error_message )
                print( "{} ERROR: Device missing ".format(fS()) )                                    # this string is specific to ssh communication
                sys.exit( fS() + " " + "ERR" )

            elif( split_line[1] == '1:' and split_line[2] == '1' ):
                print( "{} {} in holder ".format(fS(), smarthandle_name[0] ) )                                                            # device one in the holder		

            elif( split_line[1] == '2:' and split_line[2] == '0' ):
                error_message = "{} {} NOT in holder ".format(fS(), smarthandle_name[1])
                print( error_message )
                statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
                status_filename = stampedDir + "log.txt"
                write_status_to_file( status_filename, error_message )
                print( "{} ERROR: Device missing ".format(fS()) )                                    # this string is specific to ssh communication
                sys.exit( fS() + " " + "ERR" )

            elif( split_line[1] == '2:' and split_line[2] == '1' ):
                print( "{} {} in holder ".format(fS(), smarthandle_name[1] ) )
    return

# ========================================================================================= #
# Variables
# ========================================================================================= #

# ----------------------------------------------
# Devices
# ----------------------------------------------
# Get device info
print( "\n============= DEVICE  IDENTIFICATION =============" )
panel_id_file_path = dataDir + "/panels.txt"
_, _, panel_id, _ = panelSelfID( panel_id_file_path, getMAC("eth0") )

devices_id_file_path = dataDir + "/panel" + str( panel_id ) + "devices.txt"
_, device_name_list, device_bt_address_list = panelDeviceID( devices_id_file_path, panel_id )

smarthandle_name            = ( device_name_list[1],
                                device_name_list[2] )
smarthandle_bt_address      = ( [device_bt_address_list[1]],
                                [device_bt_address_list[2]] )
print( "==================================================\n" )

# ========================================================================================= #
# Operation
# ========================================================================================= #

# ----------------------------------------------------------------------------------------- #
# Device Configuration, Connection and Activation
# ----------------------------------------------------------------------------------------- #

print( "============ ESTABLISHING  CONNECTION ============" )
# connecting to smartdevices (stethoscope/handles) ---------------------------------------- #
smartdevice = dict()
print( "{} Connecting to SmartDevices".format(fS()) )
for i in range( 0, 3 ):
    try:
        smartdevice[ device_name_list[i] ] = createBTPort( device_bt_address_list[i], 1 )       # Connect BT device
    except bluetooth.btcommon.BluetoothError as bluetoothError:
        print( "{} {} unavailable ".format(fS(), device_name_list[i]) )
        statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
        status_filename = stampedDir + "log.txt"
        write_status_to_file( status_filename, bluetoothError[0] )
        sys.exit( fS() + " " + "ERR" )
print( "==================================================\n" )

# connecting to smart holders ------------------------------------------------------------- #

print( "{} Connecting to smartholders ".format(fS()) )
baud, timeout = 115200, 1
notReady    = True
STH, SHH    = chr(0x41), chr(0x42)                                                          # Holder Identifier
smartholder = dict()

for i in range( 0, 2 ):
    try:
        USB  = createUSBPort( i, baud, timeout )                                            # Create USB connection
    except:
        try:
            USB  = createACMPort( i, baud, timeout )
        except:
            print( "{} Smart Holder unavailable ".format(fS()) )
            statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
            status_filename = stampedDir + "log.txt"
            write_status_to_file( status_filename, "Serial Error" )
            sys.exit( fS() + " " + "ERR" )
            
    finally:
        if( USB.is_open == False ): USB.open()

    while( notReady ):                                                                      # Loop until we receive SOH
        inData = USB.read( size=1 )                                                         # ...
        if( inData == STH or inData == SHH ):                                               # ...
            if  ( inData == STH ):
                inData  = "STH"
                portSTH = i
            elif( inData == SHH ):
                inData  = "SHH"
                portSHH = i
            print( "{} [INFO] Holder identified as {}".format(fS(), inData) )               # [INFO] Status update
            smartholder[ inData ] = USB
            break                                                                           # ...
        
    time.sleep(0.50)                                                                        # Sleep for stability!

print( "============== SYSTEMS STATUS CHECK ==============" )
# testing whats in then holders
check_ST_holder( smartholder["STH"], consDir, executionTimeStamp )
check_SH_holder( smartholder["SHH"], consDir, executionTimeStamp, smarthandle_name )
print( "==================================================\n" )

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #
print( "============== DEVICE  DEACTIVATION ==============" )
print( "{} Disconnecting bluetooth devices ".format(fS()) )
for _, device_BT_Obj in smartdevice.iteritems():
    device_BT_Obj.close()

print( "{} Disconnecting USB devices ".format(fS()) )
for ID in smartholder:    
    if( smartholder[ ID ].is_open ):
        smartholder[ ID ].close()
print( "==================================================\n" )

# ----------------------------------------------------------------------------------------- #
# END
# ----------------------------------------------------------------------------------------- #
print( "{} Status check completed successfully... Ready to Go! ".format(fS()) )
statusDir, stampedDir = create_status_directories( consDir, executionTimeStamp )
status_filename = stampedDir + "log.txt"
write_status_to_file( status_filename, " System CHECKS! " )
print( "{} AOK".format(fS()) )
