#!/usr/bin/env python3

import socket
import time
import json
import yaml

services = {
    'drive.google.com': '',
    'mail.google.com': '',
    'google.com': ''
}

for service in services:
    current_host = socket.gethostbyname(service)
    services[service] = current_host

    with open(service + '.json', 'w') as json_output:
        json_data = json.dumps({service: services[service]})
        json_output.write(json_data)

    with open(service + '.yaml', 'w') as yaml_output:
        yaml_data = yaml.dump([{service: services[service]}])
        yaml_output.write(yaml_data)

while True:
    for service in services:
        current_host = services[service]
        new_host = socket.gethostbyname(service)
        if new_host != current_host:
            services[service] = new_host
            print(f'[ERROR] {service} IP mismatch: {current_host} {new_host}')

            with open(service + '.json', 'w') as json_output:
                json_data = json.dumps({service: services[service]})
                json_output.write(json_data)

            with open(service + '.yaml', 'w') as yaml_output:
                yaml_data = yaml.dump([{service: services[service]}])
                yaml_output.write(yaml_data)

        print(f'{service} IP: {new_host}')

    time.sleep(10)
