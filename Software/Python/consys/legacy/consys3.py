"""
consys2.py

Control System 2

The following script has been design to coordinate the device triggering, time-monitoring, and data collection of the instrument panels.
The script executes the foloowing sequence:

1 - Panel identification
2 - Scenario identification
3 - Pull instruments
4 - Pull parameters
            
Fluvio L. Lobo Fenoglietto 12/19/2016
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
# Python modules
import  sys
import  time
from    threading               import Thread
from    Queue                   import Queue
from    os.path                 import expanduser
from    os                      import getcwd, path, makedirs

# PD3D Modules
from    timeStamp              import fullStamp
from    sequentialPrompt       import timerApp
from    configurationProtocol  import *
from    bluetoothProtocol      import *
from    usbProtocol            import *
from    smarthandleProtocol    import *
from    smartHolderProtocol    import * 

import bluetooth

try:
    print fullStamp() + " Start Configuration"

    ### def createBTPort():
    ##bt_addr = "00:06:66:83:89:F6"
    ##port = 1
    ##deviceName = "SH"
    ##
    ##sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    ##sock.connect( (bt_addr, port) )
    ##
    ### def triggerBTDevice():
    ##inString = deviceName
    ##while inString == deviceName:
    ##    print fullStamp() + " Triggering Device"
    ##    sock.send('g')
    ##    time.sleep(1)
    ##    inString = sock.recv(11)
    ##    print inString
    ##    print("Success")
    ##    sock.send('s')
    ##    sock.close()
    ##    print('closed')
    ##    quit()

    # Creating Serial Port for Devices
    time.sleep(1)
    bt_addr = "00:06:66:83:89:F6"
    port = 1
    deviceName = "SH"
    print fullStamp() + " Creating port for SH0"
    sh0 = createBTPortS( bt_addr, port, deviceName )

    # Triggering Smart Handle Devices
    time.sleep(1)
    print fullStamp() + " Triggering SH0"
    triggerDevice2(sh0,"SH")

    # ----------------------------------------------
    # Simulation / Configuration Loop
    #   In this loop, connected devices will be accessed for data collection
    # ----------------------------------------------

    time.sleep(5)

    global dataStream
    def fetchData(simDuration, dataQueue):
        inData, inChar = 'null', 'null'
        simCurrentTime = 0
        simStopTime = simDuration
        dataStream = []
        firstReading = True
        breakPoint = ''
        print fullStamp() + " Starting Simulation Loop, time = %.03f seconds" %simStopTime

        try:
            # Get rid of any chopped/truncated data prior to saving to buffer
            while inData != ('\n' or '\r' or '\0'):
                inData = sh0.recv(1)

            simStartTime = time.time()
            while simCurrentTime < simStopTime:
                # Read and save into buffer until hitting a newline\EOL\carriage return
                while inChar != ('\n' or '\r' or '\0'):
                    if firstReading:
                        buff = sh0.recv(1)
                        firstReading = False
                    else:
                        inChar = sh0.recv(1)
                        buff += inChar

                # Write buffer into stream
                firstReading = True
                inChar = 'null'
                #print(simCurrentTime)
                dataStream.append(["%.02f" %simCurrentTime,
                                       buff.strip('\n')])
                
                simCurrentTime = time.time() - simStartTime
                print fullStamp() + " Current Simulation Time = %.03f" %simCurrentTime

                # End of Simulation Loop
                
        except Exception as instance:
            print fullStamp() + " Exception or Error Caught"
            print fullStamp() + " Error Type " + str(type(instance))
            print fullStamp() + " Error Arguments " + str(instance.args)
            print fullStamp() + " Closing Open Ports"

        dataQueue.put(dataStream)

    timer1 = 5
    timer2 = 10
    timer3 = 5
    simStopTime = (timer1 + timer2 + timer3)

    sh0.send('g')
    dataQueue = Queue()
    datafetchProcess = Thread( target=fetchData, args=(simStopTime,dataQueue,) )
    datafetchProcess.start()

    dataStream = dataQueue.get()

    print fullStamp() + " Processes concluded, closing ports..."

    time.sleep(0.25)
    stopDevice2(sh0,"SH")
    sh0.close()

    print fullStamp() + " Printing data..."

    Nstream = len(dataStream)
    print Nstream

    # ************************************************* #
    #               DATA STORAGE: START                 #
    # ************************************************* #

    Nlines = len(dataStream)
    
    # Create data output folder/file
    dataFileDir = getcwd() + "/dataOutput/" + fullStamp()
    dataFileName = dataFileDir + "/output.txt"
    if(path.exists(dataFileDir)) == False:
        makedirs(dataFileDir)
    
    # Write basic information to the header of the data output file
    for j in range(0,Nlines):
        with open(dataFileName, "a") as dataFile:
            dataFile.write(dataStream[j][0] + ',' + dataStream[j][1] + '\n')
        
    # ************************************************* #
    #               DATA STORAGE: END                   #
    # ************************************************* #

except Exception as instance:
    sh0.close()
    print fullStamp() + " Exception or Error Caught"
    print fullStamp() + " Error Type " + str(type(instance))
    print fullStamp() + " Error Arguments " + str(instance.args)
    print fullStamp() + " Closing Open Ports"
    
