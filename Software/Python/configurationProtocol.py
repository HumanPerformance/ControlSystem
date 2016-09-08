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
import xml.etree.ElementTree as etree


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
