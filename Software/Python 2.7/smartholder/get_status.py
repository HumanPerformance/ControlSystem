'''
*
* Inquire about status of all devices present on panel and log to file.
*
*
* VERSION: 0.2.1
*   - Wait until SmartHolder sends the SOH byte
*
* KNOWN ISSUES:
*   - Danny's existance
*
* AUTHOR        : Mohammad Odeh
* WRITTEN       : Mar. 26th, 2018 Year de Nuestro SeNor
* LAST MODIFIED : Mar. 30th, 2018 Year of Our Lord
*
'''

from    time                        import  sleep, time             # Sleep for stability, time for timing
from    getpass                     import  getuser                 # Get user name on WINDOWS
from    usbProtocol                 import  createUSBPort           # Connect to USB based device
from    usbProtocol                 import  createACMPort           # ... ACM variant
from    bluetoothProtocol_teensy32  import  createBTPort            # Connect to BT based devices
from    bluetoothProtocol_teensy32  import  closeBTPort             # Disconnect from BT based devices
from    timeStamp                   import  fullStamp   as  t       # Time stamps
##from    smarthandleProtocol         import  triggerDevice           # Not sure why
import  os, os.path, argparse, platform                             # Various features

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
SOH             = chr(0x01)                                         # Start of Header
ENQ		= chr(0x05)                                         # Enquiry
ACK             = chr(0x06)                                         # Positive Acknowledgement
NAK             = chr(0x15)                                         # Negative Acknowledgement

if platform.system()=='Linux':                                      # Define paths on a LINUX

    homeDir = "/home/pi"                                            # ...
    dst = homeDir + "/Desktop/data/"                                # ...
    fileName = dst + "log.txt"                                      # ...


elif platform.system()=='Windows':                                  # Define paths on a WINDOWS (you are a horible person)

    homeDir = "C:\\Users\\{}\\".format( getuser() )                 # ...
    dst     = homeDir + "Desktop\\data\\"                           # ...
    fileName= dst + "log.txt"                                       # ...

else:
    print( "OS not supported. Aborting" )
    quit()

if ( os.path.exists(dst)==False ):                                  # Check if directory exists
    os.makedirs(dst)                                                # Create folder
else: pass                                                          # ...

if( os.path.isfile(fileName)==False ):                              # Check if file exists
    file(fileName, 'w').close()                                     # Create mt file
else: pass                                                          # ...

# ************************************************************************
# =============================> SMARTHOLDER <============================
# ************************************************************************
__doc__ = '''
# ************************************************************************ #
#                                SMARTHOLDER                               #
# ************************************************************************ #
'''

port = 0
baud = 115200
timeout = 1
notReady = True

print( __doc__ )                                                    # [INFO] Status update

try:                                                                # Create USB connection
    SH = createUSBPort( port, baud, timeout )                       # ...
except:                                                             # Create ACM connection
    SH = createACMPort( port, baud, timeout )                       # ...
    
if( SH.is_open ):                                                   # Check if port is open
    pass                                                            # ...
else:
    SH.open()                                                       # else open it if closed

while( notReady ):                                                  # Loop until we receive SOH
    inData = SH.read( size=1 )                                      # ...
    if( inData == SOH ):                                            # ...
        print( "{} [INFO] SOH Received".format( t() ) )             # [INFO] Status update
        break                                                       # ...

sleep( 0.50 )                                                       # Sleep for stability
SH.write( ENQ )                                                     # Send ENQUIRY byte

with open( fileName, 'w' ) as f:                                    # Write stuff to file
    
    f.write( __doc__ )                                              # Write device header
    
    print( "{} Starting {} seconds of data collection"              # [INFO] Status update
           .format( t(), args["time"] ) )                           # [INFO] ...

    start = time()                                                  # Start timer
    while( time()-start < args["time"] ):
        inData = "{}".format( SH.readline() )                       # Read until timeout is reached

        if( inData == '' ):                                         # Skip empty lines
            pass                                                    # ...

        else:                                                       # Else, read incoming data
            formatted = ( "{} {}".format( t(), inData ) )           # Add time stamp

            print( formatted.strip('\n') )                          # [INFO] Status update
            f.write( formatted )                                    # Write to log file
            
SH.close()                                                          # Close port and move on

print( "{} DONE".format( t() ) )                                    # [INFO] Status update

# ************************************************************************
# =============================> STETHOSCOPE <============================
# ************************************************************************
__doc__ = '''
# ************************************************************************ #
#                                STETHOSCOPE                               #
# ************************************************************************ #
'''

with open( fileName, 'a' ) as f:                                    # Write stuff to file
    f.write( __doc__ )                                              # Write device header

# ************************************************************************
# =============================> THERMOMETER <============================
# ************************************************************************
__doc__ = '''
# ************************************************************************ #
#                                THERMOMETER                               #
# ************************************************************************ #
'''

BT_addr = "00:06:66:8C:D2:65"                                       # BT MAC address
port = 1                                                            # Port > 0

print( __doc__ )                                                    # [INFO] Status update

try:
    thermo = createBTPort( BT_addr, port )                          # Establish connection

    sleep( 0.50 )                                                   # Sleep for stability   
    thermo.send( ENQ )                                              # Send ENQUIRY byte
    inByte = thermo.recv( 1 )                                       # Expect 1 byte of data
        
    if( inByte == ACK ):                                            # If ACK
        formatted = ( "{} Thermometer: ACK\n".format( t() ) )       # ...
        
    elif( inByte == NAK ):                                          # If NAK
        formatted = ( "{} Thermometer: NAK\n".format( t() ) )       # ...

    else:                                                           # Else
        formatted = ( "{} Thermometer: ERR\n".format( t() ) )       # ...

    with open( fileName, 'a' ) as f:                                # Write stuff to file
        f.write( __doc__ )                                          # Write device header
        f.write( formatted )                                        # ...

except:
    print( "{} [INFO] Error Caught".format( t() ) )                 # [INFO] Status update              

finally:
    closeBTPort( thermo )                                           # Close port

print( "{} DONE".format( t() ) )                                    # [INFO] Status update
