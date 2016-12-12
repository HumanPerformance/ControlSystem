"""
configurationTest.py
"""

from os.path import expanduser
from configurationProtocol import *

homeDir = expanduser("~")
print homeDir

pythonDir, configDir, dataDir, outpurDir = definePaths()

#tree, root = readConfigFile(configurationPath + configurationFile)
