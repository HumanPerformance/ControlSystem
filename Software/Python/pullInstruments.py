"""
pullInstruments.py

Fluvio L. Lobo Fenoglietto 06/29/2016
"""

def pullInstruments(instrumentsConfigFile):
    # Creating Bluetooth Serial Objects
    ## Identifying Objects from Instruments List
    with open(instrumentsConfigFile,'r+') as instrumentsConfigFileObj:
        lines = instrumentsConfigFileObj.readlines()
        #print lines
    Nlines = len(lines)
    instrumentNames = []
    instrumentBTAddress = []
    for i in range(0, Nlines):
        if lines[i][0] != "#": # This comparison allows for the code to skip the comments within the configuration file
            if lines[i][:10] == "Instrument":
                instrumentNames.append(lines[i].split(";")[1][:-1])
            elif lines[i][:16] == "BluetoothAddress":
                instrumentBTAddress.append(lines[i].split(";")[1][:-1])
    #print instrumentNames
    #print instrumentBTAddress
    
    return instrumentNames, instrumentBTAddress
