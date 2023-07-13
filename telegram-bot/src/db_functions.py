import asyncio
import sqlite3 as sql
import threading
import os

from .settings import settings, bot
from .dto import *
from .functions import send_notification, schedule_notification

class LockableSqliteConnection(object):
    def __init__(self, path):
        self.lock = threading.Lock()
        self.connection = sql.connect(path, uri=True, check_same_thread=False)
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
              processed INT DEFAULT 0,
              created_on DATETIME NOT NULL DEFAULT (datetime('now'))
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
              created_on DATETIME NOT NULL DEFAULT (datetime('now'))
            );
            """)
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY
              
            );
            """)
# user_id = telegram_id
create_tables()

# Функция проверяющая, не пришли ли новые уведомления
async def check_db():
    while True:
        notifications = get_new_notifications()
        for notif in notifications:
            for sub in get_users_subscriptions(notif.sub_id):
                user = get_user_by_id(sub.user_id)
                if user:
                    sub_name = get_subscription_by_id(sub.sub_id).name
                    notif.message=f"{sub_name}:\n"+notif.message
                    await send_notification(user.id, notif.message, sub.remind)
                    if sub.remind:
                        schedule_notification(user.id, notif.message)
        if notifications:
            mark_notifications_as_processed(notifications)
        await asyncio.sleep(1)

def get_new_notifications():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM notifications WHERE processed = 0")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Notification(*x), result))

def mark_notifications_as_processed(notifications: list[Notification]):
    with lsc:
        for notif in notifications:
            lsc.cursor.execute(f"UPDATE notifications SET processed = 1 WHERE id = {notif.id}")

def get_users_subscriptions(sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions WHERE sub_id = {sub_id}")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: UsersSubscription(*x), result))

def get_user_by_id(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return User(*result)

def test_notification():
    with lsc:
        lsc.cursor.execute(f"UPDATE notifications SET processed = 0 WHERE id = 1")

def get_subscription_by_id(sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id = {sub_id}")
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return Subscription(*result)

def get_subscriptions_for_user(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id IN (SELECT sub_id FROM users_subscriptions WHERE user_id={user_id})")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Subscription(*x), result))

def get_not_subscriptions_for_user(user_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id NOT IN (SELECT sub_id FROM users_subscriptions WHERE user_id={user_id})")
        result = lsc.cursor.fetchall()
    return list(map(lambda x: Subscription(*x), result))

def get_one_users_subscription(user_id, sub_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions WHERE user_id = {user_id} AND sub_id={sub_id}")
        result = lsc.cursor.fetchone()
    if not result:
        return None
    return UsersSubscription(*result)

def set_notification(remind, sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"UPDATE users_subscriptions SET remind = {remind} WHERE user_id={user_id} AND sub_id={sub_id}")

def subscribe(sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id) VALUES ({sub_id}, {user_id})")

def unsubscribe(sub_id, user_id):
    with lsc:
        lsc.cursor.execute(f"DELETE FROM users_subscriptions WHERE sub_id={sub_id} AND user_id={user_id}")


# INSERT INTO users (id) VALUES (5718232858);
# INSERT INTO notifications (message, sub_id) VALUES ('Test notification message!', 1);
# INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (1, 5718232858, 1);
# INSERT INTO subscriptions (name, description) VALUES ("Test subscription", "This is a test subscription created for tests");
