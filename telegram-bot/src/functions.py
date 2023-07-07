from telebot.types import Message
from telebot import types
from .settings import bot, scheduler
from . import messages

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
    job = scheduler.add_job(send_notification, 'interval', args=(telegram_id, message, True), seconds=5)
    if telegram_id in scheduled_jobs:
        scheduled_jobs[telegram_id].remove()
    scheduled_jobs[telegram_id] = job

async def cancel_notification(telegram_id):
    if telegram_id in scheduled_jobs:
        scheduled_jobs[telegram_id].remove()
        del scheduled_jobs[telegram_id]
    await bot.send_message(telegram_id, messages.NOTIFICATION_DISABLED)