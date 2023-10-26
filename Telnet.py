import telnetlib

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

if __name__ == "__main__":
    host = "192.168.56.101"
    username = input('Enter a Username: ')
    password = input('Enter a Password: ')
    hostname = "R1"

    if establish_telnet_connection(host, username, password, hostname):
        print("---------------------------------------------------------------')
        print("----- SUCESS! Connecting to:", username)
        print("-----              Username:", username)
        print("-----              Password:", Password)
        print("----- New Hostname: ", hostname)
        print("Running configuration saved to runninf_config.txt")
