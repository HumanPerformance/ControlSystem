"""
instrumentDataAcquisition.py

The following script/library/module will contain all routines/scripts/functions used to read and write data coming through the connected instruments

Fluvio L. Lobo Fenoglietto 07/04/2016
"""

# ===================================
# Import Libraries/Modules
# ===================================

# Standard Modules/Libraries
import os
import os.path
# Custom Modules/Libraries
from timeStamp import *

# ===================================
# Functions
# ===================================

# -----------------------------------
# dataRead()
#   Read data from serial port
# -----------------------------------
def dataRead(arduSerialObj):
    inString = arduSerialObj.readline()
    print inString

    return inString

# -----------------------------------
# dataWrite()
#   Write data, read from serial, to
#   an output/text file
# -----------------------------------
def dataWrite(executionTimeStamp, currentTime, outputFilePath, instrumentName, inString):
    dataFileDir = outputFilePath + "/" + executionTimeStamp

    if os.path.exists(dataFileDir) == False:
        createDataFolder(dataFileDir)
    
    dataFileName = "/" + instrumentName + ".txt"
    dataFilePath = dataFileDir + dataFileName

    if os.path.isfile(dataFilePath) == False:
        createDataFile(dataFilePath, instrumentName)
    
    with open(dataFilePath, "a") as dataFile:
        timePrefix = "TIM," + str(currentTime) + ","
        dataFile.write(timePrefix + inString)
        
# -----------------------------------
# createDataFile()
#   Creates the output/text file
# -----------------------------------
def createDataFile(dataFilePath, instrumentName):
    with open(dataFilePath, "a") as dataFile:
        dataFile.write("===================== \n")
        dataFile.write("Scenario =  \n")
        dataFile.write("Instrument = " + instrumentName + "\n")
        dataFile.write("This is a header line \n")
        dataFile.write("===================== \n")

# -----------------------------------
# createDataFolder()
#   Creates the output/text file's
#   directory/folder
# -----------------------------------
def createDataFolder(dataFileDir):
    os.makedirs(dataFileDir)
    
"""
References
1 - Print String to File - http://stackoverflow.com/questions/5214578/python-print-string-to-text-file
2 - File Modes - https://docs.python.org/2/tutorial/inputoutput.html
3 - Check for file existence - http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
4 - Print on a new line - http://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-everytime
5 - Check for Existance and Create Directory - http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
"""
