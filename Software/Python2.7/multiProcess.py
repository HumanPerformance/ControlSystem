"""
multiProcess.py

Multi-Process

Fluvio L Lobo Fenoglietto
01/24/2017
"""

"""
from multiprocessing import Process, Queue

def f(x,q):
    x = x + 1
    q.put([42, x, "hello"])

q = Queue()
p = Process(target=f, args=(0,q,))
p.start()

p.join()
print q.get()
"""


import time
from multiprocessing import Process
from multiprocessing import Queue

def _function_1(x_1,q_1):
    start_time = time.time()
    current_time = 0
    stop_time = 10
    while current_time < stop_time:
        x_1 = x_1 + 1
        current_time = time.time() - start_time
        print "_function_1 " + str(current_time)
    q_1.put([x_1,"hello"])


def _function_2(x_2,q_2):
    start_time = time.time()
    current_time = 0
    stop_time = 10
    while current_time < stop_time:
        x_2 = x_2 + 1
        current_time = time.time() - start_time
        print "_function_2 " + str(current_time)
    q_2.put([x_2,"ciao"])


q_1 = Queue()
_process_1 = Process(target=_function_1, args=(0,q_1,))
_process_1.start()

q_2 = Queue()
_process_2 = Process(target=_function_2, args=(10,q_2,))
_process_2.start()

print q_1.get()
print q_2.get()

