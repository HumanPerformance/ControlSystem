import bluetooth
from bluetoothProtocol_teensy32 import *

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

addr0 = "00:06:66:8C:9C:2E"
for addr, name in nearby_devices:
    if addr == addr0:
        print("YES")
        addr1 = addr
    print("  %s - %s" % (addr, name))

createBTPort(addr1,0)
