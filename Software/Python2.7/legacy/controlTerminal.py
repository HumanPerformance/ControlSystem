"""
controlTerminal.py

This script has been designed to test coomunication/control of the OS' terminal/command-prompt

Fluvio L. Lobo Fenoglietto 05/19/2016
"""


# Import Libraries and/or Modules
import os

# Variables
echo = 'echo' # the echo prefix is used on every command sent to the terminal
cmd = 'sudo /home/pi/csec/repos/ControlSystem/Software/Processing/countdown/application.linux-armv6hf/countdown'
terminalString = cmd
print terminalString

# Terminal Control
os.system(terminalString)

