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
"""
References

1- XML eTree elementTree - https://docs.python.org/2/library/xml.etree.elementtree.html
"""
