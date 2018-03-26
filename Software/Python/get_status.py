'''
*
* Inquire about status of all devices present on panel and log to file.
*
*
* VERSION: 0.1
*   - Initial "foundation" script
*
* KNOWN ISSUES:
*   - NON
*
* AUTHOR        : Mohammad Odeh
* WRITTEN       : Mar. 26th, 2018 Year de Nuestro SeNor
* 
'''

from    time                        import  sleep, time     # Sleep for stability, time for timing
from    usbProtocol                  import  createUSBPort  # Connect to USB based device
import  os, os.path, argparse, platform                     # Various features

# ************************************************************************
# ======================> CONSTRUCT ARGUMENT PARSER <=====================
# ************************************************************************
ap = argparse.ArgumentParser()

ap.add_argument("-t", "--time-span", type=int, default=30,
                help="time span of data collection in seconds (Default = 30)")

args = vars( ap.parse_args() )

# ************************************************************************
# =========================> DEFINITIONS & SETUP <========================
# ************************************************************************
ENQ		= chr(0x05)                                 # Enquiry.
ACK             = chr(0x06)                                 # Positive Acknowledgement.
NAK             = chr(0x15)                                 # Negative Acknowledgement.

if platform.system()=='Linux':

    # Define useful paths
    homeDir = "/home/pi"
    dst = homeDir + "/Desktop/data"
    fileName = dst + "/log.txt"

else:
    print( "OS not supported. Aborting" )
    quit()


# Check if directory+file exist
    if ( os.path.exists(dst)==False ):
        # Create said directory
        os.makedirs(dst)

        # Create file
        if( os.path.isfile(fileName)==False ):
            file(fileName, 'w').close()

# ************************************************************************
# =============================> SMARTHOLDER <============================
# ************************************************************************
name = "smartHoldaa"
port = 1
baud = 115200
atmt = 1e0

SH = createUSBPort( name, port, baud, atmt )                # Create connection
if( SH.is_open ):                                           # Check if port is open
    pass
else:
    SH.open()                                               # else open it if closed

SH.write( ENQ )                                             # Send ENQUIRY byte
sleep( 0.05 )                                               # Sleep for stability

with open( fileName, 'w' ) as f:                            # Write stuff to file
    start = time()                                          # Start timer
    while( time()-start < args["time-span"] ):
        f.write( SH.readline )                              # Read until newline character is hit

SH.close()                                                  # Close port and move on


# Enquire Stethoscope

# Enquire Thermometer
