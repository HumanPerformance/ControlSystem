from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko as miko
import sys

# --------------------------
class TUNNEL(QtCore.QThread):
    '''
    Open an SSH terminal at the address specified and send the command specified.

    INPUTS:
        - ADDR: The IP address of the SSH server to access. (String)
        - CMD: The single command, in the proper format, that is to be executed. (String)

    OUTPUT:
        - output: Reading from the socket's stdout, or else an error message.  (String)
    '''
    output = QtCore.pyqtSignal(str)

    # ----------------------
    def __init__(self):
        super(TUNNEL, self).__init__()
        self.usr  = "pi"
        self.pwrd = "raspberry"

        self.ssh = miko.SSHClient()
        self.ssh.set_missing_host_key_policy(miko.AutoAddPolicy())
        self.ssh_stdin  = None
        self.ssh_stdout = None
        self.ssh_stderr = None

    # ----------------------
    def locate(CMD, ADDR):
        print("BLUE")
        self.cmd  = CMD
        self.addr = ADDR

    # ----------------------
    def run(self):
        print("Beginning SSH Tunnel: " + ADDR)
        _translate = QtCore.QCoreApplication.translate

        try:
            self.ssh.connect(self.addr, username= self.usr, password= self.pwrd)
            self.ssh_stdin, self.ssh_stdout, self.ssh_stderr = self.ssh.exec_command(self.cmd)

        except Exception as e:
            sys.stderr.write("SSH connection error: {0}".format(e))
            self.output.emit("ERR: SSH")
            print("ERR: SSH")

        if self.ssh_stdout:
            output =  self.ssh_stdout.read()
            self.output.emit(output)
            print(output)

        else:
            self.output.emit("ERR: NULL")
            print("ERR: NULL")

# --------------------------
