import paramiko as miko
import sys

## EDIT SSH DETAILS ##

#SSH_ADDRESS = "192.168.42.46"
SSH_ADDRESS = "10.171.190.201"
SSH_USERNAME = "pi"
SSH_PASSWORD = "raspberry"
#SSH_COMMAND = "sudo python pd3d/csec/repos/ControlSystem/Software/Python/consys/printme.py"
SSH_COMMAND = "sudo reboot"

ssh = miko.SSHClient()
ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

ssh_stdin = ssh_stdout = ssh_stderr = None

try:
    ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)
    
except Exception as e:
    sys.stderr.write("SSH connection error: {0}".format(e))

if ssh_stdout:
    output = ssh_stdout.read()
    print(output)

#if ssh_stderr:
#   print(ssh_stderr.read())
