# Домашнее задание к занятию «4.2. Использование Python для решения типовых DevOps задач»

1.
Есть скрипт:

```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

| Вопрос                                         | Ответ                                                                      |
|------------------------------------------------|----------------------------------------------------------------------------|
| Какое значение будет присвоено переменной `c`? | Будет ошибка TypeError: unsupported operand type(s) for +: 'int' and 'str' |
| Как получить для переменной `c` значение 12?   | c = str(a) + b                                                             |
| Как получить для переменной `c` значение 3?    | c = a + int(b)                                                             |

2.
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ./", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
    elif result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print(prepare_result)
```

Вывод после `git add .`:
```shell
04-script-02-py/README.md
README.md
```

3.
Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

```python
#!/usr/bin/env python3

import os
import sys

path = "./"
if len(sys.argv) >= 2:
    path = sys.argv[1]
    if not os.path.isdir(path):
        sys.exit("Несуществующий путь: " + path)

bash_command = ["cd " + path, "git status 2>&1"]
git_command = ["git rev-parse --show-toplevel"]
result_os = os.popen(' && '.join(bash_command)).read()
if result_os.find('not a git') != -1:
    sys.exit("Не является репозиторием: " + path)

git_top_level = (os.popen(' && '.join(git_command)).read()).replace('\n', '/')
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
    elif result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print(prepare_result)
```

Вывод:
```shell
# Есть репозиторий
./04-script-02-py/04-script-02-py.py
04-script-02-py/04-script-02-py.py
04-script-02-py/README.md
README.md

# Есть репозиторий и указан путь
./devops-netology/04-script-02-py/04-script-02-py.py ./devops-netology
fatal: not a git repository (or any of the parent directories): .git
04-script-02-py/04-script-02-py.py
04-script-02-py/README.md
README.md

# Нет репозитория
./devops-netology/04-script-02-py/04-script-02-py.py                  
Не является репозиторием: ./
```

4.
Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.
```python
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
```

Вывод:
```shell
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
drive.google.com IP: 173.194.222.194
mail.google.com IP: 142.251.1.18
google.com IP: 64.233.162.100
```