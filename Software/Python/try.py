import sys
import platform
import os
import serial.tools.list_ports
from bluetoothProtocolWin import nextAvailablePort

#platform = sys.platform
osname = os.name
os = platform.system()


portName = nextAvailablePort()
print portName
