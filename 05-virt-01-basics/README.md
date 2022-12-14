# Домашнее задание к занятию «1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения.»

1. Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и
   виртуализации на основе ОС.

**Полная (аппаратная) виртуализация** - гипервизор устанавливается непосредственно на оборудование.

**Паравиртуализация** - на оборудование устанавливается ОС, затем гипервизор, а гостевые ОС модифицируются таким
образом, чтобы использовать хостовую ОС через API гипервизора совместно, без нужды эмуляции аппаратной инфраструктуры.

**Виртуализация** - эмуляция аппаратной инфраструктуры для каждой гостевой ОС.

2. Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:

- физические сервера,
- паравиртуализация,
- виртуализация уровня ОС.

Условия использования:

- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения.
- Windows системы для использования бухгалтерским отделом.
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

- **Высоконагруженная база данных, чувствительная к отказу** - виртуализация уровня ОС, можно сделать кластер и
  распределять нагрузку между инстансами.
-
- **Различные web-приложения** - виртуализация уровня ОС, быстрый запуск, перезапуск, масштабирование.
-
- **Windows системы для использования бухгалтерским отделом** - физические сервера, доступ к удалённым рабочим столам
  через тонкие клиенты с помощью RDP.
-
- **Системы, выполняющие высокопроизводительные расчеты на GPU** - физические сервера, прямой доступ к GPU.

3. Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

- 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based
  инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного
  механизма создания резервных копий.

```
Платформа VMWare vSphere, выполняет все описанные требования, не требует наличия хостовой ОС. 
```

- Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов)
  инфраструктуры на базе Linux и Windows виртуальных машин.

```
KVM - бесплатное open source решение.
```

- Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.

```
Microsoft Hyper-V Server, решение от Microsoft отлично подходит для ОС Microsoft.
```

- Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.

```
Если не нужен графический интерфейс, то Docker, иначе - VirtualBox в связке с Vagrant. Разворачивание окружения легко настраивается, процесс автоматизируется.
```

4. Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления
   виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор,
   то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

```
Когда используются несколько систем управления виртуализацией, то расширяется набор используемых инструментов, сложнее обучение, проблемы с мониторингом состояния, отсутствие возможности распределить ресурсы одном приложении.
```

