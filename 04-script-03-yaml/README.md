# Домашнее задание к занятию «4.3. Языки разметки JSON и YAML»

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
Нужно найти и исправить все ошибки, которые допускает наш сервис

```json
{
  "info": "Sample JSON output from our service\t",
  "elements": [
    {
      "name": "first",
      "type": "server",
      "ip": 7175
    },
    {
      "name": "second",
      "type": "proxy",
      "ip": "71.78.22.43"
    }
  ]
}
```

2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

Скрипт:
```python
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
```

Вывод при запуске:
```shell
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.17
google.com IP: 64.233.162.101
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.17
google.com IP: 64.233.162.101
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.17
google.com IP: 64.233.162.101
```

json-файл(ы):
```shell
{"drive.google.com": "173.194.222.194"}

{"google.com": "64.233.162.101"}

{"mail.google.com": "142.251.1.17"}
```

yaml-файл(ы):
```shell
- drive.google.com: 173.194.222.194

- google.com: 64.233.162.101

- mail.google.com: 142.251.1.17
```
