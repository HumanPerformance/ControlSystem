"""
instrumentDataAcquisition.py

The following script/library/module will contain all routines/scripts/functions used to read and write data coming through the connected instruments

Fluvio L. Lobo Fenoglietto 07/04/2016
"""

# Standard Modules/Libraries
import os
import os.path

# Custom Modules/Libraries
from timeStamp import *

def dataRead(arduSerialObj):
    inString = arduSerialObj.readline()
    print inString

    return inString
    
def dataWrite(outputFilePath, i, inString):
    dataFileDir = outputFilePath + stampedFolder()

    if os.path.exists(dataFileDir) == False:
        createDataFolder(dataFileDir)
    
    dataFileName = "/data" + str(i) + ".txt"
    dataFilePath = dataFileDir + dataFileName

    if os.path.isfile(dataFilePath) == False:
        createDataFile(dataFilePath)
    
    with open(dataFilePath, "a") as dataFile:
        dataFile.write(inString)

def createDataFile(dataFilePath):
    with open(dataFilePath, "a") as dataFile:
        dataFile.write("===================== \n")
        dataFile.write("This is a header line \n")
        dataFile.write("This is a header line \n")
        dataFile.write("This is a header line \n")
        dataFile.write("===================== \n")

def createDataFolder(dataFileDir):
    os.makedirs(dataFileDir)
    
"""
References
1 - Print String to File - http://stackoverflow.com/questions/5214578/python-print-string-to-text-file
2 - File Modes - https://docs.python.org/2/tutorial/inputoutput.html
3 - Check for file existence - http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
4 - Print on a new line - http://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-everytime
"""
