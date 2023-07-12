# Telegram bot
## Описание
Данный телеграмм бот уведомит вас, если какой-то из сервисов системы Simurg перестанет работать.
## Установка
Устанавливаем *git* и *python 3.10*:
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


Скачиваем репозиторий
```bash
git clone https://github.com/vankad24/Simurg.git
cd Simurg
git checkout development
cd telegram-bot
```

Создаём виртуальное окружение
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

Устанавливаем зависимости
```bash
pip install poetry
poetry install
```

Создайте файл **.env** со следующим содержанием:
```env
tg_token=your_telegram_bot_token
```

## Запуск 
```bash
python main.py
```
## Функции
- [x] Мониторинг БД на новые сообщения
- [x] Оповещение подписанных пользователей
- [x] Повтор напоминания, пока не будет нажата кнопка "Ок"
- [x] Команда для просмотра своих подписок
- [ ] Команда для просмотра других подписок
- [ ] Команда для подписки/отписки, включение/выключение уведомлений
- [ ] Команды для администраторов
- [ ] Переход к реализации API