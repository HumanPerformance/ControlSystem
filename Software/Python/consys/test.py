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
homeDir, pythonDir, consDir = definePaths(cons)
response = addPaths(pythonDir)

from    timeStamp                   import fullStamp

# ------------------ operation
print( fullStamp() )
address = getMAC("eth0")
