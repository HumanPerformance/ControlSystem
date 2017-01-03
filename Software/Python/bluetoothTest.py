"""
testing algorithm for bluetooth commands and/or functions
"""

import serial
import time
import bluetooth
from bluetoothProtocol import *
from smarthandleProtocol import *


bt_address = "00:06:66:80:8C:BE"
#rfObject = createPortS("SH",bt_address,115200,5)
portRelease("rfcomm",0)
portBind("rfcomm",0,bt_address)
rfObject = serial.Serial("/dev/rfcomm0",115200,timeout=None)

# triggering device
time.sleep(1)
triggerDevice2(rfObject,"SH")

# openning device
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()

# printing data
startTime = time.time()
currentTime = 0
stopTime = 20
data = []
while currentTime < stopTime:
    data.append(["TIM,"+str(currentTime), rfObject.readline()[:-1]])
    currentTime = time.time() - startTime
    #print currentTime
    

# print data

# stopping device
time.sleep(0.25)
rfObject.close()
time.sleep(0.25)
stopDevice2(rfObject,"SH")
