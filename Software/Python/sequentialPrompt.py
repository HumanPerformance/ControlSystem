'''
A proof of concept timer app built to communicate information with the the control
system at specific time intervals.

Author: Mohammad Odeh
Date: Dec. 20th 2016

# To run, call timerApp(t0,t1,t2,direction) with the input parameters needed where
# t is time in seconds
# direction is up/down for stopwatch/countdown
'''
from    Tkinter                import *
from    configurationProtocol  import *
from    bluetoothProtocol      import *
from    usbProtocol            import *
from    smarthandleProtocol    import *
from    smartHolderProtocol    import *
from    timeStamp              import fullStamp
import time
import threading
import StopWatchModule




def phaseOne(t1):
    print fullStamp() + " Entering Configuration Loop"
    if mode is 'countDown':
        sw.Reset(t1)
        sw.countDown(t1)
    elif mode is 'stopWatch':
        sw.Reset(0)

    return

# ----------------------------------------------
# Simulation / Configuration Loop
#   In this loop, connected devices will be accessed for data collection
# ----------------------------------------------

def fetchData(t1,t2):
    print fullStamp() + " Fetching Data"
    #time.sleep(5) # Adding this wait actually improved the number of values read?!?!? - use the first timer
    simStartTime = time.time()
    simCurrentTime = 0
    simStopTime = t1+10 # currently just using the initial timer
    # simLoopCounter = 0
    dataStream = []
    print fullStamp() + " Starting Simulation Loop, time = %.03f seconds" %simStopTime
    
    try:
        while simCurrentTime < simStopTime:
            
            # Handles
            '''
            dataStream.append(["%.02f" %simCurrentTime,
                               sh0.readline()[:-1],
                               sh1.readline()[:-1],
                               hld.readline()[:-1]])
            '''
            simCurrentTime = time.time() - simStartTime
            print fullStamp() + " Current Simulation Time = %.03f" %simCurrentTime
            # simLoopCounter = simLoopCounter + 1;

            # End of Simulation Loop
            
    except Exception as instance:
        print fullStamp() + " Exception or Error Caught"
        print fullStamp() + " Error Type " + str(type(instance))
        print fullStamp() + " Error Arguments " + str(instance.args)
        print fullStamp() + " Closing Open Ports"

        '''
        time.sleep(1)
        if sh0.isOpen() == True:
            sh0.close()

        time.sleep(1)
        if sh1.isOpen() == True:
            sh1.close()

        time.sleep(1)
        if hld.isOpen == True:
            hld.close()
        '''     

    if mode is 'countDown':
        sw.Reset(t2)
        sw.countDown(t2)
    elif mode is 'stopWatch':
        sw.Reset(0)

    return

def closePorts():
    print fullStamp() + " Terminating"
    '''
    time.sleep(0.25)
    if sh0.isOpen() == True:
        sh0.close()

    time.sleep(0.25)
    if sh1.isOpen() == True:
        sh1.close()

    time.sleep(0.25)
    if hld.isOpen == True:
        hld.close()
                              
    time.sleep(0.25)
    stopDevice2(sh0,deviceTypes[0])

    time.sleep(0.25)
    stopDevice2(sh1,deviceTypes[1])

    time.sleep(0.25)                                          
    stopDevice(hld,deviceTypes[2])
    '''    
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

def placeholder():
    pass

def timerApp(timer0,timer1,timer2,direction):
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
        
        x = threading.Timer(timer0, fetchData, args=(timer1,0,))
        x.start()

        y = threading.Timer(timer0+timer1, closePorts)
        y.start()   

        z = threading.Timer(timer0+timer1+timer2, placeholder)
        z.start()
        phaseOne(timer0)
    
    elif direction is 'down':
        mode = 'countDown'
        sw.countDown(timer0)
        
        x = threading.Timer(timer0, fetchData, args=(timer1,timer2,))
        x.start()
        
        y = threading.Timer(timer0+timer1, closePorts)
        y.start()   

        z = threading.Timer(timer0+timer1+timer2, placeholder)
        z.start()
        phaseOne(timer0)

    root.mainloop()
