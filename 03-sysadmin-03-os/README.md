# Домашнее задание к занятию «3.3. Операционные системы, лекция 1»

1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой,
   это shell builtin, поэтому запустить strace непосредственно на cd не получится. Тем не менее, вы можете запустить
   strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash
   при старте. Вам нужно найти тот единственный, который относится именно к cd. Обратите внимание, что strace выдаёт
   результат своей работы в поток stderr, а не в stdout.

```shell
chdir("/tmp")
```

2. Попробуйте использовать команду file на объекты разных типов на файловой системе. Например:

```shell
vagrant@netology1:~$ file /dev/tty
/dev/tty: character special (5/0)
vagrant@netology1:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@netology1:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64
```

Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.

```shell
/usr/share/misc/magic.mgc
```

3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности
   сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение
   продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении
   потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

```shell
# PID - идентификатор процесса, пишущего в удалённый файл
# descriptor - дескриптор удалённого файла
echo "" > /proc/<PID>/fd/<descriptor>
```

4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Зомби-процессы сохраняют за собой идентификатор процесса, что может привести к исчерпанию доступных идентификаторов,
но ресурсы ОС не занимают.

5. В iovisor BCC есть утилита opensnoop:

```shell
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
```

На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для
Ubuntu 20.04.

```shell
vagrant@vagrant:~$ sudo opensnoop-bpfcc
PID    COMM               FD ERR PATH
629    irqbalance          6   0 /proc/interrupts
629    irqbalance          6   0 /proc/stat
629    irqbalance          6   0 /proc/irq/20/smp_affinity
629    irqbalance          6   0 /proc/irq/0/smp_affinity
629    irqbalance          6   0 /proc/irq/1/smp_affinity
629    irqbalance          6   0 /proc/irq/8/smp_affinity
629    irqbalance          6   0 /proc/irq/12/smp_affinity
629    irqbalance          6   0 /proc/irq/14/smp_affinity
629    irqbalance          6   0 /proc/irq/15/smp_affinity
```

6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается
   альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

```shell
Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.
```

7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:

```shell
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```

Есть ли смысл использовать в bash `&&`, если применить `set -e`?

```shell
; - выполелнение команд последовательно
&& - команда после && выполняется только если предыдущая завершилась успешно
```

```shell
set -e - останавливает выполнение скрипта при ошибке.
&& вместе с set -e, похоже, нет смысла совмещать, т.к. при возникновении ошибки дальнейшие команды и так не будут выполнены.
```

8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

```shell
-e  Exit immediately if a command exits with a non-zero status.
-u  Treat unset variables as an error when substituting.
-x  Print commands and their arguments as they are executed.
-o pipefail     the return value of a pipeline is the status of
                           the last command to exit with a non-zero status,
                           or zero if no command exited with a non-zero status

Режим прекратит выполнение скрипта в случае возникновения ошибки и выведет информацию об возникшей ошибке.
```

9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps`
   ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его
   можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

```shell
Наиболее часто встречающийся статус у процессов в системе - I

<    high-priority (not nice to other users)
N    low-priority (nice to other users)
L    has pages locked into memory (for real-time and custom IO)
s    is a session leader
l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
+    is in the foreground process group
```