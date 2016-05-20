"""
readFile.py

The following script has been designed to test the uploading and reading capabilities within python

Fluvio L. Lobo Fenoglietto 05/20/2016
"""

# Variables
filePath = "/home/pi/csec/repos/ControlSystem/Software/Python/data/scenarios/"
fileName = "sc001.txt"

filePathString = filePath + fileName
## print filePathString

# Objects and/or Structures
fileObj = open(filePathString,'r+')

# Operation
for line in fileObj:
    print line

