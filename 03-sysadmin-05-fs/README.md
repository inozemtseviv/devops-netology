# Домашнее задание к занятию «3.5. Файловые системы»

1. Узнайте
   о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (
   разряженных) файлах.

Это такие файлы, которые занимают меньше дискового пространства, чем их собственный размер. В файле высвобождаются
области, занятые одними лишь нулями (0x00). Приложение, читающее разреженный файл, дойдя до области с нулями, прочитает
нули, но реального чтения с диска не произойдёт.
Таким образом можно создавать файлы гигантского размера, состоящие из нулей, но на диске они могут занимать всего лишь
несколько килобайт. Реальное дисковое пространство выделяется тогда, когда вместо 0x00 записываются какие-то другие
данные. Разреженность поможет сэкономить дисковое пространство только в таких файлах, в которых есть действительно
большие пустые области.

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

Нет, не могут. Жесткие ссылки используют одну и ту же inode.

3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

```shell
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provider :virtualbox do |vb|
    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
  end
end
```

Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

```shell
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop /snap/core20/1328
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk
sdc                         8:32   0  2.5G  0 disk
```

4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

```shell
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop /snap/core20/1623
loop4                       7:4    0   48M  1 loop /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
└─sdb2                      8:18   0  511M  0 part
sdc                         8:32   0  2.5G  0 disk
```

5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

```shell
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop /snap/core20/1623
loop4                       7:4    0   48M  1 loop /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
└─sdb2                      8:18   0  511M  0 part
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
└─sdc2                      8:34   0  511M  0 part
```

6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

```shell
vagrant@vagrant:~$ sudo mdadm --create /dev/md0 -l 1 -n 2 /dev/sdb1 /dev/sdc1
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
```

7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

```shell
vagrant@vagrant:~$ sudo mdadm --create /dev/md1 -l 0 -n 2 /dev/sdb2 /dev/sdc2
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
```

8. Создайте 2 независимых PV на получившихся md-устройствах.

```shell
vagrant@vagrant:~$ sudo pvcreate /dev/md1 /dev/md0
vagrant@vagrant:~$ sudo pvscan
  PV /dev/sda3   VG ubuntu-vg       lvm2 [<62.50 GiB / 31.25 GiB free]
  PV /dev/md0                       lvm2 [<2.00 GiB]
  PV /dev/md1                       lvm2 [1018.00 MiB]
  Total: 3 [<65.49 GiB] / in use: 1 [<62.50 GiB] / in no VG: 2 [2.99 GiB]
```

9. Создайте общую volume-group на этих двух PV.

```shell
vagrant@vagrant:~$ sudo vgcreate VG1 /dev/md0 /dev/md1
vagrant@vagrant:~$ sudo vgscan
  Found volume group "ubuntu-vg" using metadata type lvm2
  Found volume group "VG1" using metadata type lvm2
```

10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

```shell
vagrant@vagrant:~$ sudo lvcreate -L 100M -n LV1 VG1 /dev/md1
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm
```

11. Создайте `mkfs.ext4` ФС на получившемся LV.

```shell
vagrant@vagrant:~$ sudo mkfs.ext4 /dev/VG1/LV1
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done
Writing inode tables: done
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```

12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

```shell
vagrant@vagrant:~$ mkdir /tmp/new
vagrant@vagrant:~$ sudo mount /dev/VG1/LV1 /tmp/new
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
```

13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

```shell
vagrant@vagrant:~$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
vagrant@vagrant:~$ ls -l /tmp/new
total 21924
drwx------ 2 root root    16384 Sep 23 12:42 lost+found
-rw-r--r-- 1 root root 22430863 Sep 23 11:08 test.gz
```

14. Прикрепите вывод `lsblk`.

```shell
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
```

15. Протестируйте целостность файла:

```shell
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~# echo $?
0
```

16. Используя `pvmove`, переместите содержимое PV с RAID0 на RAID1.

```shell
vagrant@vagrant:~$ sudo pvmove /dev/md1 /dev/md0
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 43.6M  1 loop  /snap/snapd/14978
loop1                       7:1    0 67.2M  1 loop  /snap/lxd/21835
loop2                       7:2    0 61.9M  1 loop  /snap/core20/1328
loop3                       7:3    0 63.2M  1 loop  /snap/core20/1623
loop4                       7:4    0   48M  1 loop  /snap/snapd/16778
loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
│   └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
│   └─VG1-LV1             253:1    0  100M  0 lvm   /tmp/new
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
```

17. Сделайте `--fail` на устройство в вашем RAID1 md.

```shell
sudo mdadm /dev/md0 -f /dev/sdc1
```

18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

```shell
vagrant@vagrant:~$ dmesg
...
[10050.546095]  sdb: sdb1 sdb2
[10113.882648]  sdc: sdc1 sdc2
[10184.797015] md/raid1:md0: not clean -- starting background reconstruction
[10184.797016] md/raid1:md0: active with 2 out of 2 mirrors
[10184.797037] md0: detected capacity change from 0 to 2144337920
[10184.798831] md: resync of RAID array md0
[10195.175391] md: md0: resync done.
[10260.364362] md1: detected capacity change from 0 to 1067450368
[10526.596968] EXT4-fs (dm-1): mounted filesystem with ordered data mode. Opts: (null)
[10526.596972] ext4 filesystem being mounted at /tmp/new supports timestamps until 2038 (0x7fffffff)
[10811.819660] md/raid1:md0: Disk failure on sdc1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.
```

19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

```shell
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~# echo $?
0
```

20. Погасите тестовый хост, `vagrant destroy`.

