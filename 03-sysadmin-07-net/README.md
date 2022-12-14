# Домашнее задание к занятию «3.7. Компьютерные сети, лекция 2»

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?
```shell
ip link для Linux и ipconfig для Windows
```

2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для
   этого?
```shell
Протокол LLDP

Пакет lldpd, команда lldpctl
```

3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды
   есть в Linux для этого? Приведите пример конфига.
```shell
Технология VLAN
Пакет vlan, команда vconfig

auto vlan1400
iface vlan1400 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        vlan_raw_device eth0
```

4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.
```shell
Типы агрегации бывают статическими и динамическими.
Опции для балансирования нагрузки:
- Mode-0(balance-rr)
- Mode-1(active-backup)
- Mode-2(balance-xor)
- Mode-3(broadcast)
- Mode-4(802.3ad)
- Mode-5(balance-tlb)
- Mode-6(balance-alb)

Пример конфига:
auto bond0
iface bond0 inet dhcp
   bond-slaves eth0 eth1
   bond-mode active-backup
   bond-miimon 100
   bond-primary eth0 eth1
```

5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите
   несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
```shell
В сети с маской /29 8 адресов - 2 зарезервированных, а 6 узловых.

Из сети с маской /24 можно получить 32 подсети с маской /29.
10.10.10.0/29
10.10.10.8/29
```

6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
   уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов
   внутри подсети.
```shell
100.64.0.0/26 (rfc6598)
```

7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один
   нужный IP?
```shell
Проверить ARP таблицу:
- Linux - ip neighbour show
- Windows - arp -a

Очистить ARP кеш:
- Linux - ip neighbour flush all
- Windows - arp -d *

Из ARP таблицы удалить только один нужный IP:
- Linux - ip neighbour del <ip_address> dev <interface>
- Windows - arp -d <ip_address>
```
