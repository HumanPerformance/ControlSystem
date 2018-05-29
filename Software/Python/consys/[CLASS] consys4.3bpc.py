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
import  argparse
import  pexpect
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs
from    threading                   import Thread
from    Queue                       import Queue

# PD3D modules
from    configurationProtocol                   import *

paths, pythonDir, consDir, stetDir, shanDir, sholDir, bpcuDir, outputDir, dataDir = definePaths()
response = addPaths(paths)

from    timeStamp                   import fullStamp    as  fS
from    bluetoothProtocol_teensy32  import *
from    usbProtocol                 import *
from    smarthandleProtocol         import *
from    stethoscopeProtocol         import *

# ========================================================================================= #
# Variables
# ========================================================================================= #

executionTimeStamp  = fS()

# ----------------------------------------------------------------------------------------- #
# Constructing argument parser
# ----------------------------------------------------------------------------------------- #

ap = argparse.ArgumentParser()

ap.add_argument( "-s", "--scenario", type=int, default=0,                   # Scenario
                help="Select scenario.\nDefault=0" )
ap.add_argument( "-st", "--simulation_time", type=int, default=45,          # Length of simulation
                help="Simulation time" )
ap.add_argument( "-m", "--mode", type=str, default="SIM",                   # Mode of operation (SIM vs NORM)
                help="Operation Mode (NORMal and SIMulation)" )
ap.add_argument( "-lp", "--lower_pressure", type=int, default=85,           # Low  pressure limit (for SIM only)
                help="Lower Pressure Limit (only for SIM)" )
ap.add_argument( "-hp", "--higher_pressure", type=int, default=145,         # High pressure limit (for SIM only)
                help="Higher Pressure Limit (only for SIM)" )
args = vars( ap.parse_args() )

print( "{} Scenario                 = {}".format(fS(), args["scenario"] )       )
print( "{} Simulation Time          = {}".format(fS(), args["simulation_time"]) )
print( "{} Operation Mode           = {}".format(fS(), args["mode"])            )
print( "{} Lower  pressure set to   = {}".format(fS(), args["lower_pressure"])  )
print( "{} Higher pressure set to   = {}".format(fS(), args["higher_pressure"]) )

# ========================================================================================= #
# Define Class
# ========================================================================================= #

class data_acquisition( object ):

    # Here you define whatever parameters you want to pass into your class
    def __init__( self, stet_name, stethoscope_BT, smartholder_USB, paramN=None ):
        self.stet_name          = stet_name                                                 # Store stethoscope ID
        self.stethoscope        = stethoscope_BT                                            # Store stethoscope BT  object
        self.smartholder        = smartholder_USB                                           # Store smartholder USB object
        
        self.something_else     = paramN                                                    # Store whatever it is you want

        # Run the setup function
        self.setup()                                                                        # Declare various variables

        # Start the ABPC thread
        self.t_ABPC = Thread( target=ABPC, args=(self,) )                                   # Start ABPC pexpect thread
        self.t_ABPC.start()                                                                 # ...

        # Start data gathering
        self.run()                                                                          # Run timed loop
        
# ----------------------------------------------------------------------------------------- #

    # Here is where you start defining your functions
    def setup( self ):
        '''
        Setup program by gathering all the required
        arguments/timers/addresses/etc... and declaring
        needed lists/variables
        '''
        
        # Gather argument parser info
        """
        self.scenario           = 0         # Normal                --no simulation
        self.scenario           = 1         # stethoscope aug.      --aug. of the stethoscope
        self.scenario           = 2         # blood pressure aug.   --aug. of blood pressure
        self.scenario           = 3         # All                   --aug. of all devices
        """
        self.scenario           = args["scenario"]                                          # Store scenario
        self.simDuration        = args["simulation_time"]                                   # Durtation of simluation in seconds

        # Now define the global variables that ALL your functions need to access
        self.holder_flag_new    = 0                                                         # Whether device is in/out of holder
        self.holder_flag_old    = 0                                                         # Previous state of ^
        self.bpc_flag_new       = 0                                                         # same
        self.bpc_flag_old       = 0                                                         # saim
        self.smartholder_data   = []                                                        # ...

# ----------------------------------------------------------------------------------------- #

    def ABPC( self ):
        # start blood pressure cuff and digital dial -------------------------------------- #
        print( "{} Connecting to blood pressure cuff ".format(fS()) )
        mode            = args["mode"]
        lower_pressure  = args["lower_pressure"]                                                                      # units in mmHg
        higher_pressure = args["higher_pressure"]                                                                   # ...
        
        prog = "python {}pressureDialGauge_v2.0.py".format(bpcuDir)
        args = (
                " --destination {} -m {} "
                "-lp {} -hp {} -b {}" ).format( executionTimeStamp, mode,
                                                lower_pressure, higher_pressure, 0.75 )
        cmd  = prog + args
        self.pressure_meter = pexpect.spawn( cmd, timeout=None )
    
        for line in self.pressure_meter:
            self.out = line.strip('\n\r')

# ----------------------------------------------------------------------------------------- #

    def run( self ):
        print( "{} {} sec. simulation begins now ".format(fS(), self.simDuration) )         # Statement confirming simulation start

        self.simCurrentTime, simStartTime = 0, time.time()
        while( self.simCurrentTime < self.simDuration ):
            self.check_holder()
            self.check_pressure()
            self.interactions()

            self.simCurrentTime = time.time() - simStartTime

        print( "{} Closing blood pressure cuff connection ".format(fS()) )
        self.pressure_meter.close()                                                         # Close the pexpect pipe
        if( t_pressure_meter.isAlive() ):
            print( "{} Shutting down ABPC thread".format(fS()) )
            self.t_ABPC.join(2.0)

        return( self.smartholder_data )
    
# ----------------------------------------------------------------------------------------- #

    def check_cholder( self ):
        # NOTE:-
        #
        # Anything that doesn't start with "self" gets destroyed and garbage
        # collected after function ends execution. Do this to things you
        # don't care about as a sort of optimization.
        # Things you want to update across the entire class should start with
        # "self".
        inData = "{}".format( self.smartholder.readline() )

        if( inData == '' ):                                             # If empty line
            pass                                                        # do nothing

        else:
            split_line = inData.split()                                 # Split incoming data

            if( split_line[1] == '1:' and split_line[2] == '0' ):
                print( "{} {} has been removed ".format(fS(),
                                                        self.stet_name) )
                self.holder_flag_new = 0                                # Set the holder flag to 0

            elif( split_line[1] == '1:' and split_line[2] == '1' ):
                print( "{} {} has been stored ".format(fS(),
                                                       self.stet_name) )
                self.holder_flag_new = 1                                # Set the holder flag to 1

            self.smartholder_data.append( ["%.02f" %self.simCurrentTime,
                                          str( self.holder_flag_new ),
                                          '\n'] )

# ----------------------------------------------------------------------------------------- #

    def check_pressure( self ):
        if( self.scenario == 3 ):
            split_line = self.out.split(",")
            
            if( split_line[0] == "SIM" ):
                self.bpc_flag_new = int(split_line[1])
                
                if( self.bpc_flag_new == 1 ):
                    print( "{} Within simulated pressure range ".format(fS()) )

                elif( self.bpc_flag_new == 0 ):
                    print( "{} Outside simulated pressure range ".format(fS()) )

            elif( split_line[0] == "MUTE" ):
                print split_line
                mute_flag = int(split_line[1])

                if( mute_flag == 0 ):
                    statusEnquiry( self.stethoscope ) # replace with new function

                elif( mute_flag == 1 ):
                    statusEnquiry( self.stethoscope ) 

# ----------------------------------------------------------------------------------------- #

    def interactions( self ):
        # scenario 0 = recording.
        if( self.scenario == 0 ):
            pass

        # scenario 1 = S4 Gallop
        elif( self.scenario == 1 ):
            if( self.holder_flag_new != self.holder_flag_old ):
                
                if( self.holder_flag_new == 0 ):
                    fileByte = definitions.S4GALL
                    startBlending( self.stethoscope, fileByte)
                    self.holder_flag_old = self.holder_flag_new
                    
                elif( self.holder_flag_new == 1 ):
                    stopBlending( self.stethoscope )
                    self.holder_flag_old = self.holder_flag_new

        # scenario 2 = Aortic Stenosis
        elif( self.scenario == 2 ):
            if( self.holder_flag_new != self.holder_flag_old ):

                if( self.holder_flag_new == 0 ):
                    fileByte = definitions.AORSTE
                    startBlending( self.stethoscope, fileByte )
                    self.holder_flag_old = self.holder_flag_new
                    
                elif( self.holder_flag_new == 1 ):
                    stopBlending( self.stethoscope )
                    self.holder_flag_old = self.holder_flag_new

        # scenario 3 = KOROT
        elif( self.scenario == 3 ):
            if( self.holder_flag_new == 0 ):
                if( self.bpc_flag_new == 1 and self.bpc_flag_new != self.bpc_flag_old ):
                    fileByte = definitions.KOROT
                    startBlending( self.stethoscope, fileByte)
                    self.bpc_flag_old = self.bpc_flag_new
                    
                elif( self.bpc_flag_new == 0 and self.bpc_flag_new != self.bpc_flag_old ):
                    stopBlending( self.stethoscope )
                    self.bpc_flag_old = self.bpc_flag_new
                
# ========================================================================================= #
# Setup program
# ========================================================================================= #

# Get device info
panel_id_file_path = dataDir + "/panels.txt"
_, _, panel_id, _ = panelSelfID( panel_id_file_path, getMAC("eth0") )

devices_id_file_path = dataDir + "/panel" + str( panel_id ) + "devices.txt"
_, device_name_list, device_bt_address_list = panelDeviceID( devices_id_file_path, panel_id )

stethoscope_name = device_name_list[0]
stethoscope_bt_address = ([device_bt_address_list[0]])

# Create BT and USB connections
print( "{} OPERATION ".format(fS()) )
print( "{} Begin device configuration ".format(fS()) )

# connecting to panel devices
print( "{} Connecting to panel devices ".format(fS()) )

# connecting to stethoscope --------------------------------------------------------------- #
print( "{} Connecting to stethoscope ".format(fS()) )
stethoscope_bt_object = createBTPort( stethoscope_bt_address[0], 1 )                        # using bluetooth protocol commands

# configuring stethoscope ----------------------------------------------------------------- #
if( args["scenario"] == 0 ):
    print( "{} Generating filename for audio data ".format(fS()) )
    randString = genRandString( 4 )
    print( "{} Generated : {}".format(fS(), randString) )
    print( "{} Setting Stethoscope Recording Mode ".format(fS()) )
    recMode = 0
    print( "{} Setting recording mode and filename".format(fS()) )
    setRecordingMode( stethoscope_bt_object, recMode )
    parseString( stethoscope_bt_object, randString )
    startRecording( stethoscope_bt_object )

# connecting to smart holders ------------------------------------------------------------- #
print( "{} Connecting to smart holders ".format(fS()) )
port = 0
baud = 115200
timeout = 1
notReady = True

try:
    smartholder_usb_object  = createUSBPort( port, baud, timeout )                          # test USB vs ACM port issue
except:
    smartholder_usb_object  = createACMPort( port, baud, timeout )
finally:
    if( smartholder_usb_object.is_open == False ):
        smartholder_usb_object.open()

SOH = chr(0x01)                                         # Start of Header
while( notReady ):                                                                          # Loop until we receive SOH
    inData = smartholder_usb_object.read( size=1 )                                          # ...
    if( inData == SOH ):                                                                    # ...
        print( "{} [INFO] SOH Received".format(fS()) )                             # [INFO] Status update
        break                                                                               # ...

time.sleep(0.50)                                                                            # Sleep for stability!


# ========================================================================================= #
# Data Gathering
# ========================================================================================= #

smartholder_data = data_acquisition( stethoscope_name,
                                     stethoscope_bt_object,
                                     smartholder_usb_object )

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #

print( fullStamp() + " Disconnecting bluetooth devices " )
if( scenario == 0 ):
    stopRecording( stethoscope_bt_object )
elif( scenario == 1 ):
    stopBlending( stethoscope_bt_object )
elif( scenario == 2 ):
    stopBlending( stethoscope_bt_object )

print( fullStamp() + " Checking and sending stethoscope to IDLE state" )
setToIdle( stethoscope_bt_object )

print( fullStamp() + " Closing Stethoscope bluetooth port" )
stethoscope_bt_object.close()

print( fullStamp() + " Disconnecting usb devices " )
if( smartholder_usb_object.is_open ):
    smartholder_usb_object.close()

# ========================================================================================= #
# Output
# ========================================================================================= #
print( fullStamp() + " Writting data to file " )

if( path.exists( outputDir ) == False ):
    print( fullStamp() + " Output directory not present " )
    print( fullStamp() + " Generating output directory " )
    makedirs( outputDir )
else:
    print( fullStamp() + " Found output directory " )

stampedDir = outputDir + executionTimeStamp + "/"
if( path.exists( stampedDir ) == False ):
    print( fullStamp() + " Time-stamped directory not present " )
    print( fullStamp() + " Generating time-stamped directory " )
    makedirs( stampedDir )
else:
    print( fullStamp() + " Found time-stamped directory " )

smartholder_output_filename = stampedDir + "holder.txt"

N_lines = len( smartholder_data )

for i in range(0, N_lines):
        if( i == 0 ):
                with open(smartholder_output_filename, 'a') as dataFile:
                        dataFile.write( fullStamp() + " Smart Holder for = " + stethoscope_name + '\n' )
                        dataFile.write( fullStamp() + " COM Port = " + str( port ) + '\n')
        with open(smartholder_output_filename, 'a') as dataFile:
                dataFile.write( smartholder_data[i][0] + "," + smartholder_data[i][1] + '\n' )

# zipping output
#print( fullStamp() + " Compressing data " )
#os.system("cd " + consDir + "; sudo zip -r " + consDir + "output.zip output")

# ----------------------------------------------------------------------------------------- #
# END
# ----------------------------------------------------------------------------------------- #
print( fullStamp() + " Program completed " )
print( fullStamp() + " " + "AOK" )
