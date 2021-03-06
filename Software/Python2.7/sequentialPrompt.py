'''
A proof of concept timer app built to communicate information with the the control
system at specific time intervals.

Author: Mohammad Odeh
Date: Dec. 20th 2016

# To run, call timerApp(t0,t1,t2,direction) with the input parameters needed where
# t is time in seconds
# direction is up/down for stopwatch/countdown
'''
from    threading           import Timer
from    Tkinter             import *
from    timeStamp           import *
import  time
import  StopWatchModule

def phaseOne(t1):
    #print fullStamp() + " Phase 1 Passed"
    if mode is 'countDown':
        sw.Reset(t1)
        sw.countDown(t1)
    elif mode is 'stopWatch':
        sw.Reset(0)

    return

def phaseTwo(t2):
    #print fullStamp() + " Phase 2 Passed"
    if mode is 'countDown':
        sw.Reset(t2)
        sw.countDown(t2)
    elif mode is 'stopWatch':
        sw.Reset(0)

    return

def phaseThree():
    #print fullStamp() + " Phase 3 Passed"
    if mode is 'countDown':
        pass
    elif mode is 'stopWatch':
        pass
    
    sw.Reset(0)
    sw.Stop()
    root.after(2000, lambda:root.destroy())
    return

def toggle_fullscreen(self, event=None):
    root.state = not root.state  #Boolean toggle
    root.attributes("-fullscreen", root.state)
    return "break"

def end_fullscreen(self, event=None):
    root.state = False
    root.attributes("-fullscreen", False)
    return "break"

def timerApp(t0,t1,t2,direction):
    #timerApp(1,1,1,"down")

    global mode, root, sw
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

        x = Timer(t0, phaseOne, args=(0,))
        x.start()

        y = Timer(t0+t1, phaseTwo, args=(0,))
        y.start()   

        z = Timer(t0+t1+t2, phaseThree)
        z.start()
    
    elif direction is 'down':
        mode = 'countDown'
        sw.countDown(t0)
        
        x = Timer(t0, phaseOne, args=(t1,))
        x.start()
        
        y = Timer(t0+t1, phaseTwo, args=(t2,))
        y.start()   

        z = Timer(t0+t1+t2, phaseThree)
        z.start()

    root.mainloop()
