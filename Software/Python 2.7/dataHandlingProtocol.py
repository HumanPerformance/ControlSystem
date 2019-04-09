"""
Data Handling Protocol

The following python module has been designed to handle the data collected and streamed by connected devices

Fluvio L Lobo Fenoglietto
01/05/2017
"""

# Data Write
#   This function writes the data read from serial to an output file
def dataWrite(executionTimeStamp, currentTime, outputDir, instrumentName, inString):
    dataFileDir = outputDir + "/" + executionTimeStamp

    if os.path.exists(dataFileDir) == False:
        createDataFolder(dataFileDir)
    
    dataFileName = "/" + instrumentName + ".txt"
    dataFilePath = dataFileDir + dataFileName

    if os.path.isfile(dataFilePath) == False:
        createDataFile(dataFilePath, instrumentName)
    
    with open(dataFilePath, "a") as dataFile:
        #timePrefix = "TIM," + str(currentTime) + ","
        #dataFile.write(timePrefix + inString)
        dataFile.write(inString + "\n")

# Create Data File
#   Creates the output/text file
def createDataFile(dataFilePath, instrumentName):
    with open(dataFilePath, "a") as dataFile:
        dataFile.write("===================== \n")
        dataFile.write("Scenario =  \n")
        dataFile.write("Instrument = " + instrumentName + "\n")
        dataFile.write("This is a header line \n")
        dataFile.write("===================== \n")

# Create Data Folder
#   Creates the output/text file's directory/folder
def createDataFolder(dataFileDir):
    os.makedirs(dataFileDir)

