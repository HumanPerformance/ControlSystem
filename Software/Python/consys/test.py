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

panel_id_file_path = dataDir + "/panels.txt"
panel_id_list, panel_address_list, panel_id, panel_address = panelSelfID(panel_id_file_path, device_address)

devices_id_file_path = dataDir + "/panel" + str( panel_id ) + "devices.txt"
device_id_list, device_name_list, device_bt_address_list = panelDeviceID(devices_id_file_path, panel_id)
