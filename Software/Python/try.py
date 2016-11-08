import sys
import platform
import os
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
print ports

#platform = sys.platform
osname = os.name
os = platform.system()
