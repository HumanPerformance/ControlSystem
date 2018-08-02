'''
* consys5.py
*
* Latest version of the control system execution software
*
* VERSION: 5.2
*   - ADDED   : Implemented ABPC update to script and it
*               now handles multiple simulation regions.
*   - ADDED   : Awesomeness!!
*   - MODIFIED: Rewrote certain parts of the code into a class
*   - FIXED   : Fluvio's horrible, horrible coding skills.
*               Oh God, what did we do to deserve this?
*   - ADDED   : Merge consys4.3 and consys4.3bpc
*
* KNOWN ISSUES:
*   - Nothing visible atm
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* WRITTEN                   :   04/18/2018
*
* MODIFIED BY               :   The Great Mohammad Odeh
* DATE                      :   Aug.  2nd, 2018 Year of Our Lord
*
'''

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

# PD3D modules
from    configurationProtocol       import *

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
ap.add_argument( "-st", "--simulation_time", type=int, default=60,          # Length of simulation
                help="Simulation time" )
ap.add_argument( "-m", "--mode", type=str, default="SIM",                   # Mode of operation (SIM vs NORM)
                help="Operation Mode (NORMal and SIMulation)" )
ap.add_argument( "-lp", "--lower_pressure", type=int, default=85,           # Low  pressure limit (for SIM only)
                help="Lower Pressure Limit (only for SIM)" )
ap.add_argument( "-hp", "--higher_pressure", type=int, default=145,         # High pressure limit (for SIM only)
                help="Higher Pressure Limit (only for SIM)" )
args = vars( ap.parse_args() )

print( "\n================== GENERAL INFO ==================" )
print( "{} Scenario                 = {:3}".format(fS(), args["scenario"] )       )
print( "{} Simulation Time          = {:3}".format(fS(), args["simulation_time"]) )
print( "{} Operation Mode           = {:3}".format(fS(), args["mode"])            )
print( "{} Lower  pressure set to   = {:3}".format(fS(), args["lower_pressure"])  )
print( "{} Higher pressure set to   = {:3}".format(fS(), args["higher_pressure"]) )
print( "==================================================\n" )

# ========================================================================================= #
# Define Class
# ========================================================================================= #

class data_acquisition( object ):
    
    # Here you define whatever parameters you want to pass into your class
    def __init__( self, args, devices_name, devices_BT, smartholder_USB, timeStamp, paramN=None ):
        
        # Stethoscope/holder stuff
        self.stet_name          = devices_name[0]                                           # Store stethoscope ID
        self.stethoscope        = devices_BT["stethoscope"]                                 # Store stethoscope BT  object

        self.smartHandle_name   = ( devices_name[1], devices_name[2] )
        self.smartHandle        = { devices_name[1]: devices_BT[devices_name[1]],
                                    devices_name[2]: devices_BT[devices_name[2]] }

        self.smartholder_STH    = smartholder_USB["STH"]                                    # Store smartholder USB object
        self.smartholder_SHH    = smartholder_USB["SHH"]                                    # ...
        
        # Unify execution timestamp to make sure both .txt outputs are stored in one place
        self.executionTimeStamp = timeStamp                                                 # This will be used as directory name

        # Anything else
        self.something_else     = paramN                                                    # Store whatever it is you want

        # Run the setup function
        self.setup( args )                                                                  # Declare various variables

        # Start the ABPC thread
        self.t_ABPC = Thread( target=self.ABPC, args=() )                                   # Start ABPC pexpect thread
        self.t_ABPC.deamon = True                                                           # Allow program to shutdown even if thread is running
        self.t_ABPC.start()                                                                 # ...

        # Start data gathering
        time.sleep( 0.25 )                                                                  # Prevent thread and data collection from interfering
        self.run()                                                                          # Run timed loop
        
# ----------------------------------------------------------------------------------------- #

    # Here is where you start defining your functions
    def setup( self, args ):
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
        self.mode               = args["mode"]                                              # ...
        self.pressureLO         = args["lower_pressure"]                                    # Units in mmHg
        self.pressureHI         = args["higher_pressure"]                                   # Same ^

        # Now define the global variables that ALL your functions need to access
        self.ST_holder_flag_new = 0                                                         # Whether device is in/out of holder
        self.ST_holder_flag_old = 0                                                         # Previous state of ^
        self.bpc_flag_new       = 0                                                         # same
        self.bpc_flag_old       = 0                                                         # saim
        self.ST_holder_data     = []                                                        # ...

        self.SH_holder_flag_new = [1,1]                                                     # SmartHandle holder flags
        self.SH_holder_flag_new = { self.smartHandle_name[0]: 1,
                                    self.smartHandle_name[1]: 1 }
        self.SH_holder_flag_old = []                                                        # Not sure we will need this
        self.SH_holder_data     = []                                                        # SmartHandle holder data
        self.smartHandle_data 	= dict()
        
# ----------------------------------------------------------------------------------------- #

    def ABPC( self ):
        # start blood pressure cuff and digital dial -------------------------------------- #
        print( "{} Connecting to blood pressure cuff ".format(fS()) )                                                                   # ...

        prog = "python {}pressureDialGauge_v2.0.py".format(bpcuDir)
        args = (
                " --destination {} -m {} "
                "-lp {} -hp {} -b {}" ).format( self.executionTimeStamp, self.mode,
                                                self.pressureLO, self.pressureHI, 0.75 )
        cmd  = prog + args
        self.pressure_meter = pexpect.spawn( cmd, timeout=None )
    
        for line in self.pressure_meter:
            self.out = line.strip('\n\r')

# ----------------------------------------------------------------------------------------- #

    def run( self ):
        print( "{} {} sec. simulation begins now ".format(fS(), self.simDuration) )         # Statement confirming simulation start

        self.smartHandle_data[ self.smartHandle_name[0] ] 	= []
        self.smartHandle_data[ self.smartHandle_name[1] ] 	= []

        self.simCurrentTime, simStartTime = 0, time.time()
        while( self.simCurrentTime < self.simDuration ):
            self.check_ST_holder()
            self.check_SH_holder()
            self.check_pressure()
            self.interactions()

            self.simCurrentTime = time.time() - simStartTime

        print( "{} Closing blood pressure cuff connection ".format(fS()) )
        self.pressure_meter.close()                                                         # Close the pexpect pipe
        if( self.t_ABPC.isAlive() ):
            print( "{} Shutting down ABPC thread".format(fS()) )
            self.t_ABPC.join(2.0)
    
# ----------------------------------------------------------------------------------------- #

    def check_ST_holder( self ):
        # NOTE:-
        #
        # Anything that doesn't start with "self" gets destroyed and garbage
        # collected after function ends execution. Do this to things you
        # don't care about as a sort of optimization.
        # Things you want to update across the entire class should start with
        # "self".
        inData = "{}".format( self.smartholder_STH.readline() )

        if( inData == '' ):                                                                 # If empty line
            pass                                                                            # do nothing

        else:
            split_line = inData.split()                                                     # Split incoming data

            if( split_line[1] == '1:' and split_line[2] == '0' ):
                print( "{} {} has been removed ".format(fS(),
                                                        self.stet_name) )
                self.ST_holder_flag_new = 0                                                 # Set the holder flag to 0

            elif( split_line[1] == '1:' and split_line[2] == '1' ):
                print( "{} {} has been stored ".format(fS(),
                                                       self.stet_name) )
                self.ST_holder_flag_new = 1                                                 # Set the holder flag to 1

            self.ST_holder_data.append( ["%.02f" %self.simCurrentTime,
                                         str( self.ST_holder_flag_new ),
                                         '\n'] )
# ----------------------------------------------------------------------------------------- #

    def check_SH_holder( self ):
        
        inData = "{}".format( self.smartholder_SHH.readline() )

        if( inData == '' ):                                                                 # If empty line
            pass                                                                            # do nothing

        else:
            ID0 = self.smartHandle_name[0]
            ID1 = self.smartHandle_name[1]
            split_line = inData.split()                                                     # Split incoming data

            if( split_line[1] == '1:' and split_line[2] == '0' ):
                print( "{} {} has been removed".format(fS(),
                                                       ID0) )
                self.SH_holder_flag_new[ ID0 ] = 0

            elif( split_line[1] == '1:' and split_line[2] == '1' ):
                print( "{} {} has been stored ".format(fS(),
                                                       ID0) )
                self.SH_holder_flag_new[ ID0 ] = 1                                          # device one in the holder		

            elif( split_line[1] == '2:' and split_line[2] == '0' ):
                print( "{} {} has been removed".format(fS(),
                                                       ID1 ) )
                self.SH_holder_flag_new[ ID1 ] = 0

            elif( split_line[1] == '2:' and split_line[2] == '1' ):
                print( "{} {} has been stored ".format(fS(),
                                                       ID1) )
                self.SH_holder_flag_new[ ID1 ] = 1

            self.SH_holder_data.append( ["%.02f" %self.simCurrentTime,
                                         str( self.SH_holder_flag_new[ ID0 ] ),
                                         str( self.SH_holder_flag_new[ ID1 ] ),
                                         '\n'])
            
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
            if( self.ST_holder_flag_new != self.ST_holder_flag_old ):
                
                if( self.ST_holder_flag_new == 0 ):
                    fileByte = definitions.S4GALL
                    startBlending( self.stethoscope, fileByte)
                    self.ST_holder_flag_old = self.ST_holder_flag_new
                    
                elif( self.ST_holder_flag_new == 1 ):
                    stopBlending( self.stethoscope )
                    self.ST_holder_flag_old = self.ST_holder_flag_new

        # scenario 2 = Aortic Stenosis
        elif( self.scenario == 2 ):
            if( self.ST_holder_flag_new != self.ST_holder_flag_old ):

                if( self.ST_holder_flag_new == 0 ):
                    fileByte = definitions.AORSTE
                    startBlending( self.stethoscope, fileByte )
                    self.ST_holder_flag_old = self.ST_holder_flag_new
                    
                elif( self.ST_holder_flag_new == 1 ):
                    stopBlending( self.stethoscope )
                    self.ST_holder_flag_old = self.ST_holder_flag_new

        # scenario 3 = KOROT
        elif( self.scenario == 3 ):
            if( self.ST_holder_flag_new == 0 ):                                             # If stethoscope is not in holder
                if( self.bpc_flag_new != self.bpc_flag_old ):                               #   ...and ABPC status changed

                    if  ( self.bpc_flag_new == 0 ):                                         #       If we are not within simulation
                        stopBlending( self.stethoscope )                                    #       ...region, don't play anything

                    elif( self.bpc_flag_new == 1 ):                                         #       If we are within the 1st region
                        fileByte = definitions.KOROT                                        #       ...play this file
                        startBlending( self.stethoscope, fileByte)                          #       Send the trigger command

                    elif( self.bpc_flag_new == 2 ):                                         #       If we are within the 2nd region
                        fileByte = definitions.KOROT                                        #       ...play this file
                        startBlending( self.stethoscope, fileByte)                          #       Send the trigger command

                    elif( self.bpc_flag_new == 3 ):                                         #       If we are within the 3rd region
                        fileByte = definitions.KOROT                                        #       ...play this file
                        startBlending( self.stethoscope, fileByte)                          #       Send the trigger command

                    elif( self.bpc_flag_new == 4 ):                                         #       If we are within the 4th region
                        fileByte = definitions.KOROT                                        #       ...play this file
                        startBlending( self.stethoscope, fileByte)                          #       Send the trigger command
                        
                    self.bpc_flag_old = self.bpc_flag_new                                   #   Update flag
    
        for device_ID, device_BT in self.smartHandle.iteritems():
##            if( self.SH_holder_flag_new[ device_ID ] == 0 ):
            self.smartHandle_data[ device_ID ].append( ["%.02f" %self.simCurrentTime,
                                                        readDataStream( device_BT,
                                                                        '\n' )] )

# ========================================================================================= #
# Setup program
# ========================================================================================= #

# Get device info
print( "============= DEVICE  IDENTIFICATION =============" )
panel_id_file_path = dataDir + "/panels.txt"
_, _, panel_id, _ = panelSelfID( panel_id_file_path, getMAC("eth0") )

devices_id_file_path = dataDir + "/panel" + str( panel_id ) + "devices.txt"
_, device_name_list, device_bt_address_list = panelDeviceID( devices_id_file_path, panel_id )

smarthandle_name            = ( device_name_list[1],
                                device_name_list[2] )
smarthandle_bt_address      = ( [device_bt_address_list[1]],
                                [device_bt_address_list[2]] )
print( "==================================================\n" )


print( "============ ESTABLISHING  CONNECTION ============" )
# connecting to smartdevices (stethoscope/handles) ---------------------------------------- #
smartdevice = dict()
print( "{} Connecting to SmartDevices".format(fS()) )
for i in range( 0, 3 ):
    smartdevice[ device_name_list[i] ] = createBTPort( device_bt_address_list[i], 1 )       # Connect BT device

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
        USB  = createACMPort( i, baud, timeout )
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
print( "==================================================\n" )

# configuring stethoscope ----------------------------------------------------------------- #
print( "============== CONFIGURING  DEVICES ==============" )
for device_ID, device_BT_Obj in smartdevice.iteritems():
    if( device_ID == "stethoscope" ):
        if( args["scenario"] == 0 ):
            print( "{} Generating filename for audio data ".format(fS()) )
            randString = genRandString( 4 )
            print( "{} Generated : {}".format(fS(), randString) )
            print( "{} Setting Stethoscope Recording Mode ".format(fS()) )
            recMode = 0
            print( "{} Setting recording mode and filename".format(fS()) )
            setRecordingMode( device_BT_Obj, recMode )
            parseString( device_BT_Obj, randString )
            startRecording( device_BT_Obj )
            
    else:
        print( "{} Triggering {}".format(fS(), device_ID) )
        startDataStream( device_BT_Obj, 20, '\n' )
print( "==================================================\n" )

# ========================================================================================= #
# Data Gathering
# ========================================================================================= #

print( "================= DATA GATHERING =================" )
output = data_acquisition( args, device_name_list,
                           smartdevice, smartholder,
                           executionTimeStamp     )

ST_holder_data      = output.ST_holder_data
SH_holder_data      = output.SH_holder_data
smarthandle_data    = output.smartHandle_data
print( "==================================================\n" )

# ----------------------------------------------------------------------------------------- #
# Device Deactivation
# ----------------------------------------------------------------------------------------- #

print( "============== DEVICE  DEACTIVATION ==============" )
print( "{} Disconnecting bluetooth devices ".format(fS()) )

if  ( args["scenario"] == 0 ): stopRecording( smartdevice["stethoscope"] )
elif( args["scenario"] == 1 ): stopBlending ( smartdevice["stethoscope"] )
elif( args["scenario"] == 2 ): stopBlending ( smartdevice["stethoscope"] )

print( "{} Placing devices in IDLE mode and closing ports".format(fS()) )
for device_ID, device_BT_Obj in smartdevice.iteritems():
    if( device_ID == "stethoscope" ):
        setToIdle( device_BT_Obj )
    else:
        stopDataStream( device_BT_Obj, 20, '\n' )

    device_BT_Obj.close()

print( "{} Disconnecting USB devices ".format(fS()) )
for ID in smartholder:    
    if( smartholder[ ID ].is_open ):
        smartholder[ ID ].close()
print( "==================================================\n" )

# ========================================================================================= #
# Output
# ========================================================================================= #

print( "================== STORING DATA ==================" )
print( "{} Writting data to file ".format(fS()) )

if( path.exists( outputDir ) == False ):
    print( "{} Output directory not present ".format(fS()) )
    print( "{} Generating output directory ".format(fS()) )
    makedirs( outputDir )
else:
    print( "{} Found output directory ".format(fS()) )

stampedDir = outputDir + "/" + executionTimeStamp + "/"
if( path.exists( stampedDir ) == False ):
    print( "{} Time-stamped directory not present ".format(fS()) )
    print( "{} Generating time-stamped directory ".format(fS()) )
    makedirs( stampedDir )
else:
    print( "{} Found time-stamped directory ".format(fS()) )

smartholder_output_filename = stampedDir + "ST_holder.txt"

N_lines = len( ST_holder_data )

for i in range(0, N_lines):
    if( i == 0 ):
        with open(smartholder_output_filename, 'a') as dataFile:
            dataFile.write( fullStamp() + " Smart Holder for = " + device_name_list[0] + '\n' )
            dataFile.write( fullStamp() + " COM Port = " + str( portSTH ) + '\n')
    with open(smartholder_output_filename, 'a') as dataFile:
        dataFile.write( ST_holder_data[i][0] + "," + ST_holder_data[i][1] + '\n' )

# -------------------------------------SMARTHANDLES---------------------------------------- #

smarthandle_output_filename = ([ stampedDir + "oto.txt",
                                 stampedDir + "ophtho.txt" ])
smartholder_output_filename = stampedDir + "SH_holder.txt"

N_lines = ([ len( smarthandle_data[smarthandle_name[0]] ),
             len( smarthandle_data[smarthandle_name[1]] ),
             len( SH_holder_data ) ])

N_smarthandles = 2
for i in range(0, len( N_lines )):
    if( i < N_smarthandles ):
        for j in range(0, N_lines[i]):
            if( j == 0 ):
                with open(smarthandle_output_filename[i], 'a') as dataFile:
                    dataFile.write( fullStamp() + " Smart Handle = " + smarthandle_name[i] + '\n' )
                    dataFile.write( fullStamp() + " Bluetooth Address = " + str(smarthandle_bt_address[i]) + '\n')
            with open(smarthandle_output_filename[i], 'a') as dataFile:
                dataFile.write( smarthandle_data[smarthandle_name[i]][j][0] + "," + smarthandle_data[smarthandle_name[i]][j][1] + '\n' )
    else:
        for j in range(0, N_lines[i]):
            if( j == 0 ):
                with open(smartholder_output_filename, 'a') as dataFile:
                    dataFile.write( fullStamp() + " Smart Holder " + '\n' )
                    dataFile.write( fullStamp() + " COM Port = " + str( portSHH ) + '\n')
            with open(smartholder_output_filename, 'a') as dataFile:
                dataFile.write( SH_holder_data[j][0] + "," + SH_holder_data[j][1] + "," + SH_holder_data[j][2] + '\n' )



# zipping output
#print( fullStamp() + " Compressing data " )
#os.system("cd " + consDir + "; sudo zip -r " + consDir + "output.zip output")
print( "==================================================\n" )

# ----------------------------------------------------------------------------------------- #
# END
# ----------------------------------------------------------------------------------------- #
print( "{} Program completed ".format(fS()) )
print( "{} AOK".format(fS()) )
