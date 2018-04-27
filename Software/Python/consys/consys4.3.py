"""
consys4.py

Latest version of the control system execution software
            
Fluvio L. Lobo Fenoglietto 04/18/2018
"""

# ========================================================================================= #
# Import Libraries and/or Modules
# ========================================================================================= #
# Python modules
import  sys
import  os
import  serial
import  time
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs

# PD3D modules
from    configurationProtocol       import *
cons    = "consys"
shan    = "smarthandle"
shol    = "smartholder"
stet    = "stethoscope"
homeDir, pythonDir, consDir = definePaths(cons)
homeDir, pythonDir, shanDir = definePaths(shan)
homeDir, pythonDir, sholDir = definePaths(shol)
homeDir, pythonDir, stetDir = definePaths(stet)

response = addPaths(pythonDir)
response = addPaths(consDir)
response = addPaths(shanDir)
response = addPaths(sholDir)
response = addPaths(stetDir)

from    timeStamp                   import fullStamp
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *


# ========================================================================================= #
# Variables
# ========================================================================================= #

# ----------------------------------------------
# Devices
# ----------------------------------------------
smarthandle_name            = (["Otoscope",
                                "Ophthalmoscope"])

otoscope_bt_address         = "00:06:66:83:89:6D"
ophthalmoscope_bt_address   = "00:06:66:80:8C:08"

smarthandle_bt_address      = ([otoscope_bt_address,
                                ophthalmoscope_bt_address])


SOH             			= chr(0x01)                                         			# Start of Header
ENQ							= chr(0x05)                                         			# Enquiry
ACK             			= chr(0x06)                                         			# Positive Acknowledgement
NAK             			= chr(0x15)                                         			# Negative Acknowledgement


# ----------------------------------------------
# Timers
# ----------------------------------------------
executionTimeStamp  = fullStamp()

# ========================================================================================= #
# Operation
# ========================================================================================= #

# ----------------------------------------------------------------------------------------- #
# Device Configuration, Connection and Activation
# ----------------------------------------------------------------------------------------- #
print fullStamp() + " OPERATION "
print fullStamp() + " Begin device configuration "

port = 0
baud = 115200
timeout = 1
notReady = True

print( fullStamp() + " Connecting to panel devices " )
print( fullStamp() + " Connecting to smart handles " )
N_smarthandles = 2
smarthandle_bt_object = []
for i in range(0, N_smarthandles):
    smarthandle_bt_object.append( createBTPort( smarthandle_bt_address[i], 1 ) )            # Connecting to bluetooth handle
    startDataStream( smarthandle_bt_object[i], 20, '\n' )                                   # Starting data streaming

print( fullStamp() + " Connecting to smart holders " )

try:
    smartholder_usb_object  = createUSBPort( port, baud, timeout )                          # test USB vs ACM port issue
except:
    smartholder_usb_object  = createACMPort( port, baud, timeout )

if smartholder_usb_object.is_open:
    pass
else:
    smartholder_usb_object.open()

while( notReady ):                                                                          # Loop until we receive SOH
    inData = smartholder_usb_object.read( size=1 )                                          # ...
    if( inData == SOH ):                                                                    # ...
        #print( "{} [INFO] SOH Received".format( fullStamp() ) )                             # [INFO] Status update
        break                                                                               # ...

time.sleep(0.50)                                                                            # Sleep for stability!

# ----------------------------------------------------------------------------------------- #
# Data Gathering
# ----------------------------------------------------------------------------------------- #

# Variables
simStartTime        = time.time()
simCurrentTime      = 0                                                                     # seconds
simDuration         = 20                                                                    # seconds
simStopTime         = simDuration                                                           # seconds

smarthandle_data 						= {} 												# dictionary structure to contain incoming smarthandle data
smarthandle_data[smarthandle_name[0]] 	= []
smarthandle_data[smarthandle_name[1]] 	= []

smartholder_data 						= [] 												# empty array for smart holder data

"""
dataStream          = []
dataStreamOne       = []
dataStreamTwo       = []
"""

holder_flag         = ([1,1]) 																# flag for presence or absence of device

print( fullStamp() + " " + str( simDuration ) + " sec. simulation begins now " )                   # Statement confirming simulation start
while( simCurrentTime < simDuration ):

    holder_data = "{}".format( smartholder_usb_object.readline() )                          # Read until timeout is reached
    #print( holder_data )
    if( holder_data == '' ):
        pass
    else:
        split_line = holder_data.split()                                                    # Split incoming data
        formatted = ( "{} {} {}".format( fullStamp(), split_line[1], split_line[2] ) )      # Construct string
        #print( formatted.strip('\n') )                                                     # [INFO] Status update

        if( split_line[1] == '1:' and split_line[2] == '0' ):
            print( fullStamp() + " " + smarthandle_name[0] + " has been removed " )
            holder_flag[0] = 0

        elif( split_line[1] == '1:' and split_line[2] == '1' ):
            print( fullStamp() + " " + smarthandle_name[0] + " has been stored " )
            holder_flag[0] = 1                                                              # device one in the holder		

        elif( split_line[1] == '2:' and split_line[2] == '0' ):
            print( fullStamp() + " " + smarthandle_name[1] + " has been removed " )
            holder_flag[1] = 0

        elif( split_line[1] == '2:' and split_line[2] == '1' ):
            print( fullStamp() + " " + smarthandle_name[1] + " has been stored " )
            holder_flag[1] = 1

        smartholder_data.append( ["%.02f" %simCurrentTime,
                                  str( holder_flag[0] ),
                                  str( holder_flag[1] ),
                                  '\n'])

    for i in range(0, N_smarthandles):
        #print( holder_flag )
        if( holder_flag[i] == 0 ):
            # print( fullStamp() + " Streaming data from " + smarthandle_name[i] )
            smarthandle_data[smarthandle_name[i]].append( ["%.02f" %simCurrentTime,
                                                           readDataStream( smarthandle_bt_object[i],
                                                           '\n' )] )
    simCurrentTime = time.time() - simStartTime												# update time

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #

for i in range(0, N_smarthandles):
    time.sleep(0.50)
    stopDataStream( smarthandle_bt_object[i], 20, '\n' )                                    # Stop streaming data
    smarthandle_bt_object[i].close()                                                        # Closing bluetooth port
    
#print dataStream


# ========================================================================================= #
# Output
# ========================================================================================= #

outDir = consDir + "output/"
if( path.exists( outDir ) == False ):
    print( fullStamp() + " Output directory not present " )
    print( fullStamp() + " Generating output directory " )
    makedirs( outDir )
else:
    print( fullStamp() + " Found output directory " )

stampedDir = outDir + fullStamp() + "/"
if( path.exists( stampedDir ) == False ):
    print( fullStamp() + " Time-stamped directory not present " )
    print( fullStamp() + " Generating time-stamped directory " )
    makedirs( stampedDir )
else:
    print( fullStamp() + " Found time-stamped directory " )


smarthandle_output_filename = ([ stampedDir + "oto.txt",
								 stampedDir + "ophtho.txt" ])
smartholder_output_filename = stampedDir + "holder.txt"

N_lines = ([ len( smarthandle_data[smarthandle_name[0]] ),
			 len( smarthandle_data[smarthandle_name[1]] ),
			 len( smartholder_data ) ])

for i in range(0, len( N_lines )):
	if( i < N_smarthandles ):
		for j in range(0, N_lines[i]):
			if( j == 0 ):
				with open(smarthandle_output_filename[i], 'a') as dataFile:
					dataFile.write( fullStamp() + " Smart Handle = " + smarthandle_name[i] + '\n' )
					dataFile.write( fullStamp() + " Bluetooth Address = " + smarthandle_bt_address[i] + '\n')
			with open(smarthandle_output_filename[i], 'a') as dataFile:
				dataFile.write( smarthandle_data[smarthandle_name[i]][j][0] + "," + smarthandle_data[smarthandle_name[i]][j][1] + '\n' )
	else:
		for j in range(0, N_lines[i]):
			if( j == 0 ):
				with open(smartholder_output_filename, 'a') as dataFile:
					dataFile.write( fullStamp() + " Smart Holder " + '\n' )
					dataFile.write( fullStamp() + " COM Port = " + str( port ) + '\n')
			with open(smartholder_output_filename, 'a') as dataFile:
				dataFile.write( smartholder_data[j][0] + "," + smartholder_data[j][1] + "," + smartholder_data[j][2] + '\n' )


# zipping output
os.system("cd " + consDir + "; sudo zip -r " + consDir + "output.zip output")
