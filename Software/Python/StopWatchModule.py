'''
A stopwatch module that has been adapted from:
http://code.activestate.com/recipes/124894-stopwatch-in-tkinter/

Modified by: Mohammad Odeh
Date: Dec. 20th 2016
'''

from Tkinter import *
import time

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._startTime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()      

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr, bg="black", 
                  fg="white", width=200, font=("Courier", 72), anchor='center')
        self._setTime(self._elapsedtime)
        l.pack(fill=BOTH, expand=YES, pady=2, padx=2)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        
        if self._countDownToggle is True:
            self._start1 = time.time()
            self._start2 = self._start1 - self._start0
            self._elapsedtime = self._startTime - self._start2   
            
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._countDownToggle = False
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self, startTime):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        if self._countDownToggle is True:
            self._start0 = time.time()
            self._start1 = time.time()
            self._startTime = startTime
            self._setTime(self._elapsedtime)

    def countDown(self, startTime):        
        if not self._running:
            self._countDownToggle = True
            self._startTime = startTime
            self._start0 = time.time()
            self._update()
            self._running = 1

'''     
def main():
    root = Tk()
    sw = StopWatch(root)
    sw.pack(side=TOP)
    
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)
    
    root.mainloop()


if __name__ == '__main__':
    main()
'''
