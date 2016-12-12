"""
configurationTest.py
"""

from os.path import expanduser
from configurationProtocol import *

homeDir = expanduser("~")
print homeDir

pythonDir, configDir, configFile, dataDir, outputDir = definePaths()

#tree, root = readConfigFile(configurationPath + configurationFile)
