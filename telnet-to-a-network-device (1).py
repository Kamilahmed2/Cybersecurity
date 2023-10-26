import telnetlib

# Define Variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
new_hostname = 'NewHostname'

# Establish Telnet Connection
telnet_connection = telnetlib.Telnet(ip_address)
print('11')  # Prints lines from 11-42

# Login to the device
telnet_connection.read_until(b'Username: ')
telnet_connection.write(username.encode('ascii') + b'\n')
telnet_connection.read_until(b'Password: ')
telnet_connection.write(password.encode('ascii') + b'\n')
print('17')  

# Enter Privileged EXEC Mode
telnet_connection.read_until(b'#')
print('23')  

# Configure the device
telnet_connection.write(b'configure terminal\n')
telnet_connection.read_until(b'#')
telnet_connection.write(f'hostname {new_hostname}\n'.encode('ascii'))
telnet_connection.read_until(b'#')

# Save the configuration
telnet_connection.write(b'end\n')
telnet_connection.read_until(b'#')
telnet_connection.write(b'write memory\n')
telnet_connection.read_until(b'#')
print("35")  

# Send a command to the remote device to output the running configuration 
telnet_connection.write(b'show running-config\n')
output = telnet_connection.read_until(b'end').decode('ascii')
print("38") 

# Save the output to a file
with open('running_config.txt', 'w') as file:
    file.write(output)

# Close the Telnet Connection
telnet_connection.write(b'quit\n')
print("42")  


