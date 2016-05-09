#
# timePlay.py
#
# This script was designed test the python time module
#
# Fluvio L. Lobo Fenoglietto 05/07/2016


import time


t0 = time.time()
print t0

# time.sleep(0.5)

t1 = time.time() - t0
print t1

time.sleep(2)

t2 = time.time() - t0
print t2
