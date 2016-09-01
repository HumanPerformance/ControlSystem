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
    
