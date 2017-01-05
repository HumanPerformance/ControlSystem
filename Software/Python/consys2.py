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

# Triggering Smart Handle Devices
time.sleep(1)
print fullStamp() + " Triggering SH0"
triggerDevice2(sh0,"SH")

time.sleep(1)
print fullStamp() + " Triggering SH1"
triggerDevice2(sh1,"SH")

# Openning Ports
time.sleep(1)
print fullStamp() + " Openning Serial Port to SH0"
if sh0.isOpen() == False:
    sh0.open()

time.sleep(1)
print fullStamp() + " Openning Serial Port to SH1"
if sh1.isOpen() == False:
    sh1.open()

# ----------------------------------------------
# Simulation
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

simStartTime = time.time()
simCurrentTime = 0
simStopTime = 30
# simLoopCounter = 0
dataStream = []
print fullStamp() + " Satrting Simulation Loop, time = " + str(simStopTime) + " seconds"

try:
    while simCurrentTime < simStopTime:

        # Handles
        dataStream.append( ["TIM,"+str(simCurrentTime),
                            sh0.readline()[:-1],
                            sh1.readline()[:-1]] )

        simCurrentTime = time.time() - simStartTime
        print fullStamp() + " Current Simulation Time = " + str(simCurrentTime)
        # simLoopCounter = simLoopCounter + 1
        
except Exception as instance:
    print fullStamp() + " Exception or Error Caught"
    print fullStamp() + " Error Type " + str(type(instance))
    print fullStamp() + " Error Arguments " + str(instance.args)
    print fullStamp() + " Closing Open Ports"
    time.sleep(1)
    if sh0.isOpen() == True:
        sh0.close()
    time.sleep(0.25)
    if sh1.isOpen() == True:
        sh1.close()

# End of Simulatio Loop

# ----------------------------------------------
# Post-Simulation
#   In this loop, devices will be disconnected
# ----------------------------------------------

# Closing Open Serial Ports
time.sleep(0.25)
print fullStamp() + " Closing Serial Port to SH0"
if sh0.isOpen() == True:
    sh0.close()

time.sleep(0.25)
print fullStamp() + " Closing Serial Port to SH1"
if sh1.isOpen() == True:
    sh1.close()

# Stopping Devices
time.sleep(1)
print fullStamp() + " Stopping SH0"
stopDevice2(sh0,deviceTypes[0])

time.sleep(1)
print fullStamp() + " Stopping SH1"
stopDevice2(sh1,deviceTypes[1])


"""
# ----------------------------------------------
# Load Configuration File
#   The program loads the configuration XML file to pull the relevant information
# ----------------------------------------------
# Loading configuration file using terminal input
scenarioNumberString = doubleDigitCorrection(inputArg[1])
scenarioConfigFileName = "/sc" + scenarioNumberString + ".txt"
scenarioConfigFile = scenarioConfigFilePath + scenarioConfigFileName
with open(scenarioConfigFile,'r+') as scenarioConfigFileObj:
    lines = scenarioConfigFileObj.readlines()

# Save loaded data into program variables
Nlines = len(lines)
scenarioConfigVariables = []
scenarioConfigValues = []
for i in range(0, Nlines-1):
    scenarioConfigVariables.append(lines[i].split(":")[0])
    scenarioConfigValues.append(lines[i].split(":")[1])
# print scenarioConfigVariables
# print int(scenarioConfigValues[1])

# ----------------------------------------------
# X.0 - Write Configuration File
# ----------------------------------------------
# Write configuration file for downstream parallel applications
with open(countdownConfigFile, 'r+') as countdownConfigFileObj:
    # Note: For the countdown application, only two inputs are currently needed: StartTime and WarningTime
    countdownConfigFileObj.write(scenarioConfigVariables[1] + ":" + str(scenarioConfigValues[1]))
    countdownConfigFileObj.write(scenarioConfigVariables[2] + ":" + str(scenarioConfigValues[2]))

# ----------------------------------------------
# X.0 - Connect Instrument(s)
# ----------------------------------------------
# Pull instrument information from the instrument configuration file
Ndevices, instrumentNames, instrumentBTAddress = pullInstruments(instrumentsConfigFile)
# Connect to instruments by creating bluetooth-serial (RFCOMM) ports
arduRFObj = createRFPort(instrumentNames, instrumentBTAddress)

# ----------------------------------------------
# X.0 - Execute Parallel Application(s)
# ----------------------------------------------
print "User may execute countdown application now"
#countdownExeFilePath = countdownDir
#countdownExeFileName = "/countdown"
#terminalCommand = "DISPLAY=:0.0; " + countdownExeFilePath + countdownExeFileName + " &"
#os.system(terminalCommand)
time.sleep(5)

# ----------------------------------------------
# X.0 - Data Acquisition Timed-Loop
# ----------------------------------------------
startTime = time.time()
currentTime = 0
stopTime = 10 # seconds

while currentTime < stopTime:
        #
        # Operation

        # Loop through all devices
        for i in range(0,Ndevices):

            # Read data from device
            inString = dataRead(arduRFObj[i])

            # Write data from device
            dataWrite(executionTimeStamp, currentTime, outputFilePath, instrumentNames[i], inString)

        # Update time
        currentTime = time.time() - startTime
        # print currentTime

print "Program Concluded"

stopRFInstruments(arduRFObj, instrumentNames)
"""

"""
References
1- Defining Functions in Python - http://www.tutorialspoint.com/python/python_functions.htm
2- Calling Functions from other Python scripts - http://stackoverflow.com/questions/20309456/how-to-call-a-function-from-another-file-in-python
3- "       "         "    "     "      "       - http://stackoverflow.com/questions/7701646/how-to-call-a-function-from-another-file
4- Returning multiple variables from python function/script - http://stackoverflow.com/questions/354883/how-do-you-return-multiple-values-in-python
5- Writing to Serial on Python - http://playground.arduino.cc/Interfacing/Python
"""
