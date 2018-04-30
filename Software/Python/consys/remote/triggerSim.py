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
SSH_ADDRESS = (["10.171.190.91",            # panel 001 - 001
                "10.171.190.201",           # panel 001 - 002
                "10.171.190.176",           # panel 002 - 001
                "10.171.190.90"])           # panel 002 - 002
SSH_USERNAME = "pi"
SSH_PASSWORD = "raspberry"
SSH_DIR = "pd3d/csec/repos/ControlSystem/Software/Python/consys/"
SSH_COMMAND = (["python " + SSH_DIR + "consys4.3.py",
                "python " + SSH_DIR + "consys4.3bpc.py"])
ssh = miko.SSHClient()
ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

ssh_stdin = ssh_stdout = ssh_stderr = None

# -------------------------------------------------------------------------------- #
# Operation: Communicating with system over ssh
# -------------------------------------------------------------------------------- #
try:
    ssh.connect(SSH_ADDRESS[2], username=SSH_USERNAME, password=SSH_PASSWORD)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND[0])
    
except Exception as e:
    sys.stderr.write("SSH connection error: {0}".format(e))

if ssh_stdout:
    output = ssh_stdout.read()
    print(output)

"""
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
