import telnetlib
import paramiko

def establish_telnet_connection(host, username, password, enable_password, hostname):
    try:
        # Connect using Telnet
        tn = telnetlib.Telnet(host)
        tn.read_until(b"Username: ")
        tn.write(username.encode('utf-8') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('utf-8') + b"\n")
        tn.write(b"enable\n")
        tn.read_until(b"Password: ")
        tn.write(enable_password.encode('utf-8') + b"\n")

        # Configure the device hostname
        tn.write(f"configure terminal\n".encode('utf-8'))
        tn.write(f"hostname {hostname}\n".encode('utf-8'))
        tn.write(b"end\n")
        tn.write(b"write memory\n")

        # Save running configuration to a file
        tn.write(b"show running-config\n")
        output = tn.read_until(b"#").decode('utf-8')
        
        with open(f"{hostname}_running_config.txt", "w") as config_file:
            config_file.write(output)

        tn.close()
        return True
    except Exception as e:
        print(f"Telnet connection failed: {str(e)}")
        return False

def establish_ssh_connection(host, username, password, enable_password, hostname):
    try:
        # Connect using SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, allow_agent=False, look_for_keys=False)
        ssh_shell = ssh.invoke_shell()

        ssh_shell.send("enable\n")
        ssh_shell.send(enable_password + "\n")

        # Configure the device hostname
        ssh_shell.send(f"configure terminal\n")
        ssh_shell.send(f"hostname {hostname}\n")
        ssh_shell.send("end\n")
        ssh_shell.send("write memory\n")

        # Save running configuration to a file
        ssh_shell.send("show running-config\n")
        output = ssh_shell.recv(65535).decode('utf-8')

        with open(f"{hostname}_running_config.txt", "w") as config_file:
            config_file.write(output)

        ssh.close()
        return True
    except Exception as e:
        print(f"SSH connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    host = "YOUR_DEVICE_IP"
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    enable_password = input("Enter your enable password: ")
    hostname = "NEW_HOSTNAME"

    # Establish Telnet Connection
    if establish_telnet_connection(host, username, password, enable_password, hostname):
        print("Telnet connection established and configuration updated.")

    # Establish SSH Connection
    if establish_ssh_connection(host, username, password, enable_password, hostname):
        print("SSH connection established and configuration updated.")
