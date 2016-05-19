"""
programStatus.py

This script has been designed to check for the execution status of a given application/program

Fluvio L. Lobo Fenoglietto 05/19/2016

"""

# Import Libraries and/or Modules
import commands

# Operation
outStatus = commands.getoutput('ps -A')
print outStatus

if 'countdown' in outStatus:
    print "IT'S ALIVE!!"


"""
References:

1- http://ubuntuforums.org/showthread.php?t=1101746

"""
