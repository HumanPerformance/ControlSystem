"""
configurationTest.py
"""

from os.path import expanduser
from configurationProtocol import *

homeDir = expanduser("~")
#print homeDir

pythonDir, configDir, configFile, dataDir, outputDir = definePaths()

tree, root = readConfigFile(configFile)


address = getMAC("eth0")

panelIndex, panelNumber = selfID(address, tree, root)

# Find Scenario Index
number = 1
scenarioIndex, scenarioNumber = findScenario(number, tree, root)
