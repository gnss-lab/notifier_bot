import sqlite3 as sql
import threading
import os

class LockableSqliteConnection(object):
    def __init__(self, db_folder, db_filename):
        self.lock = threading.Lock()
        db_path = os.path.join(os.path.normpath(db_folder), db_filename)
        if not os.path.isdir(db_folder):
            os.makedirs(db_folder)
        self.connection = sql.connect(db_path, uri=True, check_same_thread=False, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
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


def create_tables(lsc):
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

