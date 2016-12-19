"""
configurationProtocol.py

The following python module contains fuctions specific to the management of configuration files within the control system

Fluvio L Lobo Fenoglietto
09/01/2016


List of functions ::

X - Read configuration (.XML) file
X - Write configuration (.XML) file

"""

# Import External Modules
from os.path import expanduser
from timeStamp import fullStamp
import xml.etree.ElementTree as etree

# Get MAC address
#   The following function returns the MAC address of the input interface
#   Input   ::  {string}    interface   eth0, wlan0
#   Output  ::  {string}    MAC address
def getMAC(interface):
    print fullStamp() + " getMAC()"
    print fullStamp() + " Searching MAC address for " + interface + " module"
    try:
        address = open("/sys/class/net/" + interface + "/address").read()[:-1]
        print fullStamp() + " MAC (" + interface + "): " + address
        return address
    except:
        print fullStamp() + " Failed to find address, check input interface"

# Define Path Variables
#   The following function defines the path variables for the relevant directories used throughout the control system functions
#   The program does not handle other operating systems
def definePaths():
    print fullStamp() + " definePaths()"
    homeDir = expanduser("~")                                                                   # Use expand-user to identify the home directory
    rootDir = "/root"                                                                           # This is the returnof expand-user if the function is executed within a raspbian system
    if homeDir == rootDir:
        print fullStamp() + " OS - Raspbian OS"
        homeDir = "/home/pi"                                                                    # if the two strings are equivalent, then the program must have been executed from a raspbian system. A correction to the home directory has to be made.
        pythonDir = homeDir + "/pd3d/csec/repos/ControlSystem/Software/Python"                  # Python directory
        configDir = pythonDir + "/configuration"                                                # Configuration directory
        configFile = configDir + "/config.xml"                                           # Configuration file
        dataDir = pythonDir + "/data"                                                           # Data directory
        outputDir = dataDir + "/output"                                                         # Output directory
    else:
        print fullStamp() + " User executed function on an OS that is not supported..."
        pythonDir = 0
        configDir = 0
        configFile = 0
        dataDir = 0
        outputDir = 0
    return pythonDir, configDir, configFile, dataDir, outputDir

# Read Configuration (.XML) File
#   Reads or imports information from configuration file into an object or structure
#   Input  :: path to configuration file (string)
#   Output :: configuration file structure
def readConfigFile(configFile):
    print fullStamp() + " readConfigFile()"
    tree = etree.parse(configFile)
    root = tree.getroot()
    return tree, root

# Self Identification
#   This function uses the MAC address of the control system to identify itself within the configuration XML file
#   Input   ::  {string}        MAC address
#           ::  {structure}     tree
#           ::  {structure}     root
#   Output  ::  {string}        terminal message
def selfID(address, tree, root):
    print fullStamp() + " selfID()"
    Npanels = len(root[0])
    print fullStamp() + " Found " + str(Npanels) + " instrument panels"
    for i in range(0,Npanels):
        mac_bt = root[0][i][0].get("mac_bt")
        mac_eth = root[0][i][0].get("mac_eth")
        mac_wlan = root[0][i][0].get("mac_wlan")
        if address == mac_bt:
            print fullStamp() + " Match on BT MAC address"
            panelIndex = i
            panelNumber = i + 1
            return panelIndex, panelNumber
            break
        elif address == mac_eth:
            print fullStamp() + " Match on eth MAC address"
            panelIndex = i
            panelNumber = i + 1
            return panelIndex, panelNumber
            break
        elif address == mac_wlan:
            print fullStamp() + " Match on wlan MAC address"
            panelIndex = i
            panelNumber = i + 1
            return panelIndex, panelNumber
            break

# Find Scenario Index
#   The following function finds the configuration file index for the scenario number passed as an input
def findScenario(number, tree, root):
    print fullStamp() + " findScenario()"
    Nscenarios = len(root[1])
    print fullStamp() + " Found " + str(Nscenarios) + " scenarios"
    for i in range(0,Nscenarios):
        scenario_number = int(root[1][i].get("number"))
        if scenario_number == number:
            print fullStamp() + " Scenario " + str(number) + " found on index " + str(i)
            scenarioIndex = i
            scenarioNumber = number
            return scenarioIndex, scenarioNumber
            break
        elif i == Nscenarios - 1:
            print fullStamp() + " Scenario " + str(number) + " NOT found"
            scenarioIndex = -1
            scenarioNumber = number
            return scenarioIndex, scenarioNumber

# Pull Instrument Information (CSEC-Specific)
#   Automatically searches for the instrument information and stores data in several arrays
#   Input  :: tree, root --> from config. file
#   Output :: {arrays/lists} of each parameter associated with the device
def pullInstruments(tree, root):
    instrumentsTag = 4 # This program assumes the format of the configuration file will remain unchanged
    deviceName = []
    deviceBTAddress = []
    Ndevices = len(root[instrumentsTag]) 
    for i in range(0, Ndevices):
        deviceName.append(root[instrumentsTag][i][0].text)
        deviceBTAddress.append(root[instrumentsTag][i][1].text)
    return deviceName, deviceBTAddress
    
"""
References

1- XML eTree elementTree - https://docs.python.org/2/library/xml.etree.elementtree.html
"""
