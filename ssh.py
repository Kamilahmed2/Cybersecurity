   import paramiko


# “Specify the parameters required to establish an SSH connection.”
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
new_hostname = 'R3'


def connect_to_ssh(ip_address, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password,allow_agent=False,look_for_keys=False)
        print(f"SSH connection successful to {ip_address}")
        return ssh
    except paramiko.AuthenticationException:
        print('---FAILURE! Authentication failed, please verify your credentials')
        exit()
    except paramiko.SSHException as sshException:
        print('---FAILURE! Unable to establish SSH connection: ', sshException)
        exit()
    except paramiko.BadHostKeyException as badHostKeyException:
        print('---FAILURE! Unable to verify server\'s host key: ', badHostKeyException)
        exit()

ssh_client = connect_to_ssh(ip_address, username, password)


# “If the connection was successful, create a new channel for remote commands”:
channel = ssh_client.invoke_shell()

# “Transmit the command to alter the device’s hostname.”
channel.send('configure terminal\n')
channel.send('hostname ' + new_hostname + '\n')
channel.send('end\n')


# “Pause execution until the command has finished processing.”
while not channel.recv_ready():
    pass


# “Display the output of the command on the console.”
print(channel.recv(1024).decode('utf-8'))


# “Transmit a command to the remote device to generate the running configuration output and store it in a local file.”
channel.send('show running-config\n')

# “Pause execution until the command has finished processing.”
while not channel.recv_ready():
    pass

# “Display the output of the command on the console.”
print(channel.recv(1024).decode('utf-8'))

# “Redirect the output to a text file.”
with open('running_config.txt', 'w') as f:
    f.write(channel.recv(1024).decode('utf-8'))

# “Terminate the SSH connection.”
ssh_client.close()
   
   
   
   
   
   
    if establish_telnet_connection(host, username, password, hostname):
        print("---------------------------------------------------------------')
        print("----- SUCCESS! Connecting to:", username)
        print("-----              Username:", username)
        print("-----              Password:", Password)
        print("----- New Hostname: ", hostname)
        print("Running configuration saved to runninf_config.txt")