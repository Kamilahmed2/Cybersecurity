from netmiko import ConnectHandler

def establish_netmiko_connection(device_info):
    try:
        net_connect = ConnectHandler(**device_info)
        print(f"Connected to {device_info['device_type']} device.")

        return net_connect
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return None

def modify_hostname(net_connect, new_hostname):
    config_commands = [f"hostname {new_hostname}"]
    output = net_connect.send_config_set(config_commands)
    print(output)

def save_running_config(net_connect, output_file):
    running_config = net_connect.send_command("show running-config")
    with open(output_file, 'w') as file:
        file.write(running_config)

def main():
    device_info = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.1',  # Replace with the actual IP address of your device
        'username': 'your_username',
        'password': 'your_password',
        'secret': 'your_enable_password',
    }

    new_hostname = 'NewRouterHostname'
    output_file = 'running_config.txt'

    net_connect = establish_netmiko_connection(device_info)

    if net_connect:
        modify_hostname(net_connect, new_hostname)
        save_running_config(net_connect, output_file)

        print(f"Hostname modified to {new_hostname}")
        print(f"Running configuration saved to {output_file}")

        net_connect.disconnect()

if __name__ == "__main__":
    main()
