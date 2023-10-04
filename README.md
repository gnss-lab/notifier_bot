## Инструкция по запуску в docker
### Устанавливаем пакеты
```bash
sudo apt update && sudo apt install git docker.io -y
```
### Добавляем себя в группу 'docker', чтобы не использовать **sudo** (требуется перезагрузка)
```bash
sudo usermod -aG docker $USER
```
### Скачиваем репозиторий
```bash
git clone https://github.com/vankad24/Simurg.git
cd Simurg
git checkout development
```
### Создаём .env файл
```bash
echo 'tg_token=<телеграм токен бота>' > .env
echo 'FAST_API_SECRET=<секретный ключ>' >> .env
```
- Для генерации секретного ключа можно использовать `openssl rand -hex 32`
### Создаём образ docker
```bash
docker build -t simurg_bot .
```
### Запуск docker контейнера на порту 8000 и монтированием папки 'databases'
```bash
docker run -p 8000:8000 -v "$(pwd)"/databases/:/app/databases/ -ti -d simurg_bot
```
### После чего FastAPI должен быть доступен по адресу *http://127.0.0.1:8000/*

## Инструкция по запуску вручную
- [Telegram bot](/telegram_bot/README.md)
- [FastApi service](/fast_api/README.md)

## Использование
1. Зарегистрируйтесь или залогиньтесь в API.
2. Зайдите в телеграм и вызовете команду `/start`. Вы можете добавить свой телеграм id вручную, используя `/user/add`. Вы можете узнать свой id телеграм с помощью команды бота `/id`.
3. Добавьте тему, на которую люди будут подписываться `/subscription/add`.
4. Теперь любой желающий может подписаться на вашу тему. Для этого используйте команду бота `/subscribe` или аналогичную в API.
5. Для отправки уведомления вручную, используйте команду `/send_notification_by_id` или `/send_notification_by_name`. Сообщение придёт всем, кто подписан на тему (см. пункт 3).
6. Используйте `/monitored_service/add`, если хотете, чтобы бот пинговал конкретный адрес. В случае, если достучаться по адресу не получается, бот отправит всем подписчикам темы сообщение `error_message`, которое вы передали в `/monitored_service/add`. Периодичность устанавливается с помощью параметра `crontab`. Если вам нужно изменить периодичность, используйте `/monitored_service/update` и передайте новое значение `crontab`. Удалить пингование вы можете с помощью `/monitored_service/delete`.
7. Отписаться можно с помощью команды `/unsubscribe` или кнопкой `Отписаться` в сообщении бота.
