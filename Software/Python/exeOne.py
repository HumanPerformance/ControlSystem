"""
Execution One

This program is executed by a subprocess tool to test parallel operations

Fluvio L Lobo Fenoglietto
01/22/2017
"""

import time

start_time = time.time()
stop_time = 20
current_time = 0

while current_time < stop_time:
    current_time = time.time() - start_time
    print "exeOne time = " + str(current_time)
