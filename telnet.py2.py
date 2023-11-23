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
        running_config = tn.read_until(b"#").decode('utf-8')
        
        with open(f"{hostname}_running_config.txt", "w") as config_file:
            config_file.write(running_config)

        # Save startup configuration to a file
        tn.write(b"show startup-config\n")
        startup_config = tn.read_until(b"#").decode('utf-8')
        
        with open(f"{hostname}_startup_config.txt", "w") as config_file:
            config_file.write(startup_config)

        tn.close()
        return running_config, startup_config
    except Exception as e:
        print(f"Telnet connection failed: {str(e)}")
        return None, None

def compare_configurations(running_config, startup_config, local_offline_config):
    # Compare running configuration with startup configuration
    diff_startup = difflib.ndiff(running_config.splitlines(keepends=True),
                                 startup_config.splitlines(keepends=True))
    diff_text_startup = ''.join(diff_startup)

    # Save the comparison text to a local file
    with open('config_comparison_startup.txt', 'w') as file:
        file.write(diff_text_startup)

    # Compare running configuration with local offline version
    diff_local = difflib.ndiff(local_offline_config.splitlines(keepends=True),
                               running_config.splitlines(keepends=True))
    diff_text_local = ''.join(diff_local)

    # Save the comparison text to a local file
    with open('config_comparison_local.txt', 'w') as file:
        file.write(diff_text_local)

if __name__ == "__main__":
    import difflib

    host = "192.168.56.101"
    username = input('Enter a Username: ')
    password = input('Enter a Password: ')
    enable_password = input('Enter the Enable Password: ')
    hostname = "R1"

    # Fetch running and startup configurations
    running_config, startup_config = establish_telnet_connection(host, username, password, enable_password, hostname)

    if running_config is not None and startup_config is not None:
        # Fetch local offline version
        with open('devices-07.txt', 'r') as file:
            local_offline_config = file.read()

        # Compare configurations
        compare_configurations(running_config, startup_config, local_offline_config)

        print("---------------------------------------------------------------")
        print("----- SUCCESS! Connecting to:", username)
        print("----- Username:", username)
        print("----- Password:", password)
        print("----- Enable Password:", enable_password)
        print("----- New Hostname:", hostname)
        print("----- Running configuration saved to runninf_config.txt")
        print("----- Startup configuration saved to startup_config.txt")
        print("----- Configurations compared and differences saved.")
