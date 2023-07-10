import asyncio
import sqlite3 as sql
import threading

import schedule

from .settings import settings, bot
from .dto import *
from .functions import send_notification, schedule_notification

class LockableSqliteConnection(object):
    def __init__(self, db):
        self.lock = threading.Lock()
        self.connection = sql.connect(db, uri=True, check_same_thread=False)
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


db_path = r".\databases\main_bot.db"
lsc = LockableSqliteConnection(db_path)
def create_tables():
    with lsc:
        lsc.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
              id INTEGER PRIMARY KEY,
              message TEXT,
              sub_id INTEGER,
              processed INT DEFAULT 0
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
              remind INT
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
            for subs in get_users_subscriptions(notif.sub_id):
                user = get_user_by_id(subs.user_id)
                if user:
                    await send_notification(user.id, notif.message, subs.remind)
                    if subs.remind:
                        schedule_notification(user.id, notif.message)
        if notifications:
            mark_notifications_as_processed(notifications)
        schedule.run_pending()
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

def test_subscription():
    with lsc:
        lsc.cursor.execute(f"UPDATE notifications SET processed = 0 WHERE id = 1")

# INSERT INTO users (id) VALUES (5718232858);
# INSERT INTO notifications (message, sub_id) VALUES ('Test notification message!', 1);
# INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (1, 5718232858, 1);