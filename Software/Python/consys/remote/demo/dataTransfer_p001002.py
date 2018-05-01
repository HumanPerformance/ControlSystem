"""
dataTransfer.py

Script designed to allow remote retrieval of output data

Fluvio L Lobo Fenoglietto 04/30/2018
"""

# -------------------------------------------------------------------------------- #
# Import Modules and Libraries
# -------------------------------------------------------------------------------- #
import os
import paramiko

# -------------------------------------------------------------------------------- #
# Variables
# -------------------------------------------------------------------------------- #
#host = '192.168.42.10'
host = '10.171.190.91'
port = 22
username = 'pi'
password = 'raspberry'
remote_path = '/home/pi/pd3d/csec/repos/ControlSystem/Software/Python/consys/output.zip'
local_path = 'C:/Users/fluviolobo/Desktop/output.zip'

# -------------------------------------------------------------------------------- #
# Operation: Communicating with system over ssh
# -------------------------------------------------------------------------------- #
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=username, password=password)
sftp = ssh.open_sftp()

sftp.get(remote_path, local_path)

sftp.close()
ssh.close()
