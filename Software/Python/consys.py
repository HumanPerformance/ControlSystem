"""
consys.py

Control System --Python

The following program has been designed to control the following processes:
1.0 - Read and follow instruction from server
    1.1 - Instructions are passed as terminal inputs
        Note: The program currently handles one (1) input - scalable
2.0 - Load configuration file based on server instructions or input
    Note: Configuration file currently located locally - can be switched to the server
    
Fluvio L. Lobo Fenoglietto 05/19/2016
"""

# Import Libraries and/or Modules
import sys
from printMyString import printMyString

# ==============================================
# Operation
# ==============================================

# 1.0 - Read and follow instructions from server
inputArg = sys.argv
selectedScenario = int(sys.argv[1])
outString = "User Executed " + inputArg[0] + ", scenario #" + inputArg[1]
print outString

# 2.0 - Load configuration file based on server instruction
printMyString("hola")


"""
References
1- Defining Functions in Python - http://www.tutorialspoint.com/python/python_functions.htm
2- Calling Functions from other Python scripts - http://stackoverflow.com/questions/20309456/how-to-call-a-function-from-another-file-in-python
3- "       "         "    "     "      "       - http://stackoverflow.com/questions/7701646/how-to-call-a-function-from-another-file
"""
