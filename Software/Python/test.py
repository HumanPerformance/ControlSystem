from smarthandleProtocol import *
import time


bt_addr = "00:06:66:83:89:F6"
port = 1
deviceName = "SH"
socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
socket.connect( (bt_addr, port) )
##triggerDevice2(socket,deviceName)

##data=''
##now = time.time()
##later = 15
##nono = 0
##print('starting')
##while nono < 20:
##    data += socket.recv(115200)
##    nono = time.time() - now
##
##print(len(data))

##stopDevice2(socket,deviceName)
##socket.close()
