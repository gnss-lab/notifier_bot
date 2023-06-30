import asyncio
import sqlite3 as sql
import threading
import time
import uuid
from .settings import settings, bot
# from messages import MENU_STEP


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
def setup_lsc():
    with lsc:
        lsc.cursor.execute(f"create table if not exists commands (id INTEGER PRIMARY KEY, text text, read int DEFAULT 0)")
setup_lsc()

# Функция для проверки внешних команд
async def check_db():
    while True:
        commands:list = get_unread_commands()
        for command in commands:
            cid, text = command
            for uid in settings.subscribers:
                await bot.send_message(uid, text)
            mark_command_as_read(cid)
        await asyncio.sleep(1)

def get_unread_commands():
    with lsc:
        lsc.cursor.execute(f"SELECT id, text FROM commands WHERE read = 0")
        result = lsc.cursor.fetchall()
    return result

def mark_command_as_read(command_id):
    with lsc:
        lsc.cursor.execute(f"UPDATE commands SET read = 1 WHERE id = {command_id}")


# Фукнция, генерирующая айди
def generate_id() -> str:
    return str(uuid.uuid4())


# Фукнция, возвращающая шаг, на котором сейчас находится пользователь
def check_step(user_id: str) -> str:
    with lsc:
        lsc.cursor.execute(f"SELECT step FROM users WHERE id = '{user_id}'")
        result = lsc.cursor.fetchall()[0][0]
    return result


# Фукнция, меняющая шаг, на котором сейчас находится пользователь
def insert_step(n: str, user_id: str) -> None:
    with lsc:
        lsc.cursor.execute(f"UPDATE users SET step = '{n}' WHERE id = '{user_id}'")


# Фукнция, проверяющая есть ли пользователь в базе данных
def user_exist(user_id: str) -> bool:
    with lsc:
        lsc.cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        exist = lsc.cursor.fetchone()
    return exist


# Фукнция, создающая пользователя в базе данных
# def create_user(user_id: str, tg_username: str) -> None:
#     with lsc:
#         now = int(time.time())
#         lsc.cursor.execute(
#             f"INSERT INTO users (id, step, tg_username, join_time) VALUES('{user_id}', '{MENU_STEP}', '{tg_username}', '{now}')"
#         )


# with lsc:
#     lsc.cursor.execute(f"INSERT INTO commands (text) VALUES ('hello test 24')")
