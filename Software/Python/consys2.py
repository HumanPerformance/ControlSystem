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
from    sequentialPrompt       import *


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

###
# timerApp(timer1, timer2, timer3, direction)
# timer = time in SECONDS
# direction = "up" to start counting from 0 upwards
# direction = "down" to start from timer's upper bound downwards
###

timerApp(30, 30, 15, "down")


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

