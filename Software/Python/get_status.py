'''
*
* Inquire about status of all devices present on panel and log to file.
*
*
* VERSION: 0.2
*   - Check for directory hierarchy
*
* KNOWN ISSUES:
*   - Danny's existance
*
* AUTHOR        : Mohammad Odeh
* WRITTEN       : Mar. 26th, 2018 Year de Nuestro SeNor
* LAST MODIFIED : Mar. 27th, 2018 Year of Our Lord
'''

from    time                        import  sleep, time     # Sleep for stability, time for timing
from    getpass                     import  getuser         # Get user name on WINDOWS
from    usbProtocol                 import  createUSBPort   # Connect to USB based device
from    usbProtocol                 import  createACMPort   # ... ACM variant
from    bluetoothProtocol_teensy32  import  createBTPort    # Connect to BT based devices
from    timeStamp                   import  fullStamp       # Time stamps
##from    smarthandleProtocol         import  triggerDevice   # Not sure why
import  os, os.path, argparse, platform                     # Various features

# ************************************************************************
# ======================> CONSTRUCT ARGUMENT PARSER <=====================
# ************************************************************************
ap = argparse.ArgumentParser()

ap.add_argument("-t", "--time", type=int, default=15,
                help="time span of data collection in seconds (Default = 15)")

args = vars( ap.parse_args() )

# ************************************************************************
# =========================> DEFINITIONS & SETUP <========================
# ************************************************************************
ENQ		= chr(0x05)                                 # Enquiry.
ACK             = chr(0x06)                                 # Positive Acknowledgement.
NAK             = chr(0x15)                                 # Negative Acknowledgement.

if platform.system()=='Linux':                              # Define paths on a LINUX

    homeDir = "/home/pi"                                    # ...
    dst = homeDir + "/Desktop/data/"                        # ...
    fileName = dst + "log.txt"                              # ...


elif platform.system()=='Windows':                          # Define paths on a WINDOWS (you are a horible person)

    homeDir = "C:\\Users\\{}\\".format( getuser() )         # ...
    dst     = homeDir + "Desktop\\data\\"                   # ...
    fileName= dst + "log.txt"                               # ...

else:
    print( "OS not supported. Aborting" )
    quit()

if ( os.path.exists(dst)==False ):                          # Check if directory exists
    os.makedirs(dst)                                        # Create folder
else: pass                                                  # ...

if( os.path.isfile(fileName)==False ):                      # Check if file exists
    file(fileName, 'w').close()                             # Create mt file
else: pass                                                  # ...

# ************************************************************************
# =============================> SMARTHOLDER <============================
# ************************************************************************
port = 0
baud = 115200
timeout = 1

print( "Enquiring SmartHolder..." ) ,                       # [INFO] Status update

##SH = createUSBPort( port, baud, timeout )                   # Create connection
SH = createACMPort( port, baud, timeout )                   # Create connection
if( SH.is_open ):                                           # Check if port is open
    pass
else:
    SH.open()                                               # else open it if closed

sleep( 0.50 )                                               # Sleep for stability
SH.write( ENQ )                                             # Send ENQUIRY byte

with open( fileName, 'w' ) as f:                            # Write stuff to file
    
    print( "Starting {} seconds of data collection"         # [INFO] Status update
           .format( args["time"] ) )                        # [INFO] ...

    start = time()                                          # Start timer
    while( time()-start < args["time"] ):
        inData = "{}".format(SH.readline())                 # Read until timeout is reached

        if( inData == '' ):                                 # Skip empty lines
            pass                                            # ...

        elif( inData.split()[0] == 'Sensor' ):              # Check if this is the data we want
            formatted = ( "{} {}"                           # Add time stamp
                          .format( fullStamp(), inData ) )  # ...

            print( formatted.strip('\n') )                  # [INFO] Status update
            f.write( formatted )                            # Write to log file

        else:                                               # Else, don't read
            pass                                            # ...
            
SH.close()                                                  # Close port and move on

print( "DONE" )                                             # [INFO] Status update

# ************************************************************************
# =============================> STETHOSCOPE <============================
# ************************************************************************


# ************************************************************************
# =============================> THERMOMETER <============================
# ************************************************************************
##BT_addr = "00:06:66:8C:D2:65"                               # BT MAC address
##port = 1                                                    # Port > 0
##
##print( "Enquiring Thermometer..." ) ,                       # [INFO] Status update
##
##try:
##    thermo = createBTPort( BT_addr, port )                  # Establish connection
##
##    sleep( 0.50 )                                           # Sleep for stability   
##    thermo.send( ENQ )                                      # Send ENQUIRY byte
##    inByte = thermo.recv( 1 )                               # Expect 1 byte of data
##
##    with open( fileName, 'a' ) as f:                        # Write stuff to file
##        f.write( "Thermometer...{}\n".format( inByte ) )    # ...
##
##except:
##    print( "[INFO] Error Caught [INFO]..." ) ,              # [INFO] Status update
##
##finally:
##    closeBTPort( thermo )                                   # Close port
##
##print( "DONE" )                                             # [INFO] Status update
