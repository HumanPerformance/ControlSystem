"""
Stethoscope Configuration Protocol

The following module contains functions used to link resources to the main device scripts

Fluvio L Lobo Fenoglietto 11/15/2017
"""

# ================================================================================= #
# Import Libraries and/or Modules
# ================================================================================= #

from    os.path     import expanduser
import  sys
from    timeStamp   import fullStamp

# ================================================================================= #
# Define Paths
#
# Define and insert paths to directories with required documentation for the
# device scripts
#
# Fluvio L Lobo Fenoglietto 11/15/2017
# ================================================================================= #
def definePaths(device):
    baseDir = expanduser("~")                                                       # get main/root or base directory for the operating system in use
    rootDir = "/root"                                                                           # root directory for Linux - Raspbian
    if baseDir == rootDir:
        homeDir = "/home/pi"
        pythonDir = homeDir + "/pd3d/csec/repos/ControlSystem/Software/Python"
        deviceDir = pythonDir + "/" + device + "/"
    else:
        homeDir = "/home/pi"
        pythonDir = homeDir + "/pd3d/csec/repos/ControlSystem/Software/Python"
        deviceDir = pythonDir + "/" + device + "/"
    return homeDir, pythonDir, deviceDir

# ================================================================================= #
# Insert Paths
#
# Insert defined directory paths into the python directory
#
# Fluvio L Lobo Fenoglietto 11/15/2017
# ================================================================================= #
def addPaths(paths):
    if isinstance(paths, list):
        Npaths = len(paths)
        for i in range(0, Npaths):
            sys.path.insert(0, paths[i])
        response = True
    else:
        sys.path.insert(0, paths)
        response = False
    return response

# ================================================================================= #
# Get MAC address
#
# Function to retrieve MAC address
#
# Fluvio L Lobo Fenoglietto 05/25/2018
# ================================================================================= #
def getMAC(interface):
    print( fullStamp() + " getMAC()" )
    print( fullStamp() + " Searching MAC address for " + interface + " module" )
    try:
        address = open("/sys/class/net/" + interface + "/address").read()[:-1]
        print( fullStamp() + " MAC (" + interface + "): " + address )
        return address
    except:
        print( fullStamp() + " Failed to find address, check input interface" )
