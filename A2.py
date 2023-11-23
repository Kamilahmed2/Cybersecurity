
import paramiko
import difflib

# Specify the parameters required to establish an SSH connection.
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
new_hostname = 'R3'

def connect_to_ssh(ip_address, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password, allow_agent=False, look_for_keys=False)
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

# If the connection was successful, create a new channel for remote commands:
channel = ssh_client.invoke_shell()

# Transmit the command to alter the device’s hostname.
channel.send('configure terminal\n')
channel.send('hostname ' + new_hostname + '\n')
channel.send('end\n')

# Pause execution until the command has finished processing.
while not channel.recv_ready():
    pass

# Display the output of the command on the console.
print(channel.recv(1024).decode('utf-8'))

# Transmit a command to configure loopback and at least one other interface.
channel.send('configure terminal\n')
channel.send('interface loopback0\n')
channel.send('ip address 1.1.1.1 255.255.255.255\n')
channel.send('exit\n')
channel.send('interface gigabitethernet0/0\n')  # Modify with the appropriate interface
channel.send('ip address 192.168.1.1 255.255.255.0\n')  # Modify with the appropriate IP
channel.send('no shutdown\n')
channel.send('end\n')

# Pause execution until the command has finished processing.
while not channel.recv_ready():
    pass

# Display the output of the command on the console.
print(channel.recv(1024).decode('utf-8'))

# Transmit a command to configure OSPF (you can modify it for EIGRP/RIP).
channel.send('configure terminal\n')
channel.send('router ospf 1\n')  # Modify the process ID as needed
channel.send('network 1.1.1.1 0.0.0.0 area 0\n')  # Modify the network and area as needed
channel.send('network 192.168.1.0 0.0.0.255 area 0\n')  # Modify the network and area as needed
channel.send('end\n')

# Pause execution until the command has finished processing.
while not channel.recv_ready():
    pass

# Display the output of the command on the console.
print(channel.recv(1024).decode('utf-8'))

# Transmit a command to generate the running configuration output.
channel.send('show running-config\n')

# Pause execution until the command has finished processing.
while not channel.recv_ready():
    pass

# Display the output of the command on the console.
running_config = channel.recv(1024).decode('utf-8')
print(running_config)

# Save the running configuration to a local file.
with open('running_config.txt', 'w') as f:
    f.write(running_config)

# Compare the running configuration with the local offline version.
with open('devices-08.txt', 'r') as file:
    local_config = file.read()

diff = difflib.ndiff(local_config.splitlines(keepends=True),
                     running_config.splitlines(keepends=True))
diff_text2 = ''.join(diff)

# Save the comparison text to a local file.
with open('config_comparison2.txt', 'w') as file:
    file.write(diff_text2)

# Terminate the SSH connection.
