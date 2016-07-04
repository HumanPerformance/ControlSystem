"""
instrumentDataAcquisition.py

The following script/library/module will contain all routines/scripts/functions used to read and write data coming through the connected instruments

Fluvio L. Lobo Fenoglietto 07/04/2016
"""

def dataRead(arduSerialObj):
    inString = arduSerialObj.readline()
    print inString

    return inString
    
def dataWrite(i, inString):
    dataFileName = "data" + str(i) + ".txt"
    with open(dataFileName, "a") as dataFile:
        dataFile.write(inString)
        
