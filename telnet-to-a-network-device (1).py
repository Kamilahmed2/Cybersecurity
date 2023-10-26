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
telnet_connection.read_until(b'#')import telnetlib

# Define Variables
ip_address = '192.168.56.101'
username = input('Enter a Username: ')
password = input('Enter a Password: ')
hostname = 'R1'

# Establish Telnet Connection
telnet_connection = telnetlib.Telnet(ip_address)


# Login to the device
telnet_connection.read_until(b'Username: ')
telnet_connection.write(username.encode('ascii') + b'\n')
telnet_connection.read_until(b'Password: ')
telnet_connection.write(password.encode('ascii') + b'\n')


# Enter Privileged EXEC Mode
telnet_connection.read_until(b'#')


# Configure the device
telnet_connection.write(b'configure terminal\n')
telnet_connection.read_until(b'#')
telnet_connection.write(f'hostname {hostname}\n'.encode('ascii'))
telnet_connection.read_until(b'#')

# Save the configuration
telnet_connection.write(b'end\n')
telnet_connection.read_until(b'#')
telnet_connection.write(b'write memory\n')
telnet_connection.read_until(b'#')


# Send a command to the remote device to output the running configuration 
telnet_connection.write(b'show running-config\n')
output = telnet_connection.read_until(b'end').decode('ascii')

# Save the output to a file
with open('running_config.txt', 'w') as file:
    file.write(output)

print("---------------------------------------------------------------")
print("----- SUCESS! Connecting to:", ip_address)
print("-----              Username:", username)
print("-----              Password:", password)
print("----- New Hostname: ", hostname)
print("Running configuration saved to runninf_config.txt")

# Close the Telnet Connection
telnet_connection.write(b'quit\n')


