'''
*
* CUSTOMIZED VERSION FOR DEMO PURPOSES
*
* Read pressure sensor and display readings on a dial gauge
*
* Adapted from: John Harrison's original work
* Link: http://cratel.wichita.edu/cratel/python/code/SimpleVoltMeter
*
* VERSION: 0.5
*   - MODIFIED: This iteration of the pressureDialGauge is not intended
*               as a standalone program. It is meant to work in conjunction
*               with the appJar GUI. Attempting to run this program as a
*               standalone will throw so many errors at you you will regret it!!!
*
* KNOWN ISSUES:
*   - Nada so far.
* 
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Mar. 07th, 2017 Year of Our Lord
* LAST CONTRIBUTION DATE    :   Feb. 16th, 2018 Year of Our Lord
*
'''

# ========================================================================================= #
# Import Libraries and/or Modules
# ========================================================================================= #

# Python modules
import  sys, time, bluetooth, serial, argparse                                              # 'nuff said
import  Adafruit_ADS1x15                                                                    # Required library for ADC converter
from    PyQt4                                   import QtCore, QtGui, Qt                    # PyQt4 libraries required to render display
from    PyQt4.Qwt5                              import Qwt                                  # Same here, boo-boo!
from    numpy                                   import interp                               # Required for mapping values
from    threading                               import Thread                               # Run functions in "parallel"
from    os                                      import getcwd, path, makedirs               # Pathname manipulation for saving data output

# PD3D modules
from    dial_v2                                 import Ui_MainWindow
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

from    timeStamp                               import fullStamp
from    bluetoothProtocol_teensy32              import *
from    stethoscopeProtocol                     import *
import  stethoscopeDefinitions                  as     definitions


# ========================================================================================= #
# Variables
# ========================================================================================= #

executionTimeStamp = fullStamp()                                                            # generating execution time stamp 

# ----------------------------------------------------------------------------------------- #
# Constructing argument parser
# ----------------------------------------------------------------------------------------- #

ap = argparse.ArgumentParser()

ap.add_argument( "-s", "--samplingFrequency", type=float, default=0.25,                     # sampling frequency for pressure measurement
                help="Set sampling frequency (in secs).\nDefault=0.25" )

ap.add_argument( "-b", "--bumpFrequency", type=float, default=0.75,                         # Simulated bump frequency
                help="Set synthetic bump frequency (in secs).\nDefault=0.75" )

ap.add_argument( "-d", "--debug", action='store_true',                                      # debug mode --mo
                help="Invoke flag to enable debugging" )

#ap.add_argument( "--directory", type=str, default='output',                                # directory --will remove
#                help="Set directory" )

ap.add_argument( "--destination", type=str, default="output.txt",
                help="Output directory" )

#ap.add_argument( "--stethoscope", type=str, default="00:06:66:8C:D3:F6",
#                help="Choose stethoscope" )

ap.add_argument( "-m", "--mode", type=str, default="REC",                                   # reconrding or simulation mode
                help="Mode to operate under; SIM: Simulation || REC: Recording" )

ap.add_argument( "-lp", "--lower_pressure", type=str, default=75,                           # set lower pressure limit as an input (for SIM only)
                help="Lower Pressure Limit (only for SIM)" )

ap.add_argument( "-hp", "--higher_pressure", type=str, default=125,                         # set higher pressure limit as an input (for SIM only)
                help="Higher Pressure Limit (only for SIM)" )
args = vars( ap.parse_args() )


# ========================================================================================= #
# Program Configuration
# ========================================================================================= #

class MyWindow(QtGui.QMainWindow):

    pressureValue = 0
    lastPressureValue = 0
    
    def __init__( self, parent=None ):

        # Initialize program and extract dial GUI
        QtGui.QWidget.__init__( self, parent )
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        self.thread = Worker( self )

        # Close rfObject socket on exit
        #self.ui.pushButtonQuit.clicked.connect( self.cleanUp )

        # Setup gauge-needle dimensions
        self.ui.Dial.setOrigin( 90.0 )
        self.ui.Dial.setScaleArc( 0.0, 340.0 )
        self.ui.Dial.update()
        self.ui.Dial.setNeedle( Qwt.QwtDialSimpleNeedle(
                                                        Qwt.QwtDialSimpleNeedle.Arrow,
                                                        True, Qt.QColor(Qt.Qt.red),
                                                        Qt.QColor(Qt.Qt.gray).light(130)
                                                        )
                                )

        self.ui.Dial.setScaleOptions( Qwt.QwtDial.ScaleTicks |
                                      Qwt.QwtDial.ScaleLabel | Qwt.QwtDial.ScaleBackbone )

        # Small ticks are length 5, medium are 15, large are 20
        self.ui.Dial.setScaleTicks( 5, 15, 20 )
        
        # Large ticks show every 20, put 10 small ticks between
        # each large tick and every 5 small ticks make a medium tick
        self.ui.Dial.setScale( 10.0, 10.0, 20.0 )
        self.ui.Dial.setRange( 0.0, 300.0 )
        self.ui.Dial.setValue( 0 )

        # Unpack argumnet parser parameters as attributes
        # self.directory      = args["directory"]
        self.destination    = args["destination"]
        # self.address        = args["stethoscope"]
        self.mode           = args["mode"]
        self.lp             = args["lower_pressure"]
        self.hp             = args["higher_pressure"]

        # Boolean to control recording function
        #self.init_rec = True

        # List all available BT devices
        self.ui.Dial.setEnabled( True )
        #self.ui.pushButtonPair.setEnabled( False )
        #self.ui.pushButtonPair.setText(QtGui.QApplication.translate("MainWindow", "Paired", None, QtGui.QApplication.UnicodeUTF8))
        
        # set timeout function for updates
        self.ctimer = QtCore.QTimer()                                               # Define timer
        QtCore.QObject.connect( self.ctimer,                                        # Connect signals...
                                QtCore.SIGNAL( "timeout()" ),                       # to slots.
                                self.UpdateDisplay )                                # ...
        self.ctimer.start( 10 )                                                     # Start timed thread

        # Set timeout function for writing to log
        millis = int( args["samplingFrequency"]*1000 )                              # Cast into integer
        self.log_timer = QtCore.QTimer()                                            # Define timer
        QtCore.QObject.connect( self.log_timer,                                     # Connect signals...
                                QtCore.SIGNAL( "timeout()" ),                       # to slots.
                                self.thread.write_log )                             # ...
        self.log_timer.start( millis )                                              # Start timed thread

        # Create logfile
        self.setup_log()

# ------------------------------------------------------------------------
    '''
    --- v1.0
    --- Removed as this will be done externally
    
    def connectStethoscope( self, address ):
        """
        Connect to stethoscope.
        """
        
        self.thread.deviceBTAddress = str( address )                                # Set BT address
        self.ui.Dial.setEnabled( True )                                             # Enable dial
        self.ui.pushButtonPair.setEnabled( False )                                  # Disable pushbutton

        # Create logfile
        self.setup_log()
        
        # set timeout function for updates
        self.ctimer = QtCore.QTimer()                                               # Define timer
        QtCore.QObject.connect( self.ctimer,                                        # Connect signals...
                                QtCore.SIGNAL( "timeout()" ),                       # to slots.
                                self.UpdateDisplay )                                # ...
        self.ctimer.start( 10 )                                                     # Start timed thread

        # Set timeout function for writing to log
        millis = int( args["samplingFrequency"]*1000 )                              # Cast into integer
        self.log_timer = QtCore.QTimer()                                            # Define timer
        QtCore.QObject.connect( self.log_timer,                                     # Connect signals...
                                QtCore.SIGNAL( "timeout()" ),                       # to slots.
                                self.thread.write_log )                             # ...
        self.log_timer.start( millis )                                              # Start timed thread
    '''
# ------------------------------------------------------------------------
 
    def UpdateDisplay( self ):
        """
        Update DialGauge display with the most recent pressure readings.
        """
        
        if( self.pressureValue != self.lastPressureValue ):

            self.ui.Dial.setValue( self.pressureValue )                             # Update dial GUI
            self.lastPressureValue = self.pressureValue                             # Update variables

# ------------------------------------------------------------------------
    '''
    --- v1.0
    --- Removed as this will be done externally
    
    def scan_rfObject( self ):
        """
        Scan for available BT devices.
        Returns a list of tuples (num, name)
        """
        
        available = []
        BT_name, BT_address = findSmartDevice( deviceBTAddress[0] )
        if( BT_name != 0 ):
            available.append( (BT_name[0], BT_address[0]) )
            return( available )
    '''
# ------------------------------------------------------------------------

    def setup_log( self ):
        """
        Setup directory and create logfile.
        """
        
        # Create data output folder/file
        outDir = consDir + "output/"                                                        # find or generate the main output directory
        if( path.exists( outDir ) == False ):
            #print( fullStamp() + " Output directory not present " )
            #print( fullStamp() + " Generating output directory " )
            makedirs( outDir )
        #else:
            #print( fullStamp() + " Found output directory " )                          

        stampedDir = outDir + args["destination"] + "/"                                      # find or generate the time-stamped output directory
        if( path.exists( stampedDir ) == False ):
            #print( fullStamp() + " Time-stamped directory not present " )
            #print( fullStamp() + " Generating time-stamped directory " )
            makedirs( stampedDir )
        #else:
            #print( fullStamp() + " Found time-stamped directory " )
        
        self.dataFileDir = stampedDir
        self.dataFileName = stampedDir + "bpcu.txt"

        with open( self.dataFileName, "w" ) as f:                                   # Write down info as ...
            f.write( "Date/Time     :  {}\n".format(fullStamp())    )               # a header on the ...
            f.write( "Scenario      : #{}\n".format(scenarioNumber) )               # output file.
            f.write( "Device Name   :  {}\n".format(deviceName)     )               # ...
            f.write( "seconds,    kPa , mmHg Actual, mmHg Simulated, SIM\n" )       # ...
            f.close()                                                               # ...
            #print( fullStamp() + " Created data output .txt file" )                 # [INFO] Status

# ------------------------------------------------------------------------

    def cleanUp( self ):
        """
        Clean up at program exit.
        Stops recording and closes communication with device
        """
        
        #print( fullStamp() + " Goodbye!" )
        QtCore.QThread.sleep( 2 )                               # this delay may be essential


# ========================================================================================= #
# Class for optional, independent thread
# ========================================================================================= #

class Worker( QtCore.QThread ):

    # Create flags for what mode we are running
    normal      = True                                                              # normal state, out of the simulated pressure range
    playback    = False                                                             # simulated state, within the simulated pressure range
    recent      = playback                                                          # most recent state                                                                  
    
    # Define sampling frequency (units: sec) controls writing frequency
    wFreq = args["samplingFrequency"]                                               # Frequency at which to write data
    wFreqTrigger = time.time()                                                      # Trigger counter ^
    
    def __init__( self, parent = None ):
        QtCore.QThread.__init__( self, parent )
##        self.exiting = False                                                        # Not sure what this line is for

##        print( fullStamp() + " Initializing Worker Thread" )

        # Pressure reading variables
        self.P_Pscl     = 0                                                         # Pressure in Pascal
        self.P_mmHg_0   = 0                                                         # Pressure in mmHg (real)
        self.P_mmHg     = 0                                                         # Pressure in mmHg (simulated)
        
        # LobOdeh and EMA filter stuff
##        self.m, self.last_m = 0, 0                                                  # Slopes
##        self.b, self.last_b = 0, 0                                                  # y-intercepts
##        self.t, self.last_t = 0, 0                                                  # Time step (x-axis)
        self.initialRun = True                                                      # Store initial values at first run
        self.filterON   = False                                                     # Filter boolean
        self.at_marker  = False                                                     # Marker (EMA trigger points) boolean

        # Synthetic bump frequency
        self.bumpFreq = args["bumpFrequency"]                                       # Frequency at which to synthesize a pulse
        self.bumpTrigger = time.time()                                              # Trigger counter ^
        
        # Start
        self.owner = parent
        self.start()

# ------------------------------------------------------------------------

    def __del__(self):
        print( fullStamp() + " Exiting Worker Thread" )

# ------------------------------------------------------------------------

    def run(self):
        """
        This method is called by self.start() in __init__()
        """
        
        try:
            
            self.startTime = time.time()                                            # Store initial time (for timestamp)
            
            while( True ):                                                          # Loop 43va!
                val = self.readPressure()                                           # Read pressure

                # Synthesize pulse if conditions are met
                if( 75 <= val and val <= 125                                        # Check conditions 
                    and time.time() - self.bumpTrigger >= self.bumpFreq             # ...
                    and self.filterON ):                                            # ...

                    if( args["debug"] ):                                            # [INFO] update
                        print( "\n[INFO] Synthesizing pulse..." )                   # ...
                    
                    self.bumpTrigger = time.time()                                  # Reset timer
                    self.synthesize_pulse( val )                                    # Synthesize pulse

                # Otherwise don't
                else:
                    self.owner.pressureValue = val                                  # ... 

        except Exception as instance:
            print( fullStamp() + " Failed to connect" )                             # Indicate error
            print( fullStamp() + " Exception or Error Caught" )                     # ...
            print( fullStamp() + " Error Type " + str(type(instance)) )             # ...
            print( fullStamp() + " Error Arguments " + str(instance.args) )         # ...

# ------------------------------------------------------------------------

    def readPressure( self ):
        """
        Read pressure transducer and convert voltage into pressure readings
        """
        
        # Compute pressure
        V_analog        = ADC.read_adc( 0, gain=GAIN )                              # Convert analog readings to digital
        V_digital       = interp( V_analog, [1235, 19279.4116], [0.16, 2.41] )      # Map the readings
        self.P_Pscl     = ( V_digital/V_supply - 0.04 )/0.018                       # Convert voltage to SI pressure readings
        self.P_mmHg_0   = self.P_Pscl*760/101.3                                     # Convert SI pressure to mmHg (0==original)

        # Criteria to turn ON  filter
        if( self.P_mmHg_0 >= 180 and self.at_marker == False):
            self.filterON   = True                                                  # Flag filter to turn ON
            self.at_marker  = True                                                  # Flag that we hit the marker

            if( args["debug"] ):                                                    # [INFO] Status
                print( "[INFO] Filter ON" )                                         # ...

        # Criteria to turn OFF filter
        elif( self.P_mmHg <= 40 and self.at_marker and self.filterON ):
            self.filterON   = False                                                 # Flag filter to turn OFF
            self.at_marker  = False                                                 # Reset marker flag                                                   
            self.initialRun = True                                                  # Store initial values at first run

            if( args["debug"] ):                                                    # [INFO] Status
                print( "[INFO] Filter OFF" )                                        # ...

        # If filter is ON, apply it
        if( self.filterON ):
            self.t       = time.time() - self.startTime                             # [DEPRACATED] Used for LobOdeh
            self.P_mmHg  = self.EMA(self.P_mmHg_0, ALPHA=0.03)                      # Apply EMA filter

        else:
            pass

        if( self.playback is not self.recent ):
            if( self.playback == True ):
                print( "SIM, 1")                                                    # within simulated pressure range
            elif( self.playback == False ):
                print( "SIM, 0")                                                    # outside simulated pressure range
            #print( "SIM %r" %(self.playback) )
            self.recent = self.playback
            
        # Use simulated data
        if( self.filterON ):
            if( self.owner.mode == "SIM" ): self.sim_mode( self.P_mmHg )            # Trigger simulations mode (if --mode SIM)
            else: self.rec_mode()                                                   # Trigger recording   mode (if --mide REC)
            
            return( self.P_mmHg )                                                   # Return pressure readings in mmHg

        # Use real data
        else:
            if( self.owner.mode == "SIM" ): self.sim_mode( self.P_mmHg_0 )          # Trigger simulations mode (if --mode SIM)
            else: self.rec_mode()                                                   # Trigger recording   mode (if --mide REC)

            return( self.P_mmHg_0 )                                                 # Return pressure readings in mmHg

# ------------------------------------------------------------------------

    def sim_mode( self, P ):
        """
        In charge of triggering simulations
        """
        
        lp = float( args["lower_pressure"] )
        hp = float( args["higher_pressure"] )
        
        # Error handling (1)
        try:
            # Entering simulation pressure interval
            if (P >= lp) and (P <= hp) and (self.playback == False):
                self.normal = False                                                 # Turn OFF normal playback
                self.playback = True                                                # Turn on simulation

            # Leaving simulation pressure interval
            elif ((P < lp) or (P > hp)) and (self.normal == False):
                self.normal = True                                                  # Turn ON normal playback
                self.playback = False                                               # Turn OFF simulation

        # Error handling (2)        
        except Exception as instance:
            print( "" )                                                             # ...
            print( fullStamp() + " Exception or Error Caught" )                     # ...
            print( fullStamp() + " Error Type " + str(type(instance)) )             # Indicate the error
            print( fullStamp() + " Error Arguments " + str(instance.args) )         # ...

# ------------------------------------------------------------------------

    """
    --- v1.0
    --- Removed as this will be done externally

    def rec_mode( self ):
        
        #In charge of triggering recordings
        
        
        if( self.owner.init_rec == True ):
            self.owner.init_rec = False
            #statusEnquiry( self.rfObject )
            #startCustomRecording( self.rfObject, self.owner.destination )           # If all is good, start recording

        else: pass
    """   

# ------------------------------------------------------------------------

    def write_log( self ):
        """
        Write to log file.

        Inputs:-
            - NONE

        Output:-
            - NONE
        """

        try:
            self.wFreqTrigger = time.time()                                         # Reset wFreqTrigger
            stamp = time.time()-self.startTime                                      # Time stamp

            # Write to file
            dataStream = "%6.2f , %6.2f , %11.2f, %14.2f, %4r\n" %( stamp,          # Format readings into ...
                                                                    self.P_Pscl,    # desired form.
                                                                    self.P_mmHg_0,  # ...
                                                                    self.owner.pressureValue,
                                                                    self.playback )

            with open( self.owner.dataFileName, "a" ) as f:
                f.write( dataStream )                                               # Write to file
                f.close()                                                           # Close file

        except:
            pass
        
# ------------------------------------------------------------------------

    def EMA( self, data_in, ALPHA=0.03 ):
        """
        Exponential Moving Average (EMA) filter

        Inputs:-
            - data_in   : Data to be smoothed
            - ALPHA     : Filtering weight

                          High ALPHA: NO SMOOTHING
                    ( Disregards previous data points )
                          Low  ALPHA: HELLUVA SMOOTHING
                ( Complete dependence on previous data points )

        Output:-
            - self.ema  : Filtered data
        """
        
        if( self.initialRun ):
            self.ema        = data_in                                               # Store ema_0
            self.initialRun = False                                                 # Flag initialRun as False

        else:
            self.ema        = ALPHA * data_in + (1.0-ALPHA)*self.ema                # Filter

        return( self.ema )                                                          # Return smoothed data

# ------------------------------------------------------------------------

    def synthesize_pulse( self, val ):
        """
        Synthesize pulse

        INPUTS:-
            - val : Data point that will be used as a start and
                    end value for the synthesized pulse

        OUTPUT:-
            - NONE
        """
        
        # Increment
        for i in range( 0, 6 ):
            self.owner.pressureValue = val * ( 1 + i/1000. )
            time.sleep(0.01)
            if( args["debug"] ):                                                    # [INFO] Status
                print( "[INFO] Dial @ {}".format(self.owner.pressureValue) )        # ...

        # Decrement
        for i in range( -5, 1 ):
            self.owner.pressureValue = val * -1*( -1 + i/1000. )
            time.sleep(0.01)
            if( args["debug"] ):                                                    # [INFO] Status
                print( "[INFO] Dial @ {}".format(self.owner.pressureValue) )        # ...

            
# ========================================================================================= #
# SETUP
# ========================================================================================= #
port = 1                                                                                    # Port number to use in communication
deviceName = "Blood Pressure Cuff"                                                          # Designated device name
scenarioNumber = 1                                                                          # Device number

V_supply = 3.3                                                                              # Supply voltage to the pressure sensor

ADC = Adafruit_ADS1x15.ADS1115()                                                            # Initialize ADC
GAIN = 1                                                                                    # Read values in the range of +/-4.096V

# ========================================================================================= #
# MAIN
# ========================================================================================= #

def main():
    
    print( fullStamp() + " Booting DialGauge" )
    app = QtGui.QApplication(sys.argv)
    MyApp = MyWindow()
    MyApp.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    sys.exit( main() )
