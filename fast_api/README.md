# FastApi service
## Описание
API сервис для управления ботом и рассылки уведомлений подписчикам
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
cd fast_api
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

## Запуск
*_Сначала нужно запустить бота!_*
```bash
uvicorn main:app --reload --host 0.0.0.0
```
 
После чего в браузере откройте
*http://127.0.0.1:8000/*


Где находятся логи

Как запускать проект и тесты

