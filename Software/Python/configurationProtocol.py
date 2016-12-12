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
        dataDir = pythonDir + "/data"                                                           # Data directory
        outputDir = dataDir + "/output"                                                         # Output directory
    else:
        print fullStamp() + " User executed function on an OS that is not supported..."
        pythonDir = 0
        configDir = 0
        dataDir = 0
        outputDir = 0
    return pythonDir, configDir, dataDir, outputDir

# Read Configuration (.XML) File
#   Reads or imports information from configuration file into an object or structure
#   Input  :: path to configuration file (string)
#   Output :: configuration file structure
def readConfigFile(configFile):
    tree = etree.parse(configFile)
    root = tree.getroot()
    return tree, root

# Search Given Child (Group within tree)
#   Searches for a specific "child" or section within the configuration file
#   Input  :: {string} name of "child" or section

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
