import os
import paramiko
#paramiko.util.log_to_file('/tmp/paramiko.log')
#paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

host = '10.171.190.91'
port = 22
username = 'pi'
password = 'raspberry'

#files = ['file1', 'file2', 'file3', 'file4']
remote_path = '/home/pi/pd3d/csec/repos/ControlSystem/Software/Python/consys/output.zip'
local_path = 'C:/Users/fluviolobo/Desktop/output.zip'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=username, password=password)
sftp = ssh.open_sftp()

sftp.get(remote_path, local_path)

sftp.close()
ssh.close()
