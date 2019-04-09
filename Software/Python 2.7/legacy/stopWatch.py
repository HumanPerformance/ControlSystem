"""
stopWatch.py

This script has been designed to demo the time measurement capabilities of python

Fluvio L. Lobo Fenoglietto 05/23/2016
"""

import time

startTime = time.time()
currentTime = 0
stopTime = 60

while currentTime < stopTime:
        currentTime = time.time() - startTime
        print currentTime
        # time.sleep(1)
else:
        print "clock stopped"
