# Telegram bot
## Описание
Данный телеграмм бот уведомит вас, если какой-то из сервисов системы Simurg перестанет работать.
## Установка
### Устанавливаем *git* и *python 3.10*:
- Для windows скачиваем с официального сайта
- Для ubuntu выполните следующие команды:
```bash
sudo apt update
sudo apt install git -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10-venv
```
Если вы устанавливали на ubuntu, используйте команду `python3.10` вместо `python`


### Скачиваем репозиторий
```bash
git clone https://github.com/vankad24/Simurg.git
cd Simurg
git checkout development
cd telegram-bot
```

### Создаём и активируем виртуальное окружение
- Для windows
```bash
python -m venv venv
cd venv/Scripts/
activate
cd ../..
```
- Для linux
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Устанавливаем зависимости
```bash
pip install poetry
poetry install
```

### Создаём .env файл в корневой папке проекта
```bash
echo 'tg_token=<телеграм токен бота>' > .env
echo 'FAST_API_SECRET=<секретный ключ>' >> .env
```
- Для генерации секретного ключа можно использовать `openssl rand -hex 32`

## Запуск
Запуск производится из корневой папки проекта.
```bash
cd ..
python main_bot.py
```

## Использование
Как пользоваться смотри [здесь](/README.md#Использование)

## Логи
Логи находятся в папке `telegram_bot/logs`. Изменить настройки логирования можно в файле `telegram_bot/src/logger.py` 
