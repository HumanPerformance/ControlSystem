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
import  pexpect
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs

# PD3D modules
from    configurationProtocol                   import *
cons    = "consys"
shan    = "smarthandle"
shol    = "smartholder"
stet    = "stethoscope"
bpcu    = "bloodpressurecuff"

homeDir, pythonDir, consDir = definePaths(cons)
homeDir, pythonDir, shanDir = definePaths(shan)
homeDir, pythonDir, sholDir = definePaths(shol)
homeDir, pythonDir, stetDir = definePaths(stet)
homeDir, pythonDir, bpcuDir = definePaths(bpcu)

response = addPaths(pythonDir)
response = addPaths(consDir)
response = addPaths(shanDir)
response = addPaths(sholDir)
response = addPaths(stetDir)
response = addPaths(bpcuDir)

from    timeStamp                   import fullStamp
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *
from    stethoscopeProtocol         import *


# ========================================================================================= #
# Variables
# ========================================================================================= #

# ----------------------------------------------
# Devices
# ----------------------------------------------
stethoscope_name = "stethoscope"
stethoscopes_bt_address = (["00:06:66:8C:D3:F6"])


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


# pressure meter

#rfObject = createBTPort( "00:06:66:8C:D3:F6", 1 )

cmd = "sudo python " + bpcuDir + "pressureDialGauge2.py --mode SIM"
pressure_meter = pexpect.spawn( cmd, timeout=None )

# the following while loop should be the foundation for the simulation loop of this script
while( True ):
    for line in pressure_meter:
        out = line.strip('\n\r')
        print( out )

"""
connect to stethoscope here or let the blood pressure cuff handle it
"""

"""
port = 0
baud = 115200
timeout = 1
notReady = True
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

smartholder_data 						= [] 												# empty array for smart holder data


holder_flag         = 1                                          			    # single sensor flag

print( fullStamp() + " " + str( simDuration ) + " sec. simulation begins now " )                   # Statement confirming simulation start
while( simCurrentTime < simDuration ):

    holder_data = "{}".format( smartholder_usb_object.readline() )                          # Read until timeout is reached
    #print( holder_data )
    if( holder_data == '' ):
        pass
    else:
        split_line = holder_data.split()                                                    # Split incoming data
        formatted = ( "{} {} {}".format( fullStamp(), split_line[1], split_line[2] ) )      # Construct string
        print( formatted.strip('\n') )                                                     # [INFO] Status update

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

    simCurrentTime = time.time() - simStartTime												# update time


        
# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #




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


"""
