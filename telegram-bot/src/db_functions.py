import asyncio
import sqlite3 as sql
import threading
import os

import requests
from apscheduler.triggers.cron import CronTrigger

from .settings import settings, bot, scheduler
from .dto import *
from .functions import send_notification, schedule_notification

class LockableSqliteConnection(object):
    def __init__(self, path):
        self.lock = threading.Lock()
        self.connection = sql.connect(path, uri=True, check_same_thread=False, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
        self.cursor = None

    def __enter__(self):
        self.lock.acquire()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        self.lock.release()

DB_FILENAME = "main_bot.db"
DB_FOLDER = "databases"
DB_PATH = os.path.join(os.path.normpath(DB_FOLDER), DB_FILENAME)
if not os.path.isdir(DB_FOLDER):
    os.makedirs(DB_FOLDER)
lsc = LockableSqliteConnection(DB_PATH)

def create_tables():
    with lsc:
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
              id INTEGER PRIMARY KEY,
              message TEXT,
              sub_id INTEGER,
              initiator_id INTEGER,
              processed INT DEFAULT 0,
              created_on TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime'))
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
              id INTEGER PRIMARY KEY,
              name TEXT,
              description TEXT
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_subscriptions (
              id INTEGER PRIMARY KEY,
              sub_id INTEGER,
              user_id INTEGER,
              remind INT DEFAULT 0,
              created_on TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime'))
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY
              
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fastapi_users (
              id INTEGER PRIMARY KEY,
              email TEXT,
              username TEXT,
              hashed_password TEXT
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS monitored_services (
              id INTEGER PRIMARY KEY,
              url TEXT,
              message TEXT,
              sub_id INTEGER,
              initiator_id INTEGER,
              cron_time TEXT,
              created_on TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
              processed INTEGER DEFAULT 0,
              need_delete INTEGER DEFAULT 0
            );
            """)

create_tables()

# Функция, проверяющая, не пришли ли новые уведомления
async def check_db():
    loop_repeat_delay = 1
    messages_limit = 10
    per_seconds_limit = 1
    counter = 0

    for service in get_all_services():
        if service.need_delete:
            delete_monitored_service(service.id)
        if not service.processed:
            mark_service_as_processed(service.id)
        schedule_service_checking(service)

    while True:
        notifications = get_new_notifications()
        for notif in notifications:
            if counter > messages_limit:
                counter = 0
                await asyncio.sleep(per_seconds_limit)
            counter+=1

            for sub in get_users_subscriptions(notif.sub_id):
                user = get_user_by_id(sub.user_id)
                if user:
                    sub_name = get_subscription_by_id(sub.sub_id).name
                    notif.message=f"{sub_name}:\n{notif.message}\n\n{notif.created_on}"
                    await send_notification(user.id, notif.message, sub.remind)
                    if sub.remind:
                        schedule_notification(user.id, notif.message)
        if notifications:
            mark_notifications_as_processed(notifications)

        for service in get_deleted_services():
            delete_monitored_service(service.id)

        for service in get_new_services():
            mark_service_as_processed(service.id)
            schedule_service_checking(service)

        await asyncio.sleep(loop_repeat_delay)


def check_service(service):
    try:
        response = requests.get(service.url)
        failed = response.status_code >= 400
    except:
        failed = True

    if failed:
        add_notification(service.message, service.sub_id, service.initiator_id)
    else:
        print("ok")

def schedule_service_checking(service):
    scheduler.add_job(check_service, CronTrigger.from_crontab(service.cron_time), id=str(service.id), args=(service,), replace_existing=True)
    # scheduler.get_job(str(ser_id), 'default')

def get_new_notifications():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM notifications WHERE processed = 0")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Notification(*x), result))

def get_all_services():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: MonitoredServices(*x), result))

def get_new_services():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services WHERE processed = 0")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: MonitoredServices(*x), result))

def get_deleted_services():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services WHERE need_delete = 1")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: MonitoredServices(*x), result))

def delete_monitored_service(ser_id):
    with lsc:
        lsc.cursor.execute(f"DELETE FROM monitored_services WHERE id=?", (ser_id,))
    job = scheduler.get_job(str(ser_id), 'default')
    if job:
        job.remove()

def mark_service_as_processed(ser_id):
    with lsc:
        lsc.cursor.execute(f"UPDATE monitored_services SET processed = 1 WHERE id = ?", (ser_id,))

def mark_notifications_as_processed(notifications: list[Notification]):
    with lsc:
        for notif in notifications:
            lsc.cursor.execute(f"UPDATE notifications SET processed = 1 WHERE id = ?", (notif.id,))

def get_users_subscriptions(sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions WHERE sub_id = ?", (sub_id,))
        result = lsc.cursor.fetchall()
    return list(map(lambda x: UsersSubscription(*x), result))

def get_user_by_id(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users WHERE id = ?", (user_id,))
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return User(*result)

def get_subscription_by_id(sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id = ?", (sub_id,))
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return Subscription(*result)

def get_subscriptions_for_user(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id IN (SELECT sub_id FROM users_subscriptions WHERE user_id= ?)", (user_id,))
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Subscription(*x), result))

def get_not_subscriptions_for_user(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id NOT IN (SELECT sub_id FROM users_subscriptions WHERE user_id=?)", (user_id,))
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Subscription(*x), result))

def get_one_users_subscription(user_id, sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions WHERE user_id = ? AND sub_id=?", (user_id,sub_id))
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return UsersSubscription(*result)

def set_notification(remind, sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"UPDATE users_subscriptions SET remind = ? WHERE user_id= ? AND sub_id=?", (remind,user_id,sub_id))

def subscribe(sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id) VALUES (?, ?)",(sub_id,user_id))

def unsubscribe(sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"DELETE FROM users_subscriptions WHERE sub_id=? AND user_id=?", (sub_id, user_id))

def add_telegram_user(user_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users (id) VALUES (?)",(user_id,))

def telegram_user_exists(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT id FROM users WHERE id=? LIMIT 1",(user_id,))
        result = lsc.cursor.fetchone()
    if not result:
        return False
    return True

def add_notification(message, sub_id, initiator_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO notifications (message, sub_id, initiator_id) VALUES (?, ?, ?)",(message,sub_id,initiator_id))