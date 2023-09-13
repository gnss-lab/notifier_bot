from .models import UserInDB
from loguru import logger
from lib.db_create import create_tables

class DB:
    def __init__(self, lsc):
        self.lsc = None
        self.set_lsc(lsc)

    def set_lsc(self, lsc):
        if self.lsc:
            self.lsc.connection.close()
        create_tables(lsc)
        self.lsc = lsc

    def add_user(self, user_id):
        logger.debug(f"{user_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO users (id) VALUES (?)", (user_id,))
            return user_id
    
    def get_telegram_user(self, user_id):
        logger.debug(f"{user_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT id FROM users WHERE id = ?", (user_id,))
            result = self.lsc.cursor.fetchone()
            if not result:
                return None
            return result[0]
    
    def add_subscription(self, name, description):
        logger.debug(f"{name=} {description=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO subscriptions (name, description) VALUES (?, ?)", (name,description))
            self.lsc.cursor.execute(f"SELECT MAX(id) FROM subscriptions")
            result = self.lsc.cursor.fetchone()
            return result[0]
    
    def subscribe(self, sub_id, user_id, remind):
        logger.debug(f"{sub_id=} {user_id=} {remind=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO users_subscriptions (sub_id, user_id, remind) VALUES (?, ?, ?)",(sub_id,user_id,remind))
            self.lsc.cursor.execute(f"SELECT MAX(id) FROM users_subscriptions")
            result = self.lsc.cursor.fetchone()
            return result[0]

    def unsubscribe(self, sub_id, user_id):
        logger.debug(f"{sub_id=} {user_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"DELETE FROM users_subscriptions WHERE sub_id=? AND user_id=?",(sub_id,user_id,))
    
    def add_notification(self, message, sub_id, initiator_id):
        logger.debug(f"{message=} {sub_id=} {initiator_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO notifications (message, sub_id, initiator_id) VALUES (?, ?, ?)",(message,sub_id, initiator_id))
            self.lsc.cursor.execute(f"SELECT MAX(id) FROM notifications")
            result = self.lsc.cursor.fetchone()
            return result[0]
    
    def add_fastapi_user(self, username, email, hashed_password):
        logger.debug(f"{username=} {email=} {hashed_password=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO fastapi_users (username, email, hashed_password) VALUES (?,?,?)", (username,email,hashed_password))
    
    def add_monitored_service(self, url, message, sub_id, initiator_id, cron_time):
        logger.debug(f"{url=} {message=} {sub_id=} {initiator_id=} {cron_time=}")
        with self.lsc:
            self.lsc.cursor.execute(f"INSERT INTO monitored_services (message, sub_id, url, initiator_id, cron_time) VALUES (?,?,?,?,?)", (message, sub_id, url, initiator_id,cron_time))
            self.lsc.cursor.execute(f"SELECT MAX(id) FROM monitored_services")
            result = self.lsc.cursor.fetchone()
            return result[0]
    
    def delete_monitored_service(self, ser_id):
        logger.debug(f"{ser_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"UPDATE monitored_services SET need_delete = 1 WHERE id = ?", (ser_id,))
    
    def update_monitored_service(self, ser_id, cron_time):
        logger.debug(f"{ser_id=} {cron_time=}")
        with self.lsc:
            self.lsc.cursor.execute(f"UPDATE monitored_services SET cron_time = ?, processed = 0 WHERE id = ?", (cron_time, ser_id))
    
    def get_users(self, ):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM users")
            result = self.lsc.cursor.fetchall()
            return result
    
    def get_subscriptions(self, ):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM subscriptions")
            result = self.lsc.cursor.fetchall()
            return result

    def get_subscription_by_id(self, sub_id):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE id = ?", (sub_id,))
            r = self.lsc.cursor.fetchone()
            if not r:
                return None
            return r
    
    def get_users_subscriptions(self, ):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM users_subscriptions")
            result = self.lsc.cursor.fetchall()
            return result
    
    def get_notifications(self, ):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM notifications")
            result = self.lsc.cursor.fetchall()
            return result
    
    def get_fastapi_user_by_name(self, username):
        logger.debug(f"{username=}")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM fastapi_users WHERE username = ? LIMIT 1", (username,))
            r = self.lsc.cursor.fetchone()
        if not r:
            return None
        return UserInDB(id=r[0],email=r[1],username=r[2],hashed_password=r[3])
    
    def get_subscription_id_by_name(self, sub_name):
        logger.debug(f"{sub_name=}")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM subscriptions WHERE name =? LIMIT 1", (sub_name,))
            r = self.lsc.cursor.fetchone()
        if not r:
            return None
        return r[0]
    
    def get_monitored_services(self, ):
        logger.debug(f"")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM monitored_services")
            result = self.lsc.cursor.fetchall()
            return result
    
    def get_monitored_service_by_id(self, ser_id):
        logger.debug(f"{ser_id=}")
        with self.lsc:
            self.lsc.cursor.execute(f"SELECT * FROM monitored_services WHERE id=?", (ser_id,))
            result = self.lsc.cursor.fetchone()
            return result
