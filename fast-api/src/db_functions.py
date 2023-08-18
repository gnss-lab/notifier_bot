import sqlite3 as sql
import threading
import os

from .models import UserInDB
from loguru import logger

class LockableSqliteConnection(object):
    def __init__(self, db):
        self.lock = threading.Lock()
        self.connection = sql.connect(db, uri=True, check_same_thread=False, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
        self.cursor = None
        logger.info("create LockableSqliteConnection object")

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
    logger.debug(f"{user_id=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users (id) VALUES (?)", (user_id,))
        return user_id

def add_subscription(name, description):
    logger.debug(f"{name=} {description=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO subscriptions (name, description) VALUES (?, ?)", (name,description))
        lsc.cursor.execute(f"SELECT MAX(id) FROM subscriptions")
        result = lsc.cursor.fetchone()
        return result[0]

def subscribe(sub_id, user_id, remind):
    logger.debug(f"{sub_id=} {user_id=} {remind=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (?, ?, ?)",(sub_id,user_id,remind))
        lsc.cursor.execute(f"SELECT MAX(id) FROM users_subscriptions")
        result = lsc.cursor.fetchone()
        return result[0]

def add_notification(message, sub_id, initiator_id):
    logger.debug(f"{message=} {sub_id=} {initiator_id=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO notifications (message, sub_id, initiator_id) VALUES (?, ?, ?)",(message,sub_id, initiator_id))
        lsc.cursor.execute(f"SELECT MAX(id) FROM notifications")
        result = lsc.cursor.fetchone()
        return result[0]

def add_fastapi_user(username, email, hashed_password):
    logger.debug(f"{username=} {email=} {hashed_password=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO fastapi_users (username, email, hashed_password) VALUES (?,?,?)", (username,email,hashed_password))

def add_monitored_service(url, message, sub_id, initiator_id, cron_time):
    logger.debug(f"{url=} {message=} {sub_id=} {initiator_id=} {cron_time=}")
    with lsc:
        lsc.cursor.execute(f"INSERT INTO monitored_services (message, sub_id, url, initiator_id, cron_time) VALUES (?,?,?,?,?)", (message, sub_id, url, initiator_id,cron_time))
        lsc.cursor.execute(f"SELECT MAX(id) FROM monitored_services")
        result = lsc.cursor.fetchone()
        return result[0]

def delete_monitored_service(ser_id):
    logger.debug(f"{ser_id=}")
    with lsc:
        lsc.cursor.execute(f"UPDATE monitored_services SET need_delete = 1 WHERE id = ?", (ser_id,))

def update_monitored_service(ser_id, cron_time):
    logger.debug(f"{ser_id=} {cron_time=}")
    with lsc:
        lsc.cursor.execute(f"UPDATE monitored_services SET cron_time = ?, processed = 0 WHERE id = ?", (cron_time, ser_id))

def get_users():
    logger.debug(f"")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users")
        result = lsc.cursor.fetchall()
        return result

def get_subscriptions():
    logger.debug(f"")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions")
        result = lsc.cursor.fetchall()
        return result

def get_users_subscriptions():
    logger.debug(f"")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM users_subscriptions")
        result = lsc.cursor.fetchall()
        return result

def get_notifications():
    logger.debug(f"")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM notifications")
        result = lsc.cursor.fetchall()
        return result

def get_fastapi_user_by_name(username):
    logger.debug(f"{username=}")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM fastapi_users WHERE username = ? LIMIT 1", (username,))
        r = lsc.cursor.fetchone()
    if not r:
        return None
    return UserInDB(id=r[0],email=r[1],username=r[2],hashed_password=r[3])

def get_subscription_id_by_name(sub_name):
    logger.debug(f"{sub_name=}")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE name =? LIMIT 1", (sub_name,))
        r = lsc.cursor.fetchone()
    if not r:
        return None
    return r[0]

def get_monitored_services():
    logger.debug(f"")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services")
        result = lsc.cursor.fetchall()
        return result

def get_monitored_service_by_id(ser_id):
    logger.debug(f"{ser_id=}")
    with lsc:
        lsc.cursor.execute(f"SELECT * FROM monitored_services WHERE id=?", (ser_id,))
        result = lsc.cursor.fetchone()
        return result
