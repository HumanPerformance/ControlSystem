# ========================================================================================= #
# Import Libraries and/or Modules
# ========================================================================================= #
# Python modules
import  sys
import  os
import  serial
import  time
from    os.path                     import expanduser
from    os                          import getcwd, path, makedirs

# PD3D modules
from    configurationProtocol       import *
cons    = "consys"
homeDir, pythonDir, consDir, ouputDir, dataDir = definePaths(cons)
response = addPaths(pythonDir)

from    timeStamp                   import fullStamp

# ------------------ operation
print( fullStamp() )
device_address = getMAC("eth0")

id_file_path = dataDir + "/panels.txt"
panel_id_list, panel_address_list, panel_id, panel_address = selfID(id_file_path, device_address)
