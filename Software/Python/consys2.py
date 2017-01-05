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
from    os.path                import expanduser

# PD3D Modules
from    timeStamp              import fullStamp
from    configurationProtocol  import *
from    bluetoothProtocol      import *
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
    selectedScenario = 0

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

time.sleep(1)
print fullStamp() + " Connecting Smart Holder"
rfObject = createPort(0, 250000, None)

# Triggering Smart Handle Devices
time.sleep(1)
print fullStamp() + " Triggering SH0"
triggerDevice2(sh0,"SH")

time.sleep(1)
print fullStamp() + " Triggering SH1"
triggerDevice2(sh1,"SH")

time.sleep(1)
print fullStamp() + " Triggering Smart Holder"
triggerDevice(rfObject,deviceTypes[2])

# Openning Ports
time.sleep(1)
print fullStamp() + " Openning Serial Port to SH0"
if sh0.isOpen() == False:
    sh0.open()

time.sleep(1)
print fullStamp() + " Openning Serial Port to SH1"
if sh1.isOpen() == False:
    sh1.open()

time.sleep(1)
print fullStamp() + " Opening Serial Port to Smart Holder"
if rfObject.isOpen() == False:
    rfObject.open()

# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

simStartTime = time.time()
simCurrentTime = 0
simStopTime = 30
# simLoopCounter = 0
dataStream = []
print fullStamp() + " Starting Simulation Loop, time = %.03f seconds" %simStopTime

try:
    while simCurrentTime < simStopTime:

        # Handles
        dataStream.append(["%.02f" %simCurrentTime,
                           sh0.readline()[:-1],
                           sh1.readline()[:-1],
                           rfObject.readline()[:-1]])

        simCurrentTime = time.time() - simStartTime
        print fullStamp() + " Current Simulation Time = %.03f" %simCurrentTime
        # simLoopCounter = simLoopCounter + 1;

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

    time.sleep(1)
    if rfObject.isOpen == True:
        rfObject.close()

# print dataStream

# ----------------------------------------------
# Post-Simulation
#   Close Serial Ports
#   Disconnect Devices
#   Store Data
# ----------------------------------------------


# Close Serial Ports
time.sleep(0.25)
if sh0.isOpen() == True:
    sh0.close()

time.sleep(0.25)
if sh1.isOpen() == True:
    sh1.close()

time.sleep(0.25)
if rfObject.isOpen == True:
    rfObject.close()

# Stop Devices
time.sleep(0.25)
stopDevice2(sh0,deviceTypes[0])

time.sleep(0.25)
stopDevice2(sh1,deviceTypes[1])

time.sleep(0.25)                                          
stopDevice(rfObject,deviceTypes[2])

# Store Data


