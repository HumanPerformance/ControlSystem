# Import modules
from    configurationProtocol   import *
from    bluetoothProtocol       import *
from    thermometerProtocol     import *

deviceName = "DemoThermometer"
deviceBTAddress = ["00:06:66:8C:D3:2F", "00:06:66:8C:D2:65"]
BaudRate = 115200
timeout = 5
attempts = 3
simDuration = 20

# create rfObjects/ports and add delay for stability
rfObject = createPort( deviceName, deviceBTAddress[0], BaudRate, timeout, attempts )
time.sleep(0.25)

# Open port 
rfObject.open()

# Start simulation (fever) then close port
startSIM_000( rfObject)
rfObject.close()

# sleep for the duration of the simulation
time.sleep(simDuration)

# Open port, return to normal operation, then close port
rfObject.open()
normalOP(rfObject)
rfObject.close()

# Release port to avoid permanent connection
portRelease('rfcomm', 0)                                    
