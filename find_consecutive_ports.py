#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import socket
import configparser

# Function to check if ports already exist in the ports inventory
def check_ports_in_inventory(config, start_port, num_ports):
    for section in config.sections():
        current_start_port = int(config[section]['start_port'])
        current_end_port = int(config[section]['end_port'])
        if start_port + num_ports - 1 < current_start_port or start_port > current_end_port:
            continue  # The port range does not interfere with the current range, move to the next section
        else:
            return True  # The port range is already used in the inventory
    return False

# Function to check if ports are already in listening state on the server
def check_ports_listening(start_port, num_ports):
    for port in range(start_port, start_port + num_ports):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
            except OSError:
                return True  # The port is in listening state
    return False

# Function to find a range of consecutive available ports starting from a given start port
def find_consecutive_ports(start_port, num_ports, inventory_file):
    config = configparser.ConfigParser()
    config.read(inventory_file)
    
    while True:
        # Check if the port range already exists in the inventory
        if not check_ports_in_inventory(config, start_port, num_ports):
            # Check if the ports are not in listening state on the server
            if not check_ports_listening(start_port, num_ports):
                return list(range(start_port, start_port + num_ports))

        # Increment the start port if the port range is already used
        start_port += 50

# Function to write the found ports into the ports inventory
def store_ports_in_inventory(inventory_file, start_port, num_ports):
    config = configparser.ConfigParser()
    config.read(inventory_file)
    section_name = 'Ports'  # Name of the section for ports
    config[section_name] = {'start_port': str(start_port), 'end_port': str(start_port + num_ports - 1)}
    with open(inventory_file, 'w') as configfile:
        config.write(configfile)

# Main function of the Ansible module
def main():
    module = AnsibleModule(
        argument_spec=dict(
            start_port=dict(type='int', required=True),  # Argument to specify the start port
            num_ports=dict(type='int', required=True),   # Argument to specify the number of ports
            inventory_file=dict(type='str', required=True),  # Argument to specify the ports inventory
            application_name=dict(type='str', required=True)  # Argument to specify the application name
        )
    )

    start_port = module.params['start_port']  # Retrieve the start port from the passed parameters
    num_ports = module.params['num_ports']    # Retrieve the number of ports from the passed parameters
    inventory_file = module.params['inventory_file']  # Retrieve the ports inventory from the passed parameters
    application_name = module.params['application_name']  # Retrieve the application name from the passed parameters
    
    # Find consecutive ports
    ports = find_consecutive_ports(start_port, num_ports, inventory_file)
    
    # Write the found ports into the ports inventory
    store_ports_in_inventory(inventory_file, ports[0], num_ports)
    
    # Exit the module execution with the found ports
    module.exit_json(changed=True, ports=ports)

if __name__ == '__main__':
    main()
