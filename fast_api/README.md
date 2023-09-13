# FastApi service
## Описание
API сервис для управления ботом и рассылки уведомлений подписчикам
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
cd fast_api
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

## Запуск
Запуск производится из корневой папки проекта.
```bash
cd ..
python main_api.py
```
 
После чего в браузере откройте
*http://127.0.0.1:8000/*

## Использование
Как пользоваться смотри [здесь](/README.md#Использование)

## Дополнительно
### Логи
Логи находятся в папке `fast_api/logs`. Изменить настройки логирования можно в файле `fast_api/src/logger.py` 

### Тесты
Запускать тесты необходимо из папки `fast_api`:
```bash
pytest --cov --cov-report html:cov_html
```
После выполнения команды создастся папка `cov_html`. В ней можно открыть файл `index.html` и наглядно посмотреть покрытие тестами. 

Для запуска конкретного теста необходимо использовать команду:
```bash
pytest tests/test_main.py::test_sometest
```