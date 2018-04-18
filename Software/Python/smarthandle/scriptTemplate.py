"""
---

"""

# Import
import  sys
import  os
import  serial
import  time

from    configurationProtocol    import *
device = "smarthandle"
homeDir, pythonDir, deviceDir = definePaths(device)
response = addPaths(pythonDir)

import  smarthandleDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *

# Operation

