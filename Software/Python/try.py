import sys
import platform
import os
import serial.tools.list_ports
from bluetoothProtocolWin import nextAvailableBTPort

#platform = sys.platform
osname = os.name
os = platform.system()


availableBTPort = nextAvailableBTPort()
