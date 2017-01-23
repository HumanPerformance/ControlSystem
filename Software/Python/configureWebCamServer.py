"""
configureWebCamServer.py

Configure Web Camera Server

This function automatically configures the web cam server on a raspberry pi

Fluvio L Lobo Fenoglietto
01/13/2017
"""

import subprocess

cmd = ["sudo apt-get update"]
output = subprocess.Popen(cmd[0],stdout=subprocess.PIPE)
while output.poll() == None:
    pass
print output

