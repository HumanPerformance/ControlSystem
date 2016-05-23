"""
executingSubprocess.py

This script was designed to demo the python capability of calling/executing external commands and/or applications in seprate processes/terminals

Fluvio L. Lobo Fenoglietto 05/23/2016
"""
import subprocess
from subprocess import Popen
import commands


terminalCmd = 'sh /home/pi/csec/repos/ControlSystem/Software/Processing/countdown/build/armvh6f/countdown'
print terminalCmd

subprocess.Popen([terminalCmd])

#outStatus = commands.getoutput('ps -A')
#print outStatus

#if 'countdown' in outStatus:
#    print "IT'S ALIVE!!"


