# Cryptonite — Secure E2E Encryptor (DEMO)

**Cryptonite** — это кроссплатформенный инструмент командной строки для сквозного шифрования (end-to-end encryption).  
Он использует гибридную криптографию: RSA-OAEP + AES-256-GCM.  

Проще говоря:  
- RSA отвечает за защиту ключей.  
- AES-256-GCM — за быстрое и надежное шифрование данных.  

Проект создан в рамках **Akin Foundation** для защиты текстов и файлов от несанкционированного доступа.  

---

## Возможности

- Генерация RSA-ключей (2048 / 4096 бит).  
- Поддержка защищенных паролем приватных ключей.  
- Шифрование текста прямо из командной строки.  
- Шифрование файлов любого размера.  
- Расшифровка в консоль или в файл.  
- Возможность ввода приватного ключа вручную (если файл недоступен).  
- Работа на Windows, Linux, macOS.  

---

## Установка (MacOS, Linux, Windows)

# 1. macOS
   Перед установкой убедитесь, что Python уже установлен на вашем устройстве. Для этого откройте терминал и выполните команду:
   ```bash
   python3 --version
   ```

   Если Python установлен, вы увидите версию. Если Python не установлен, вам нужно будет установить его с помощью Homebrew. Для этого выполните следующие шаги:

   1) Установите Homebrew (если он еще не установлен):

      [Перейдите на официальный сайт Homebrew](https://brew.sh/)

   2) Установите Python с помощью Homebrew:
   ```bash
   brew install python
   ```

   3) Убедитесь, что Python и pip установлены правильно, выполнив:
   ```bash
   python --version
   ```

   4) Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

# 2. Linux (Debian & Ubuntu)
   1) Обновите списки пакетов и установите необходимые зависимости:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

   2) Убедитесь, что Python и pip установлены правильно, выполнив:
   ```bash
   python3 --version
   ```

   3) Установите зависимости с помощью `pip`:
   ```bash
   pip3 install -r requirements.txt
   ```

# 2.1. Linux (Fedora)
   1) Установите Python и pip:
   ```bash
   sudo dnf install python3 python3-pip
   ```

   2) Убедитесь, что Python и pip установлены правильно, выполнив:
   ```bash
   python3 --version
   ```
   
   3) Установите зависимости:
   ```bash
   pip3 install -r requirements.txt
   ```

# 3. Windows
   1) Установите [Python](python.org) с официального сайта

   2) Убедитесь, что Python и pip установлены правильно, выполнив:
   ```bash
   python --version
   ```
   
   3) Откройте командную строку или PowerShell и выполните команду:
   ```bash
   pip install -r requirements.txt
   ```

---

## Использование

Показать все команды:
```bash
python main.py --help
```

### 1. Генерация ключей
```bash
python main.py genkeys --bits 4096 --protect
```
- `--bits` — размер ключа (минимум 2048, рекомендуется 4096).  
- `--protect` — запрашивает пароль и шифрует приватный ключ.  
- По умолчанию сохраняет ключи как `private_key.pem` и `public_key.pem`.  

---

### 2. Шифрование текста
```bash
python main.py encrypt --text "Akin Foundation" --pub public_key.pem --out message.enc
```
- `--text` — текст для шифрования.  
- `--out` — имя файла для результата (по умолчанию message.enc).  

---

### 3. Шифрование файла
```bash
python main.py encrypt --in secret.bin --pub public_key.pem --out message.enc
```

---

### 4. Дешифрование
```bash
python main.py decrypt --in message.enc --priv private_key.pem --protect --out decrypted.bin
```
- `--protect` — запросит пароль, если ключ защищен.  
- `--out` — файл для расшифрованных данных (если не указать — выводит в консоль).  

---

## Важные советы по безопасности

- Никогда не публикуйте приватные ключи в открытом доступе.  
- Храните `private_key.pem` только в защищенных местах (например, в менеджере секретов).  
- Используйте пароль (`--protect`) для шифрования приватного ключа.  
- Проверяйте целостность файлов и не используйте ключи на непроверенных машинах.  

---

## Структура проекта

```
Cryptonite/
│── crypto_utils/        # Вспомогательные утилиты (RSA, AES, сериализация)
│── assets/              # Инициализация CLI-интерфейса
│── commands/            # Логика CLI-команд (genkeys, encrypt, decrypt)
│── main.py              # Точка входа (CLI-интерфейс)
│── requirements.txt     # Зависимости
│── README.md            # Документация
│── LICENSE              # Лицензия
```
