"""
Parallel Execution

Script designed to explore the parallel execution of different processes using python

Fluvio L Lobo Fenoglietto
01/22/2017
"""


import subprocess
import time

p = subprocess.Popen(['python', 'exeOne.py'])


start_time = time.time()
stop_time = 20
current_time = 0

while current_time < stop_time:
    current_time = time.time() - start_time
    print "exeTwo time = " + str(current_time)
