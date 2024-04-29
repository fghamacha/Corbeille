#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import socket
import configparser

def find_consecutive_ports(start_port, num_ports):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', start_port))
            except OSError:
                start_port += 50
                continue
        
        consecutive_ports = [start_port]
        for port in range(start_port + 1, start_port + num_ports):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    consecutive_ports.append(port)
                except OSError:
                    start_port += 50
                    break
        else:
            return consecutive_ports

def check_existing_ports(project_name, ports):
    config = configparser.ConfigParser()
    config.read(project_name)
    if 'Ports' in config:
        start_port = int(config['Ports']['start_port'])
        end_port = int(config['Ports']['end_port'])
        for port in ports:
            if start_port <= port <= end_port:
                return False
    return True

def write_ports_to_config(project_name, ports):
    if check_existing_ports(project_name, ports):
        config = configparser.ConfigParser()
        config[project_name] = {'start_port': str(ports[0]), 'end_port': str(ports[-1])}
        with open(project_name, 'a') as configfile:
            config.write(configfile)
    else:
        print("Les ports existent déjà dans le range de ports du projet.")

def main():
    module = AnsibleModule(
        argument_spec=dict(
            start_port=dict(type='int', required=True),
            num_ports=dict(type='int', required=True),
            config_file=dict(type='str', required=True),
            application_name=dict(type='str', required=True)
        )
    )

    start_port = module.params['start_port']
    num_ports = module.params['num_ports']
    config_file = module.params['config_file']
    application_name = module.params['application_name']
    
    ports = find_consecutive_ports(start_port, num_ports)
    write_ports_to_config(config_file, ports)
    
    module.exit_json(changed=True, ports=ports)

if __name__ == '__main__':
    main()
