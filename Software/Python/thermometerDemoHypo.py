
# Import
from    configurationProtocol   import *
from    bluetoothProtocol       import *
from    thermometerProtocol     import *


deviceName = "DemoThermometer"
deviceBTAddress = ["00:06:66:8C:D3:2F", "00:06:66:8C:D2:65"]
BaudRate = 115200
timeout = 5
attempts = 3

# create rfObjects/ports
rfObject = createPort( deviceName, deviceBTAddress[0], BaudRate, timeout, attempts )
print( rfObject.isOpen() )
print( type(rfObject) )

# Open port and add delay for stability
rfObject.open()

print( rfObject.isOpen() )
# Start simulation (fever) then close port
startSIM_001( rfObject, timeout, attempts )
rfObject.close()

# Release port to avoid permanent connection
portRelease('rfcomm', 0)                                    
