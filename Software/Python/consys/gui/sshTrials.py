import paramiko as miko
import sys

## EDIT SSH DETAILS ##

SSH_ADDRESS = "192.168.0.27"
SSH_USERNAME = "root"
SSH_PASSWORD = "dietpi"
SSH_DIR = "/home/git/ControlSystem/Software/Python/consys/"
SSH_COMMAND = "python " + SSH_DIR + "single.py"

ssh = miko.SSHClient()
ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

ssh_stdin = ssh_stdout = ssh_stderr = None
output = []

try:
    ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)
    
except Exception as e:
    sys.stderr.write("SSH connection error: {0}".format(e))

if ssh_stdout:
    raw = str( ssh_stdout.read() )
    output = raw.split(" ")
    lines = len(output)
    print( output[lines-1] )

### extract output flag ------------------------------------------------------------ #
##delimeter = (["\n", " "])
##outList = output.split( delimeter[0] )                                             
##N_lines = len(outList)
##status_flag = outList[N_lines - 2].split( delimeter[1] )[1]
##print( status_flag )
##
### translate flag ----------------------------------------------------------------- #
##if( status_flag == "AOK" ):
##    print( "Program completed successfully" )
##else:
##    print( "Program execution failed... revise log" )
