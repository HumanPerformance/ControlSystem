"""
panelDiagnosticTest

Panel Diagnostic Test

Similarly to other test scripts, the following algorithm uses the functions from the diagnostic protocol module to check the status of the intrument panel and its associated devices/modules

Fluvio L. Lobo Fenoglietto
01/11/2017
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
# Python modules
import  sys
import  os
import  serial
import  time
from    os.path                import expanduser

# PD3D Modules
from    timeStamp              import fullStamp
from    configurationProtocol  import *
from    bluetoothProtocol      import *
from    usbProtocol            import *
from    smarthandleProtocol    import *
from    smartHolderProtocol    import *


# ==============================================
# Operation
# ==============================================

# ----------------------------------------------
# Panel self-dentification
#   The panel obtains the mac address of the local system
# ----------------------------------------------
mac_eth = getMAC('eth0')

# ----------------------------------------------
# Timers
# ----------------------------------------------
executionTimeStamp = fullStamp()

# ----------------------------------------------
# Path/Directory Variables
# ----------------------------------------------
pythonDir, configDir, configFile, dataDir, outputDir = definePaths()

# ----------------------------------------------
# Upload Configuration XML
# ----------------------------------------------
tree, root = readConfigFile(configFile)

# ----------------------------------------------
# Define Panel
#   Using the MAC address from the local system and the configuration XML, the program identifies the SIP id and index
# ----------------------------------------------
panelIndex, panelID = selfID(mac_eth, tree, root)

# ----------------------------------------------
# Pull and Cross-Reference Devices
#   This function pulls the devices to be used in the selected scenario from the configuration XML
#   Then uses that list to croo-reference the addresses of the devices associated with the selected instrument panel
#   Returns the list of device names and addresses for execution
# ----------------------------------------------
panelDeviceTypes, panelDevices, panelDeviceAddresses = pullPanelInstruments(panelIndex, tree, root)

# ----------------------------------------------
# Verify each instrument associated to the panel
# ----------------------------------------------

print fullStamp() + " Verifying " + panelDevices[0]
print fullStamp() + " " + panelDevices[0] + " has been verified..."

print fullStamp() + " Verifying " + panelDevices[1]
print fullStamp() + " " + panelDevices[1] + " CANNOT be verified at the moment..."

print fullStamp() + " Verifying " + panelDevices[2]
time.sleep(1)
sh0 = createPortS(panelDeviceTypes[2],0,panelDeviceAddresses[2],115200,5)

print fullStamp() + " Verifying " + panelDevices[3]
time.sleep(1)
sh1 = createPortS(panelDeviceTypes[3],1,panelDeviceAddresses[3],115200,5)

print fullStamp() + " Verifying " + panelDevices[4]
print fullStamp() + " " + panelDevices[4] + " CANNOT be verified at the moment..."
#time.sleep(1)
#hld = createUSBPort(panelDeviceTypes[4],0, 250000, None)
