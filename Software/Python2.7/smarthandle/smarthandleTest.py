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

#import  smarthandleDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *

# Operation

deviceBTAddress = "00:06:66:83:89:5F"
portNumber = 1

rfObject = createBTPort(deviceBTAddress, portNumber)

data = []
for i in range(0,100):
    time.sleep(0.10)
    data.append( rfObject.recv(128) )

rfObject.close()
