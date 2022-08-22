# Домашнее задание к занятию «2.4. Инструменты Git»

Для выполнения заданий в этом разделе давайте склонируем репозиторий с исходным кодом терраформа https://github.com/hashicorp/terraform

### Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.

```shell
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md
```

### Какому тегу соответствует коммит 85024d3?
```shell
v0.12.23
```

### Сколько родителей у коммита b8d720? Напишите их хеши.
```shell
2 коммита

56cd7859e05c36c06b56d013b55a252d0bb7e158
9ea88f22fc6269854151c571162c5bcf958bee2b
```

### Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.
```shell
b14b74c493 [Website] vmc provider links
3f235065b9 Update CHANGELOG.md
6ae64e247b registry: Fix panic when server is unreachable
5c619ca1ba website: Remove links to the getting started guide's old location
06275647e2 Update CHANGELOG.md
d5f9411f51 command: Fix bug when using terraform login on Windows
4b6d06cc5d Update CHANGELOG.md
dd01a35078 Update CHANGELOG.md
225466bc3e Cleanup after v0.12.23 release
```

### Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).
```shell
commit 8c928e83589d90a031f811fae52a81be7153e82f
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Thu Apr 2 18:04:39 2020 -0700
```

### Найдите все коммиты в которых была изменена функция globalPluginDirs.
```shell
78b1220558 Remove config.go and update things using its aliases
52dbf94834 keep .terraform.d/plugins for discovery
41ab0aef7a Add missing OS_ARCH dir to global plugin paths
66ebff90cd move some more plugin search path logic to command
8364383c35 Push plugin discovery down into command package
```

### Кто автор функции synchronizedWriters?
```shell
Martin Atkins

commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Wed May 3 16:25:41 2017 -0700
```