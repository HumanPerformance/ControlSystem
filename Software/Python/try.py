import sys
import platform
import os
import serial.tools.list_ports
from bluetoothProtocolWin import nextAvailableBTPort

#platform = sys.platform
osname = os.name
os = platform.system()


usedPorts = serial.tools.list_ports.comports()                                                          # ...
for i in range(0,len(usedPorts)):                                                                       # Loop through found ports...
    port, description, hwid = usedPorts[i]                                                              # Read port-name, description, and hwid from each found port...
    print hwid
