"""
testing algorithm for bluetooth commands and/or functions
"""

from bluetoothProtocol import findDevices
from bluetoothProtocol import findSmartDevices

availableDeviceNames, availableDeviceBTAddresses = findDevices()
smartDeviceNames, smartDeviceBTAddresses = findSmartDevices("RNBT",availableDeviceNames, availableDeviceBTAddresses)
