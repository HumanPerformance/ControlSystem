"""
countdownProtocol.py

Countdown Protocol

The following python script displays a countdown clock on the screen of the control system that cues the trainee with the remaining evaluation time

Mohammad Odeh
Fluvio L Lobo Fenoglietto
01/23/2017
"""

import  sys
import  time
import  threading
import  StopWatchModule
from    Tkinter    import *
from    timeStamp  import *

global mode, root, sw

Narguments = len(sys.argv)
if Narguments > 5:
    print fullStamp() + " WARNING: User may have entered an incorrect number of arguments/inputs!"

functionName = str(sys.argv[0])
t0 = int(sys.argv[1])
t1 = int(sys.argv[2])
t2 = int(sys.argv[3])
direction = str(sys.argv[4])

print fullStamp() + " User executed " + str(sys.argv[0])
print fullStamp() + " t0 = " + str(t0)
print fullStamp() + " t1 = " + str(t1)
print fullStamp() + " t2 = " + str(t2)
print fullStamp() + " direction = " + direction

root = Tk()
root.configure(bg='black')
root.attributes('-fullscreen', True)
root.state = True
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)
sw = StopWatchModule.StopWatch(root)
sw.pack(side=TOP, expand=YES, fill=BOTH)

if direction is 'up':
    mode = 'stopWatch'
    sw.Start()

    x = threading.Timer(t0, phaseOne, args=(0,))
    x.start()

    y = threading.Timer(t0+t1, phaseTwo, args=(0,))
    y.start()   

    z = threading.Timer(t0+t1+t2, phaseThree)
    z.start()

elif direction is 'down':
    mode = 'countDown'
    sw.countDown(t0)
    
    x = threading.Timer(t0, phaseOne, args=(t1,))
    x.start()
    
    y = threading.Timer(t0+t1, phaseTwo, args=(t2,))
    y.start()   

    z = threading.Timer(t0+t1+t2, phaseThree)
    z.start()

root.mainloop()
