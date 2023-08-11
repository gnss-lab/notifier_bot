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
        return user_id

def add_subscription(name, description):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO subscriptions (name, description) VALUES ('{name}', '{description}')")
        lsc.cursor.execute(f"SELECT id FROM subscriptions WHERE {name=}")
        result = lsc.cursor.fetchall()
        return result[-1][0]

def subscribe(sub_id, user_id, remind):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES ({sub_id}, {user_id}, {remind})")
        lsc.cursor.execute(f"SELECT id FROM users_subscriptions WHERE {sub_id=} AND {user_id=}")
        result = lsc.cursor.fetchall()
        return result[-1][0]

def add_notification(message, sub_id, initiator_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO notifications (message, sub_id, initiator_id) VALUES ('{message}', {sub_id}, {initiator_id})")
        lsc.cursor.execute(f"SELECT id FROM notifications WHERE {message=} AND {sub_id=} AND {initiator_id=}")
        result = lsc.cursor.fetchall()
        return result[-1][0]

def add_fastapi_user(username, email, hashed_password):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO fastapi_users (username, email, hashed_password) VALUES ('{username}','{email}','{hashed_password}')")

def add_monitored_service(url, message, sub_id):
    with lsc:
        lsc.cursor.execute(f"INSERT INTO monitored_services (message, sub_id, url) VALUES ('{message}', {sub_id}, '{url}')")
        lsc.cursor.execute(f"SELECT id FROM monitored_services WHERE {message=} AND {sub_id=} AND {url=}")
        result = lsc.cursor.fetchall()
        return result[-1][0]

def delete_monitored_services(ser_id):
    with lsc:
        lsc.cursor.execute(f"DELETE FROM monitored_services WHERE id={ser_id}")

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

def get_fastapi_user_by_name(username):
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

def get_monitored_services():
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services")
        result = lsc.cursor.fetchall()
        return result

def get_monitored_service_by_id(ser_id):
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services WHERE id={ser_id}")
        result = lsc.cursor.fetchone()
        return result

# INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (1, 5718232858, 1);
# INSERT INTO users (id) VALUES (5718232858);
# INSERT INTO notifications (message, sub_id) VALUES ('Test notification message!', 1);
# INSERT INTO subscriptions (name, description) VALUES ("Test subscription", "This is a test subscription created for tests");