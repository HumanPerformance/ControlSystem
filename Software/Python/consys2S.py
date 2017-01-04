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
from    configurationProtocol  import getMAC
from    configurationProtocol  import definePaths
from    configurationProtocol  import readConfigFile
from    configurationProtocol  import selfID
from    configurationProtocol  import findScenario
from    configurationProtocol  import pullParameters
from    configurationProtocol  import pullInstruments
from    configurationProtocol  import instrumentCrossReference
from    bluetoothProtocol      import createPort2
from    bluetoothProtocol      import createPorts2
from    bluetoothProtocol      import createPortS
from    smarthandleProtocol    import triggerDevice2
from    smarthandleProtocol    import triggerDevices
from    smarthandleProtocol    import dataRead
from    smarthandleProtocol    import dataReadStreams
from    smarthandleProtocol    import dataWrite
from    smarthandleProtocol    import createDataFolder
from    smarthandleProtocol    import createDataFile
from    smarthandleProtocol    import stopDevice2
from    smarthandleProtocol    import stopDevices

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

rfObject = createPortS(deviceTypes[1],deviceAddresses[1],115200,5)

# triggering device
time.sleep(1)
triggerDevice2(rfObject,"SH")

# openning device
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()

"""
configStartTime = time.time()
configCurrentTime = 0
configStopTime = 20 #timers[0]
configLoopCounter = 0
print fullStamp() + " Starting Configuration Loop, time = " + str(configStopTime) + " seconds"
while configCurrentTime < configStopTime:

    # Connect to listed devices...
    if configLoopCounter == 0:
        print fullStamp() + " Connecting smart devices"
        rfObject = createPortS(deviceTypes[0], deviceAddresses[0], 115200, 5)

        time.sleep(1)
        print fullStamp() + " Triggering smart devices"
        triggerDevice2(rfObject,deviceTypes[0])
        
        print fullStamp() + " Opening smart device communication"
        time.sleep(1)
        if rfObject.isOpen() == False:
            rfObject.open()
    
    configCurrentTime = time.time() - configStartTime
    configLoopCounter = configLoopCounter + 1

# End of Configuration Loop
"""
# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

simStartTime = time.time()
simCurrentTime = 0
simStopTime = 30
# simLoopCounter = 0
dataStream = []
print fullStamp() + " Starting Simulation Loop, time = " + str(simStopTime) + " seconds"

try:
    while simCurrentTime < simStopTime:

        # Handles
        dataStream.append( ["TIM,"+str(simCurrentTime), rfObjects.readline()[:-1]] )

        simCurrentTime = time.time() - simStartTime
        print fullStamp() + " Current Simulation Time = " + str(simCurrentTime)
        # simLoopCounter = simLoopCounter + 1;

        # End of Simulatio Loop
        
except Exception as instance:
    print fullStamp() + " Exception or Error Caught"
    print fullStamp() + " Error Type " + str(type(instance))
    print fullStamp() + " Error Arguments " + str(instance.args)
    print fullStamp() + " Closing Open Ports"
    time.sleep(1)
    if rfObject.isOpen() == True:
        rfObject.close()

# print dataStream

time.sleep(0.25)
if rfObject.isOpen() == True:
    rfObject.close()
time.sleep(0.25)
stopDevice2(rfObject,deviceTypes[0])


