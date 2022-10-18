#!/usr/bin/env python3

import socket
import time

services = {
    'drive.google.com': '',
    'mail.google.com': '',
    'google.com': ''
}

for service in services:
    current_host = socket.gethostbyname(service)
    services[service] = current_host

while True:
    for service in services:
        current_host = services[service]
        new_host = socket.gethostbyname(service)
        if new_host != current_host:
            services[service] = new_host
            print(f'[ERROR] {service} IP mismatch: {current_host} {new_host}')

        print(f'{service} IP: {new_host}')

    time.sleep(10)
