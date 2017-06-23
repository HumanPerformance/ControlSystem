# Import modules
import  time
from    timeStamp                        import fullStamp
from    bluetoothProtocol_teensy32       import *
from    pulseOximeterProtocol            import *


print fullStamp() + " Connecting to Pulse Oximeter"
deviceName = "DemoPulseOximeter"
deviceBTAddress = "00:06:66:8C:D2:1F"
portNumber = 0
baudRate = 115200
attempts = 3
simDuration = 20

rfObject = createPort( deviceName, portNumber, deviceBTAddress, baudRate, attempts )


print fullStamp() + " Triggering TACHYCARDIA"
time.sleep(1)
tachySim(rfObject, attempts)

print fullStamp() + " Hold Simulation for 20 seconds"
time.sleep(20)

print fullStamp() + " Trigger NORMAL OPERATION"
time.sleep(1)
normalOP(rfObject, attempts)

print fullStamp() + " Releasing Serial Port"
portRelease('rfcomm', 0) 
