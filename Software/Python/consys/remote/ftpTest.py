import paramiko

def create_sftp_client(host, port, username, password, keyfilepath, keyfiletype):
    """
    create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

    Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
    supplied username and supplied password or with the private key in a file with the supplied path.
    If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
    :rtype: SFTPClient object.
    """
    sftp = None
    key = None
    transport = None
    try:
        if keyfilepath is not None:
            # Get private key used to authenticate user.
            if keyfiletype == 'DSA':
                # The private key is a DSA type key.
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                # The private key is a RSA type key.
                key = paramiko.RSAKey.from_private_key(keyfilepath)

        # Create Transport object using supplied method of authentication.
        transport = paramiko.Transport((host, port))
        transport.connect(None, username, password, key)

        sftp = paramiko.SFTPClient.from_transport(transport)

        return sftp
    except Exception as e:
        print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()
        pass


def create_sftp_client2(host, port, username, password, keyfilepath, keyfiletype):
    """
    create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

    Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
    supplied username and supplied password or with the private key in a file with the supplied path.
    If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
    :rtype: SFTPClient object.
    """
    ssh = None
    sftp = None
    key = None
    try:
        if keyfilepath is not None:
            # Get private key used to authenticate user.
            if keyfiletype == 'DSA':
                # The private key is a DSA type key.
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                # The private key is a RSA type key.
                key = paramiko.RSAKey.from_private_key(keyfilepath)

        # Connect SSH client accepting all host keys.
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password, key)

        # Using the SSH client, create a SFTP client.
        sftp = ssh.open_sftp()
        # Keep a reference to the SSH client in the SFTP client as to prevent the former from
        # being garbage collected and the connection from being closed.
        sftp.sshclient = ssh

        return sftp
    except Exception as e:
        print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
        if sftp is not None:
            sftp.close()
        if ssh is not None:
            ssh.close()
        pass

# ------------------------------------------------------------------------------------------------- #

## EDIT SSH DETAILS ##

SSH_ADDRESS = "10.171.190.91"
SSH_USERNAME = "pi"
SSH_PASSWORD = "raspberry"
#SSH_COMMAND = "sudo python pd3d/csec/repos/ControlSystem/Software/Python/consys/printme.py"
SSH_COMMAND = "ls"

local_file_path = "C:/Users/fluviolobo/Desktop/hola.txt"
#remote_file_path = "/home/pi/pd3d/csec/repos/ControlSystem/Software/Python/consys/output/output.txt"
#remote_file_path = "install_2018-04-03-19-16-14.log"
remote_file_path = "/Desktop/hola.txt"


host = '10.171.190.201'
port = 22
username = 'pi'
keyfile_path = None
password = 'raspberry'

sftpclient = create_sftp_client(host, port, username, password, keyfile_path, 'DSA')

# List files in the default directory on the remote computer.
sftpclient.chdir("./Desktop")
dirlist = sftpclient.listdir('.')
for row in dirlist:
    print row

# Retrieve a file with the name 'remote_file.txt' on the remote computer and store it in a file named 'downloaded_file.txt'
# next to this SFT client program.
sftpclient.get(remote_file_path, local_file_path)
# Upload a file that locally has the name 'testfile.txt' to a file on the remote computer that will have the name 'remote_testfile.txt'.
#sftpclient.put('testfile.txt', 'remote_testfile.txt')

# We're done with the SFTPClient.
sftpclient.close()
