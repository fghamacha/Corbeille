#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import socket
import configparser

# Fonction pour trouver un range de ports consécutifs disponibles à partir d'un port de départ
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

# Fonction pour vérifier si les ports existent déjà dans le fichier d'inventaire
def check_ports_in_inventory(config_file, ports):
    config = configparser.ConfigParser()
    config.read(config_file)
    for section in config.sections():
        start_port = int(config[section]['start_port'])
        end_port = int(config[section]['end_port'])
        for port in ports:
            if start_port <= port <= end_port:
                return False
    return True

# Fonction pour écrire les ports trouvés dans le fichier d'inventaire
def store_ports_in_inventory(config_file, ports):
    if check_ports_in_inventory(config_file, ports):
        config = configparser.ConfigParser()
        config.read(config_file)
        section_name = 'Ports'  # Nom de la section pour les ports
        config[section_name] = {'start_port': str(ports[0]), 'end_port': str(ports[-1])}
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        print("Les ports existent déjà dans le fichier d'inventaire.")

# Fonction principale du module Ansible
def main():
    module = AnsibleModule(
        argument_spec=dict(
            start_port=dict(type='int', required=True),  # Argument pour spécifier le port de départ
            num_ports=dict(type='int', required=True),   # Argument pour spécifier le nombre de ports
            config_file=dict(type='str', required=True),  # Argument pour spécifier le fichier d'inventaire
            application_name=dict(type='str', required=True)  # Argument pour spécifier le nom de l'application
        )
    )

    start_port = module.params['start_port']  # Récupère le port de départ depuis les paramètres passés
    num_ports = module.params['num_ports']    # Récupère le nombre de ports depuis les paramètres passés
    config_file = module.params['config_file']  # Récupère le fichier d'inventaire depuis les paramètres passés
    application_name = module.params['application_name']  # Récupère le nom de l'application depuis les paramètres passés
    
    ports = find_consecutive_ports(start_port, num_ports)  # Trouve les ports consécutifs
    store_ports_in_inventory(config_file, ports)  # Écrit les ports trouvés dans le fichier d'inventaire
    
    module.exit_json(changed=True, ports=ports)  # Termine l'exécution du module en retournant les ports trouvés

if __name__ == '__main__':
    main()
