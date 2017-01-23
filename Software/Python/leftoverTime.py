"""
leftoverTimer
"""

import time

startTime = time.time()
currentTime = 0
stopTime = 15

print "hola"
time.sleep(3)
print "chao"
time.sleep(3)

currentTime = time.time() - startTime
print "Now waiting " + str(stopTime - currentTime)
time.sleep(stopTime - currentTime)
