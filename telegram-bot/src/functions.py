import schedule

from telebot.types import Message
from telebot import types
from .settings import bot
import asyncio

scheduled_jobs = dict()

def check_user_permissions(message: Message) -> bool:
    # if not user_exist(message.chat.id):
    #     bot.send_message(message.chat.id, NOT_REGISTERED_MESSAGE)
    #     return False
    return True

async def send_notification(telegram_id, message, add_keyboard=False):
    if add_keyboard:
        keyboard = types.InlineKeyboardMarkup()
        ok_button = types.InlineKeyboardButton("Ок", callback_data='ok')
        keyboard.add(ok_button)
        await bot.send_message(telegram_id, message, reply_markup=keyboard)
    else:
        await bot.send_message(telegram_id, message)

def schedule_notification(telegram_id, message):

    def notify():
        # RuntimeError: This event loop is already running
        asyncio.run(send_notification(telegram_id, message, True))

    job = schedule.every(3).seconds.do(notify)
    if telegram_id in scheduled_jobs:
        schedule.cancel_job(scheduled_jobs[telegram_id])
    scheduled_jobs[telegram_id] = job

def cancel_notification(telegram_id):
    if telegram_id in scheduled_jobs:
        del scheduled_jobs[telegram_id]