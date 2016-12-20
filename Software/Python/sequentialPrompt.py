'''
A proof of concept timer app built to communicate information with the the control
system at specific time intervals.

Author: Mohammad Odeh
Date: Dec. 20th 2016

# To run, call timerApp(t0,t1,t2,direction) with the input parameters needed where
# t is time in seconds
# direction is up/down for stopwatch/countdown
'''
from Tkinter import *
import time
import threading
import StopWatchModule

def phaseOne():
    print "Phase 1 Passed"
    sw.Reset()
    pass

def phaseTwo():
    print "Phase 2 Passed"
    sw.Reset()
    pass

def phaseThree():
    print "Phase 3 Passed"
    sw.Reset()
    sw.Stop()
    pass

def phaseOneALT(t1):
    print "Phase 1 Passed"
    sw.ResetDown(t1)
    sw.countDown(t1)
    pass

def phaseTwoALT(t2):
    print "Phase 2 Passed"
    sw.ResetDown(t2)
    sw.countDown(t2)
    pass

def phaseThreeALT():
    print "Phase 3 Passed"
    sw.ResetDown(0)
    sw.Stop()
    pass

def toggle_fullscreen(self, event=None):
    root.state = not root.state  # Just toggling the boolean
    root.attributes("-fullscreen", root.state)
    return "break"

def end_fullscreen(self, event=None):
    root.state = False
    root.attributes("-fullscreen", False)
    return "break"

def timerApp(t0,t1,t2,direction):
    #timerApp(2,5,2,"down")

    if direction == "up":
        sw.Start()

        x = threading.Timer(t0, phaseOne)
        x.start()

        y = threading.Timer(t0+t1, phaseTwo)
        y.start()   

        z = threading.Timer(t0+t1+t2, phaseThree)
        z.start()
    
    elif direction == "down":
        sw.countDown(t0)
        
        x = threading.Timer(t0, phaseOneALT, args=(t1,))
        x.start()
        
        y = threading.Timer(t0+t1, phaseTwoALT, args=(t2,))
        y.start()   

        z = threading.Timer(t0+t1+t2, phaseThreeALT)
        z.start()
        

    root.mainloop()

root = Tk()
root.configure(bg='black')
root.attributes('-fullscreen', True)
root.frame = Frame(root)
root.frame.pack()
root.state = False
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)
sw = StopWatchModule.StopWatch(root)
sw.pack(side=TOP)
