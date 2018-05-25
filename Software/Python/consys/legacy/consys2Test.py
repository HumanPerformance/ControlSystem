"""
consys2.py

Control System 2

The following script has been design to coordinate the device triggering, time-monitoring, and data collection of the instrument panels.
The script executes the foloowing sequence:

1 - Panel identification
2 - Scenario identification
3 - Pull instruments
4 - Pull parameters
            
Fluvio L. Lobo Fenoglietto 12/19/2016
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
# Python modules
import  sys
import  os
import  serial
import  time
from    multiprocessing        import Process
from    os.path                import expanduser

# PD3D Modules
from    timeStamp              import fullStamp
from    sequentialPrompt       import timerApp
from    configurationProtocol  import *
from    bluetoothProtocol      import *
from    usbProtocol            import *
from    smarthandleProtocol    import *
from    smartHolderProtocol    import * 

# ==============================================
# Variables
# ==============================================

# ----------------------------------------------
# Input Terminal Variables
#   The script reads the inputs from the terminal execution triggered by the Control Room
#   Consys currently handles one (1) input variable, the "scenario #"
# ----------------------------------------------
try:
    inputArg = sys.argv
    selectedScenario = int(sys.argv[1])
    print fullStamp() + " User Executed " + inputArg[0] + ", scenario #" + inputArg[1]
except:
    selectedScenario = 1

# ----------------------------------------------
# Panel self-dentification
#   The panel obtains the mac address of the local system
# ----------------------------------------------
mac_bt = getMAC('eth0')

# ----------------------------------------------
# Timers
# ----------------------------------------------
executionTimeStamp = fullStamp()

# ----------------------------------------------
# Path/Directory Variables
# ----------------------------------------------
pythonDir, configDir, configFile, dataDir, outputDir = definePaths()

# ----------------------------------------------
# Upload Configuration XML
# ----------------------------------------------
tree, root = readConfigFile(configFile)

# ----------------------------------------------
# Define Panel
#   Using the MAC address from the local system and the configuration XML, the program identifies the SIP id and index
# ----------------------------------------------
panelIndex, panelID = selfID(mac_bt, tree, root)

# ----------------------------------------------
# Define Scenario
#   Using the scenario number from the terminal input and the configuration XML, the program identifies the scenarion index
# ----------------------------------------------
scenarioIndex, scenarioNumber, scenarioID = findScenario(selectedScenario, tree, root)

# ----------------------------------------------
# Pull Scenario Info
#   This functions pulls relevant information about the scenarios from the configuration XML
# ----------------------------------------------
timers = pullParameters(scenarioIndex, tree, root)

# ----------------------------------------------
# Pull and Cross-Reference Devices
#   This function pulls the devices to be used in the selected scenario from the configuration XML
#   Then uses that list to croo-reference the addresses of the devices associated with the selected instrument panel
#   Returns the list of device names and addresses for execution
# ----------------------------------------------
scenarioDeviceNames = pullInstruments(panelIndex, scenarioIndex, tree, root)
deviceIndex, deviceTypes, deviceNames, deviceAddresses = instrumentCrossReference(panelIndex, scenarioDeviceNames, tree, root)

# ==============================================
# Operation
# ==============================================

# ----------------------------------------------
# Pre-Simulation / Configuration Loop
#   The following while-loop will preceed the simulatio loop
#   This loop works as a configuration step
# ----------------------------------------------

print fullStamp() + " Start Configuration"

# Creating Serial Port for Devices
time.sleep(1)
print fullStamp() + " Creating port for SH0"
sh0 = createPortS(deviceTypes[0],0,deviceAddresses[0],115200,5)

time.sleep(1)
print fullStamp() + " Creating port for SH1"
sh1 = createPortS(deviceTypes[1],1,deviceAddresses[1],115200,5)

"""
time.sleep(1)
print fullStamp() + " Connecting Smart Holder"
hld = createUSBPort(deviceTypes[2],1,115200,5)
"""

# Triggering Smart Handle Devices
time.sleep(1)
print fullStamp() + " Triggering SH0"
triggerDevice2(sh0,"SH")

time.sleep(1)
print fullStamp() + " Triggering SH1"
triggerDevice2(sh1,"SH")

"""
time.sleep(1)
print fullStamp() + " Triggering Smart Holder"
triggerDevice(hld,deviceTypes[2])
"""

# Openning Ports
time.sleep(1)
print fullStamp() + " Openning Serial Port to SH0"
if sh0.isOpen() == False:
    sh0.open()

time.sleep(1)
print fullStamp() + " Openning Serial Port to SH1"
if sh1.isOpen() == False:
    sh1.open()

"""
time.sleep(1)
print fullStamp() + " Opening Serial Port to Smart Holder"
if hld.isOpen() == False:
    hld.open()
"""

# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

time.sleep(5)

global dataStream
dataStream = []
def fetchData(simDuration, dataStream):

    simStartTime = time.time()
    simCurrentTime = 0
    simStopTime = simDuration
    print fullStamp() + " Starting Simulation Loop, time = %.03f seconds" %simStopTime


    # print fullStamp() + " Starting SubProcess"
    # subP = subprocess.Popen(['python','exeOne.py'])

    try:
        while simCurrentTime < simStopTime:
            
            # Handles
            
            dataStream.append(["%.02f" %simCurrentTime,
                               sh0.readline()[:-1],
                               sh1.readline()[:-1]])
                               #hld.readline()[:-1]])
            
            simCurrentTime = time.time() - simStartTime
            print fullStamp() + " Current Simulation Time = %.03f" %simCurrentTime
 
            # End of Simulation Loop
            
    except Exception as instance:
        print fullStamp() + " Exception or Error Caught"
        print fullStamp() + " Error Type " + str(type(instance))
        print fullStamp() + " Error Arguments " + str(instance.args)
        print fullStamp() + " Closing Open Ports"

        
        time.sleep(1)
        if sh0.isOpen() == True:
            sh0.close()

        time.sleep(1)
        if sh1.isOpen() == True:
            sh1.close()

        """
        time.sleep(1)
        if hld.isOpen == True:
            hld.close()
        """
    return dataStream

###
# timerApp(timer1, timer2, timer3, direction)
# timer = time in SECONDS
# direction = "up" to start counting from 0 upwards
# direction = "down" to start from timer's upper bound downwards
###

timer1 = 5
timer2 = timers[0]
timer3 = 5
simStopTime = (timer1 + timer2 + timer3)
process_1 = Process( target=timerApp, args=(timer1, timer2 , timer3, "down",) )
process_1.start()
process_2 = Process( target=fetchData, args=(simStopTime,dataStream,) )
process_2.start()
process_2.join()

print len(dataStream)
print dataStream[0]
print dataStream[10]
print dataStream[len(dataStream)-10]

print fullStamp() + " Data Collection Terminated"
print fullStamp() + " Ending Communication with Devices"

time.sleep(0.25)
if sh0.isOpen() == True:
    sh0.close()

time.sleep(0.25)
if sh1.isOpen() == True:
    sh1.close()

print "ports closed"
"""
time.sleep(0.25)
if hld.isOpen == True:
    hld.close()
"""

time.sleep(0.25)
stopDevice2(sh0,deviceTypes[0])

time.sleep(0.25)
stopDevice2(sh1,deviceTypes[1])

"""
time.sleep(0.25)                                          
stopDevice(hld,deviceTypes[2])
"""

"""
# ----------------------------------------------
# Data Storage
# ----------------------------------------------

# Print data on device-specific text files
Ndevices = len(deviceNames)
Nlines = len(dataStream)

dataFileDir = outputDir + "/" + executionTimeStamp

if os.path.exists(dataFileDir) == False:
    os.makedirs(dataFileDir)

for i in range(0,Ndevices):
    
    dataFileName = "/" + deviceNames[i] + ".txt"
    dataFilePath = dataFileDir + dataFileName
    
    if os.path.isfile(dataFilePath) == False:
        
        with open(dataFilePath, "a") as dataFile:
            dataFile.write("===================== \n")
            dataFile.write("Scenario = " + str(scenarioNumber) + "\n")
            dataFile.write("Instrument = " + deviceNames[0] + "\n")
            dataFile.write("This is a header line \n")
            dataFile.write("===================== \n")
    
    for j in range(0,Nlines):

        with open(dataFilePath, "a") as dataFile:
            dataFile.write(dataStream[j][0] + "," + dataStream[j][i+1] + "\n")


# zip output folder for data delivery

# find data directory
# command "sudo zip -r output.zip output"
#os.system("sudo zip -r " + dataDir + "/" + "output.zip output")
os.system("cd " + dataDir + "; sudo zip -r " + panelID + ".zip output")
"""
