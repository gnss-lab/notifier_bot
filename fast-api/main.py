from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import src.db_functions as db

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.get("/add/user")
async def add_user(user_id: int):
    """user_id = telegram_id"""
    db.add_user(user_id)

@app.get("/add/subscription")
async def add_subscription(sub_name: str, sub_description: str):
    db.add_subscription(sub_name, sub_description)

@app.get("/subscribe")
async def subscribe(sub_id:int, user_id:int, remind:bool = False):
    db.subscribe(sub_id, user_id, remind)

@app.get("/send_notification")
async def send_notification(message: str, sub_id: int):
    db.add_notification(message, sub_id)

@app.get("/get/users")
async def get_users():
    return db.get_users()

@app.get("/get/subscriptions")
async def get_subscriptions():
    return db.get_subscriptions()

@app.get("/get/users_subscriptions")
async def get_users_subscriptions():
    return db.get_users_subscriptions()

@app.get("/get/notifications")
async def get_notifications():
    return db.get_notifications()





# uvicorn main:app --reload