import sqlite3 as sql
import threading
import os

from .models import UserInDB


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

DB_FILENAME = "main_bot.db"
DB_FOLDER = "../telegram-bot/databases"
DB_PATH = os.path.join(os.path.normpath(DB_FOLDER), DB_FILENAME)
if not os.path.isdir(DB_FOLDER):
    os.makedirs(DB_FOLDER)
lsc = LockableSqliteConnection(DB_PATH)

def add_user(user_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users (id) VALUES ({user_id})")

def add_subscription(name, description):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO subscriptions (name, description) VALUES ('{name}', '{description}')")

def subscribe(sub_id, user_id, remind):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES ({sub_id}, {user_id}, {remind})")

def add_notification(message, sub_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO notifications (message, sub_id) VALUES ('{message}', {sub_id})")

def get_users():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users")
        result = lsc.cursor.fetchall()
        return result

def get_subscriptions():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions")
        result = lsc.cursor.fetchall()
        return result

def get_users_subscriptions():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions")
        result = lsc.cursor.fetchall()
        return result

def get_notifications():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM notifications")
        result = lsc.cursor.fetchall()
        return result

def get_user_by_name(username):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM fastapi_users WHERE username = '{username}'")
        r = lsc.cursor.fetchone()
    if not r:
        return None
    return UserInDB(id=r[0],email=r[1],username=r[2],hashed_password=r[3])

def get_subscription_id_by_name(sub_name):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE name = '{sub_name}' LIMIT 1")
        r = lsc.cursor.fetchone()
    if not r:
        return None
    return r[0]


def add_fastapi_user(username, email, hashed_password):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO fastapi_users (username, email, hashed_password) VALUES ('{username}','{email}','{hashed_password}')")

# INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (1, 5718232858, 1);
# INSERT INTO users (id) VALUES (5718232858);
# INSERT INTO notifications (message, sub_id) VALUES ('Test notification message!', 1);
# INSERT INTO subscriptions (name, description) VALUES ("Test subscription", "This is a test subscription created for tests");