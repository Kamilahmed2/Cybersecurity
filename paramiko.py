import paramiko
import difflib

def establish_ssh_connection(host, username, password, enable_password, hostname):
    try:
        # Connect using SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        # Configure the device hostname
        ssh_shell = ssh.invoke_shell()
        ssh_shell.send('enable\n')
        ssh_shell.send(enable_password + '\n')
        ssh_shell.send(f'configure terminal\n')
        ssh_shell.send(f'hostname {hostname}\n')
        ssh_shell.send(b'end\n')
        ssh_shell.send(b'write memory\n')

        # Save running configuration to a file
        stdin, stdout, stderr = ssh.exec_command('show running-config\n')
        output = stdout.read().decode('utf-8')

        with open(f"{hostname}_running_config.txt", "w") as config_file:
            config_file.write(output)

        # Read start-up configuration and compare with running configuration
        ssh.exec_command('show startup-config', get_pty=True)
        startup_output = stdout.read().decode('utf-8')

        diff = difflib.ndiff(startup_output.splitlines(keepends=True),
                              output.splitlines(keepends=True))
        diff_text = ''.join(diff)

        print("Running configuration compared with startup configuration:")
        print(diff_text)

        ssh.close()
        return True
    except Exception as e:
        print(f"SSH connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    host = "192.168.56.101"
    username = input('Enter a Username: ')
    password = input('Enter a Password: ')
    enable_password = input('Enter the Enable Password: ')
    hostname = "R1"

    if establish_ssh_connection(host, username, password, enable_password, hostname):
        print("---------------------------------------------------------------")
        print("----- SUCCESS! Connecting to:", username)
        print("----- Username:", username)
        print("----- Password:", password)
        print("----- Enable Password:", enable_password)
        print("----- New Hostname: ", hostname)
        print("Running configuration saved to runninf_config.txt")
        print("Differences between running and startup configurations are printed above.")

