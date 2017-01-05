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
from    threading              import Timer
from    os.path                import expanduser

# PD3D Modules: General
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
from    usbProtocol            import createPort

# PD3D Modules: Smart Handle
from    smarthandleProtocol    import triggerDevice2
from    smarthandleProtocol    import triggerDevices
from    smarthandleProtocol    import dataRead
from    smarthandleProtocol    import dataReadStreams
from    smarthandleProtocol    import dataWrite
from    smarthandleProtocol    import createDataFolder
from    smarthandleProtocol    import createDataFile
from    smarthandleProtocol    import stopDevice2
from    smarthandleProtocol    import stopDevices

# PD3D Modules: Smart Holder
from    smartHolderProtocol    import dataRead
from    smartHolderProtocol    import triggerDevice
from    smartHolderProtocol    import dataRead
from    smartHolderProtocol    import dataReadStreams
from    smartHolderProtocol    import dataWrite
from    smartHolderProtocol    import createDataFolder
from    smartHolderProtocol    import createDataFile
from    smartHolderProtocol    import stopDevice


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

#mac_bt = "B8:27:EB:DD:1F:86"   #Original address of panel in lab. Also changed in the .xml
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


configStartTime = time.time()
configCurrentTime = 0
configStopTime = 10 #timers[0]
configLoopCounter = 0
print fullStamp() + " Starting Configuration Loop, time = " + str(configStopTime) + " seconds"
while configCurrentTime < configStopTime:

    # Connect to listed devices...
    if configLoopCounter == 0:
        print fullStamp() + " Connecting smart devices"
        rfObject = createPort(0, 250000, None)

        time.sleep(1)
        print fullStamp() + " Triggering smart devices"
        triggerDevice(rfObject,deviceTypes[0])
        
        print fullStamp() + " Opening smart device communication"
        time.sleep(1)
        if rfObject.isOpen() == False:
            rfObject.open()
    
    configCurrentTime = time.time() - configStartTime
    configLoopCounter = configLoopCounter + 1

# End of Configuration Loop

# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------
'''
def endSim():
    print dataStream
    print "Closing rfObject"
    time.sleep(0.25)
    rfObject.close()
    time.sleep(0.25)
    stopDevice2(rfObject,deviceTypes[0])
    return
'''
simStartTime = time.time()
simCurrentTime = 0
simStopTime = 15
# simLoopCounter = 0
#dataStream = []
print fullStamp() + " Satrting Simulation Loop, time = " + str(simStopTime) + " seconds"
#end = Timer(simStopTime, endSim)
#end.start()
for i in range(1,6):
    simStartTime = time.time()
    simCurrentTime = 0
    dataStream=[]
    while simCurrentTime < simStopTime:
        
        # Handles
        dataStream.append( ["TIM,"+str(simCurrentTime),
                           rfObject.readline()[:-1]] )
        simCurrentTime = time.time() - simStartTime
        
        '''
        if rfObject.readline()[:-1] is not None:
            while rfObject.in_waiting is not 0:
                #print "Loop # " + str(i) + " TIM," + str(simCurrentTime) + " " + rfObject.readline()[:-1] + "\n"
                time.sleep(0.05)
                #print simCurrentTime
                simCurrentTime = time.time() - simStartTime

        # simLoopCounter = simLoopCounter + 1;
        '''
# End of Simulatio Loop
    #print dataStream
    print ''
    print "Loop # " + str(i)
    print "First Element: " + str(dataStream[0])
    print "Middle: " + str(dataStream[len(dataStream)/2])
    print "End: " + str(dataStream[len(dataStream)-1])
    print "Array Length: " + str(len(dataStream))
    
#print dataStream
print "Closing rfObject"
time.sleep(0.25)
rfObject.close()
time.sleep(0.25)                                          
stopDevice(rfObject,deviceTypes[0])

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
