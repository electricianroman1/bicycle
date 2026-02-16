# Установка MongoDB и MongoDB Compass на Ubuntu 25.04

## Сведения о системе

### Аппаратное обеспечение
| Параметр             | Значение                 |
|----------------------|--------------------------|
| Модель устройства    | innotek GmbH VirtualBox  |
| Оперативная память   | 9.1 GiB                  |
| Процессор            | Intel® Core™ i5-9400F × 4|
| Графика              | Программный рендеринг    |
| Ёмкость диска        | 111.0 GB                 |

### Программное обеспечение
| Параметр        | Значение                     |
|-----------------|------------------------------|
| Версия прошивки | VirtualBox                   |
| Название ОС     | Ubuntu 25.04                 |
| Сборка ОС       | (не задано)                  |
| Тип ОС          | 64-разрядная                 |
| Версия GNOME    | 48                           |
| Оконная система | Wayland                      |
| Версия ядра     | Linux 6.14.0-28-generic      |

### Отчёт
| Параметр     | Значение                 |
|--------------|--------------------------|
| Сформирован  | 2025-08-20 23:29:53      |

## Процесс установки

### 1. Подготовка системы

> **Внимание**: В ОС Ubuntu sudo включена по умолчанию, а в Debian, если в процессе установки не был выбран соответствующий пакет.

Переход в режим root:
```bash
sudo -i
```
> Команда `-i` или `--login`: Запускает оболочку от имени целевого пользователя, как если бы пользователь вошел в систему.

> **Внимание**: Введённый пароль не видно. После ввода нажмите клавишу RETURN.

Установка необходимых инструментов:
```bash
apt install curl  # version 8.12.1-3ubuntu1
```

> После выполнения команды отображается процесс установки:
> ```
> Установка: curl
> Сводка: Обновление: 0, Установка: 1, Удаление: 0, Пропуск обновления: 0
> Объём загрузки: 258 kB
> Требуемое пространство: 503 kB / 92,1 GB доступно
> ```

### 2. Добавление репозитория MongoDB

> Чтобы установить актуальный пакет MongoDB, необходимо добавить его в список репозиториев. Но предварительно следует импортировать открытый ключ для MongoDB в вашу систему.

Импорт GPG-ключа:
```bash
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
```

> **Зачем это нужно**: Эта команда загружает и сохраняет открытый ключ MongoDB в вашей системе. Ключ необходим для проверки подлинности пакетов MongoDB при установке, что гарантирует их безопасность и целостность. Без этого шага система не сможет проверить, что пакеты получены из официального источника и не были изменены.

Добавление репозитория:
```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

> В результате создается файл с именем `mongodb-org-7.0.list`. Для просмотра его содержимого:

```bash
cd /etc/apt/sources.list.d/  # переходим в директорию
cat mongodb-org-7.0.list     # просматриваем содержимое
cd /  # выходим из директории
```

> Ожидаемое содержимое файла:
> ```
> deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse
> ```

Обновление списка пакетов:
```bash
sudo apt update
```

> В процессе обновления в выводе должен появиться репозиторий MongoDB:
> ```
> Пол:24 https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 InRelease [3 005 B]
> ```

### 3. Установка MongoDB

Установка пакета MongoDB:
```bash
sudo apt install mongodb-org
```

> Процесс установки включает загрузку и установку нескольких компонентов:
> ```
> Установка зависимостей:
> mongodb-database-tools mongodb-org-database-tools-extra mongodb-org-shell
> mongodb-mongosh mongodb-org-mongos mongodb-org-tools
> mongodb-org-database mongodb-org-server
> 
> Сводка:
> Обновление: 0, Установка: 9, Удаление: 0, Пропуск обновления: 19
> Объём загрузки: 179 MB
> Требуемое пространство: 602 MB / 92,1 GB доступно
> ```

> После подтверждения установки (ввод `y`) происходит загрузка и установка пакетов.

Проверка версии:
```bash
mongod --version
```

Ожидаемый вывод:
```
db version v7.0.23
Build Info: {
    "version": "7.0.23",
    "gitVersion": "78d6d71385be23831b5971993af60bcafed785bc",
    "openSSLVersion": "OpenSSL 3.4.1 11 Feb 2025",
    "modules": [],
    "allocator": "tcmalloc",
    "environment": {
        "distmod": "ubuntu2204",
        "distarch": "x86_64",
        "target_arch": "x86_64"
    }
}
```

### 4. Запуск и настройка службы

> При установке служба MongoDB по умолчанию будет отключена.

Запуск службы MongoDB:
```bash
sudo systemctl start mongod
```

Проверка статуса:
```bash
sudo systemctl status mongod
```

> Ожидаемый вывод:
> ```
> ● mongod.service - MongoDB Database Server
> Loaded: loaded (/usr/lib/systemd/system/mongod.service; disabled; preset: enabled)
> Active: active (running) since Mon 2025-08-18 20:37:43 MSK; 15s ago
> Docs: https://docs.mongodb.org/manual
> Main PID: 8837 (mongod)
> Memory: 76.9M (peak: 77.2M)
> CPU: 723ms
> CGroup: /system.slice/mongod.service
> └─8837 /usr/bin/mongod --config /etc/mongod.conf
> ```

Проверка используемого порта:
```bash
sudo ss -pnltu | grep 27017
```

> Ожидаемый вывод:
> ```
> tcp LISTEN 0 4096 127.0.0.1:27017 0.0.0.0:* users:(("mongod",pid=8837,fd=14))
> ```

### 5. Установка MongoDB Compass

> Мы рассматриваем установку через загрузку подготовленного пакета на сайте и используем для этого wget и dpkg. Если wget не установлен, тогда скачиваем его.

Скачивание и установка MongoDB Compass:
```bash
apt install wget -y && wget https://downloads.mongodb.com/compass/mongodb-compass_1.40.4_amd64.deb
```

> Если wget уже установлен:
> ```
> Уже установлен пакет wget самой новой версии (1.24.5-2ubuntu1).
> wget помечен как установленный вручную.
> ```

Установка скачанного пакета:
```bash
dpkg -i mongodb-compass_1.40.4_amd64.deb
```

> Процесс установки:
> ```
> Выбор ранее не выбранного пакета mongodb-compass.
> Настраивается пакет mongodb-compass (1.40.4) ...
> Обрабатываются триггеры для gnome-menus (3.36.0-1.1ubuntu3) ...
> Обрабатываются триггеры для desktop-file-utils (0.28-1) ...
> ```

## Заключение

> **Поздравляю! MongoDB и MongoDB Compass установлены!**

Установка MongoDB и MongoDB Compass успешно завершена. Оба компонента готовы к использованию.

**Примечание:** Сервис MongoDB по умолчанию отключен после установки. Для автоматического запуска при загрузке системы выполните:
```bash
sudo systemctl enable mongod
```

## Статус
✅ Установка завершена успешно
