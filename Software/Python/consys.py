"""
consys.py

Control System --Python

The following program has been designed to control the following processes:
1.0 - Read and follow instruction from server
    1.1 - Instructions are passed as terminal inputs
        Note: The program currently handles one (1) input - scalable
2.0 - Load configuration file based on server instructions or input
    Note: Configuration file currently located locally - can be switched to the server
    2.1 - Define path of configuration file based on user input
    2.2 - Load configuration file
    2.3 - Save loaded data into program variables
3.0 - Write loaded variables into downstream configuration file for parallel applications
    Note: Dowstream parallel applications currently include:
            - countdown.pde (Processing)
    3.1 - Define path of configuration file
    3.2 - Write configuration file
4.0 - Execution of downstream parallel applications
    Note: Dowstream parallel applications currently include:
            - countdown.pde (Processing)
            
Fluvio L. Lobo Fenoglietto 05/19/2016
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
import sys
import os
from os.path import expanduser
from doubleDigitCorrection import doubleDigitCorrection

# ==============================================
# Variables
# ==============================================
homeDir = expanduser("~")
consysPyDir = homeDir + "/csec/repos/ControlSystem/Software/Python"
consysPyDataDir = consysPyDir + "/data"
countdownDir = homeDir + "/csec/repos/ControlSystem/Software/Processing/countdown/build/armvh6f"
countdownDataDir = countdownDir + "/data"

# ==============================================
# Operation
# ==============================================

# 1.0 - Read and follow instructions from server
inputArg = sys.argv
selectedScenario = int(sys.argv[1])
outString = "User Executed " + inputArg[0] + ", scenario #" + inputArg[1]
print outString

# 2.0 - Load configuration file based on server instruction
## 2.1 - Define path of configuration file based on user input
scenarioConfigFilePath = consysPyDataDir + "/scenarios"
scenarioNumberString = doubleDigitCorrection(inputArg[1])
scenarioConfigFileName = "/sc" + scenarioNumberString + ".txt"
# print scenarioConfigFileName
## 2.2 - Load configuration file
scenarioConfigFile = scenarioConfigFilePath + scenarioConfigFileName
with open(scenarioConfigFile,'r+') as scenarioConfigFileObj:
    lines = scenarioConfigFileObj.readlines()
## 2.3 - Save loaded data into program variables
Nlines = len(lines)
print Nlines
scenarioConfigVariables = []
scenarioConfigValues = []
for i in range(0, Nlines-1):
    scenarioConfigVariables.append(lines[i].split(":")[0])
    scenarioConfigValues.append(lines[i].split(":")[1])
print scenarioConfigVariables
print int(scenarioConfigValues[1])

# 3.0 - Write loaded variables into downstream configuration file for parallel applications
## 3.1 - Define path of configuration file
countdownConfigFilePath = countdownDataDir
countdownConfigFileName = "/countdownInit.txt"
countdownConfigFile = countdownConfigFilePath + countdownConfigFileName
## 3.2 - Write configuration file
with open(countdownConfigFile, 'r+') as countdownConfigFileObj:
    # Note: For the countdown application, only two inputs are currently needed: StartTime and WarningTime
    countdownConfigFileObj.write(scenarioConfigVariables[1] + ":" + str(scenarioConfigValues[1]))
    countdownConfigFileObj.write(scenarioConfigVariables[2] + ":" + str(scenarioConfigValues[2]))

# 4.0 - Execution of downstream parallel applications
## 4.1 - Define path to program executeable
countdownExeFilePath = countdownDir
countdownExeFileName = "/countdown"
## 4.2 - Execute application
terminalCommand = "sh " + countdownExeFilePath + countdownExeFileName
os.system(terminalCommand)


"""
References
1- Defining Functions in Python - http://www.tutorialspoint.com/python/python_functions.htm
2- Calling Functions from other Python scripts - http://stackoverflow.com/questions/20309456/how-to-call-a-function-from-another-file-in-python
3- "       "         "    "     "      "       - http://stackoverflow.com/questions/7701646/how-to-call-a-function-from-another-file 
"""
