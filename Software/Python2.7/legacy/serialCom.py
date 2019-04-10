
#
# arduinoTalk
#
# The following python script was designed to demo the communication between the Raspberry Pi and an Arduino module in a master-slave configuration
#
# Fluvio L. Lobo Fenoglietto 05/06/2016


#
# Requirements:
# a) The 'nanpy-firmaware' must have been installed on the Arduino board to be used as a slave


import sys
import glob
import serial

def serialPorts():
    """ List of serial port names

        :returns:
            The list of serial ports available on the system
            
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.starts
