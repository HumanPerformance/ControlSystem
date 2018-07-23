"""
triggerSim.py

Script designed to trigger simulation remotely

Fluvio L Lobo Fenoglietto 04/30/2018
"""

# -------------------------------------------------------------------------------- #
# Import Modules and Libraries
# -------------------------------------------------------------------------------- #
import paramiko as miko
import sys

# -------------------------------------------------------------------------------- #
# Variables
# -------------------------------------------------------------------------------- #
SSH_ADDRESS = (["192.168.42.10",            # panel 001 - 001
                "192.168.42.12",            # panel 001 - 002
                "10.171.190.176",           # panel 002 - 001
                "10.171.190.90"])           # panel 002 - 002
SSH_USERNAME = "pi"
SSH_PASSWORD = "raspberry"
SSH_DIR = "pd3d/csec/repos/ControlSystem/Software/Python/consys/"
SSH_COMMAND = (["python " + SSH_DIR + "consys4.3.py",
                "DISPLAY=:0 python " + SSH_DIR + "consys4.3bpc.py"])
ssh = miko.SSHClient()
ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

ssh_stdin = ssh_stdout = ssh_stderr = None

# -------------------------------------------------------------------------------- #
# Operation: Communicating with system over ssh
# -------------------------------------------------------------------------------- #
try:
    for i in range( 0, 2 ):
        ssh.connect(SSH_ADDRESS[i], username=SSH_USERNAME, password=SSH_PASSWORD)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND[i])
    
except Exception as e:
    sys.stderr.write("SSH connection error: {0}".format(e))

"""
if ssh_stdout:
    output = ssh_stdout.read()
    print(output)


# extract output flag ------------------------------------------------------------ #
delimeter = (["\n", " "])
outList = output.split( delimeter[0] )                                             # split output on the basis of a delimeter
N_lines = len(outList)
status_flag = outList[N_lines - 2].split( delimeter[1] )[1]
print( status_flag )

# translate flag ----------------------------------------------------------------- #
if( status_flag == "AOK" ):
    print( "Program completed successfully" )
else:
    print( "Program execution failed... revise log" )
"""
