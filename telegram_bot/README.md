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

### Добавляем токен
Создайте файл **.env** в корневой папке проекта со следующим содержанием:
```env
tg_token=<your_telegram_bot_token>
```
Вместо `<your_telegram_bot_token>` введите токен вашего телеграм бота.

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
