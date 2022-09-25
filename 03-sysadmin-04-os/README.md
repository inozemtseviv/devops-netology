# Домашнее задание к занятию «3.4. Операционные системы, лекция 2»

1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации
   его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где
   процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно
   простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    - поместите его в автозагрузку,
    - предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на
      systemctl cat cron),
    - удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки
      автоматически
      поднимается.

Добавил конфиг node_exporter с возможностью добавления опций через внешний файл:

```shell
vagrant@vagrant:~$ cat /etc/systemd/system/node_exporter.service
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
EnvironmentFile=/etc/default/node_exporter
ExecStart=/usr/local/bin/node_exporter $OPTIONS

[Install]
WantedBy=multi-user.target
```

Поместил node_exporter в автозагрузку, убедился, что он стартует и подымается после перезагрузки:

```shell
● node_exporter.service - Prometheus Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-09-25 08:56:17 UTC; 36s ago
   Main PID: 640 (node_exporter)
      Tasks: 4 (limit: 1066)
     Memory: 12.5M
     CGroup: /system.slice/node_exporter.service
             └─640 /usr/local/bin/node_exporter --collector.textfile.directory /var/lib/node_exporter/textfile_collector

Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=thermal_zone
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=time
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=timex
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=udp_queues
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=uname
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=vmstat
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=xfs
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:112 collector=zfs
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=node_exporter.go:191 msg="Listening on" address=:9100
Sep 25 08:56:18 vagrant node_exporter[640]: level=info ts=2022-09-25T08:56:18.049Z caller=tls_config.go:170 msg="TLS is disabled and it cannot be >
```

2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы
   выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

```shell
# CPU
process_cpu_seconds_total
node_cpu_seconds_total{cpu="0",mode="idle"}
node_cpu_seconds_total{cpu="0",mode="system"}
node_cpu_seconds_total{cpu="0",mode="user"}

# Память
node_memory_MemAvailable_bytes
node_memory_MemFree_bytes
node_memory_Buffers_bytes
node_memory_Cached_bytes

# Диск
node_filesystem_avail_bytes
node_disk_io_time_seconds_total{device="sda"}
node_disk_read_time_seconds_total{device="sda"}
node_disk_write_time_seconds_total{device="sda"}

# Сеть
node_network_info
node_network_receive_bytes_total
node_network_receive_errs_total
node_network_transmit_bytes_total
node_network_transmit_errs_total
```

3. Установите в свою виртуальную машину Netdata. Воспользуйтесь готовыми пакетами для
   установки (`sudo apt install -y netdata`). После успешной установки:
    - в конфигурационном файле `/etc/netdata/netdata.conf` в секции `[web]` замените значение с localhost
      на `bind to = 0.0.0.0`,
    - добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

```shell
    config.vm.network "forwarded_port", guest: 19999, host: 19999
```

После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на localhost:19999.
Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

```shell
vagrant@vagrant:~$ sudo ss -tulpn | grep 19999
tcp    LISTEN   0        4096              0.0.0.0:19999          0.0.0.0:*      users:(("netdata",pid=633,fd=4))
```

4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе
   виртуализации?

```shell
vagrant@vagrant:~$ dmesg | grep -i virt
[    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[    0.001937] CPU MTRRs all blank - virtualized system.
[    0.057220] Booting paravirtualized kernel on KVM
[    2.326688] systemd[1]: Detected virtualization oracle.
```

5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой
   существующий лимит не позволит достичь такого числа (`ulimit --help`)?

```shell
# nr_open - лимит на количество открытых дескрипторов. 
vagrant@vagrant:~$ /sbin/sysctl -n fs.nr_open
1048576

vagrant@vagrant:~$ cat /proc/sys/fs/nr_open
1048576

# а этот лимит не позволит достичь такого числа
vagrant@vagrant:~$ ulimit -n
1024
```

6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном
   неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через nsenter. Для простоты работайте в данном
   задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

```shell
vagrant@vagrant:~$ ps -aux | grep sleep
root        1655  0.0  0.0   5476   580 pts/0    S    11:08   0:00 sleep 1h
vagrant     1662  0.0  0.0   6432   720 pts/0    S+   11:08   0:00 grep --color=auto sleep
```

```shell
vagrant@vagrant:~$ sudo nsenter --target 1655 --pid --mount
root@vagrant:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   5476   580 pts/0    S    11:08   0:00 sleep 1h
root           2  0.0  0.4   7236  4076 pts/0    S    11:10   0:00 -bash
root          13  0.0  0.3   8888  3244 pts/0    R+   11:10   0:00 ps aux
```

7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu
   20.04 (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", после чего (минуты) – ОС
   должна стабилизироваться. Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. Как настроен этот
   механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

```shell
# это объявление и запуск функции с именем ":", которая вызывает себя рекурсивно и передается с помощью другому вызову этой же функции в фоне.

# стабилизация
[ 1190.692323] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-4.scope
```

```shell
# Максимальное количество одновременно созданных в сессии процессов.
vagrant@vagrant:~$ ulimit -u
3554

# Изменение этого параметра.
vagrant@vagrant:~$ ulimit -u 1001
vagrant@vagrant:~$ ulimit -u
1001
```