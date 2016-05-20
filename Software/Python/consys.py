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

# ==============================================
# Operation
# ==============================================

# 1.0 - Read and follow instructions from server
inputArg = sys.argv
outString = "User Executed " + inputArg[0]
print outString

# 2.0 - Load configuration file based on server instruction

