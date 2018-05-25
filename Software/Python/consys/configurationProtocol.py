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
        homeDir     = "/home/pi"
        pythonDir   = homeDir + "/pd3d/csec/repos/ControlSystem/Software/Python"
        deviceDir   = pythonDir + "/" + device + "/"
        outputDir   = pythonDir + "/consys/output"
        dataDir     = pythonDir + "/consys/data"
    else:
        homeDir = "/home/pi"
        pythonDir = homeDir + "/pd3d/csec/repos/ControlSystem/Software/Python"
        deviceDir = pythonDir + "/" + device + "/"
        outputDir   = pythonDir + "/consys/output"
        dataDir     = pythonDir + "/consys/data"

    return homeDir, pythonDir, deviceDir, outputDir, dataDir

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

# ================================================================================= #
# Self Identification
#
# Function to self-identify the panel using a MAC address
#
# Fluvio L Lobo Fenoglietto 05/28/2018
# ================================================================================= #
def selfID(id_file_path, device_address):
    print( fullStamp() + " selfID()" )                                              # signals execution of the function

    dataFile = open( id_file_path, 'r' )                                            # opens data file with panel information
    line_num             = 0
    panel_id_list        = []                                                       # define array variable
    panel_address_list   = []
    for line in dataFile:                                                           # for each line in the file ...
        if len(line) <= 1:                                                          # if nothing in line ... pass
            pass
        elif line[0] == "#":                                                        # if line starts with number sign (= comment) ... pass
            pass
        else:                                                                       # in any other case ...
            trim_line = line[:-1]                                                   # trim line by ignoring "end of line" character
            split_line = trim_line.split(",")                                       # split line with comma delimiter (default)
            panel_id_list.append( split_line[0] )                                   # append the first element as the number id
            panel_address_list.append( split_line[1] )                              # append the second element as the MAC address
            if split_line[1] == device_address:                                     # compare each address to the input panel/device MAC address
                panel_id        = line_num                                          # if so ... store id number
                panel_address   = panel_address_list[line_num]                      # if so ... associate address too ...

            line_num = line_num + 1

    return panel_id_list, panel_address_list, panel_id, panel_address
    
