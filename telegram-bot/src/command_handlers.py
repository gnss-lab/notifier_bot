from .settings import bot
from . import messages as ms
from telebot.types import Message
from .db_functions import get_subscription_by_id, add_telegram_user,\
    get_one_users_subscription, get_subscriptions_for_user, get_not_subscriptions_for_user
import requests
from telebot import types

@bot.message_handler(commands=["start"])
async def handle_start_command(message: Message) -> None:
    add_telegram_user(message.chat.id)
    await bot.send_message(message.chat.id, ms.WELCOME_MESSAGE)

@bot.message_handler(commands=["joke"])
async def joke_command(message: Message) -> None:
    joke_text = requests.get('https://geek-jokes.sameerkumar.website/api?format=json').json()["joke"]
    await bot.send_message(message.chat.id, joke_text)

@bot.message_handler(commands=["id"])
async def joke_command(message: Message) -> None:
    await bot.send_message(message.chat.id, str(message.chat.id))

@bot.message_handler(commands=["my_subscriptions"])
async def my_subscriptions_command(message: Message) -> None:
    await show_my_subscriptions(message.chat.id)

@bot.message_handler(commands=["subscribe"])
async def subscribe_command(message: Message) -> None:
    await show_not_my_subscriptions(message.chat.id)

async def show_subscriptions_list(sub_list:list, user_id, success_message, fail_message, is_my_subscriptions, changeable_message_id=None):
    if sub_list:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for sub in sub_list:
            button = types.InlineKeyboardButton(sub.name, callback_data=f"{ms.CALLBACK_SHOW_SUB_CARD};{sub.id};{is_my_subscriptions}")
            keyboard.add(button)
        if changeable_message_id:
            await bot.edit_message_text(success_message, user_id, changeable_message_id, reply_markup=keyboard)
        else:
            await bot.send_message(user_id, success_message, reply_markup=keyboard)
    else:
        if changeable_message_id:
            await bot.edit_message_text(fail_message, user_id, changeable_message_id)
        else:
            await bot.send_message(user_id, fail_message)

async def show_my_subscriptions(user_id, changeable_message_id=None):
    subs = get_subscriptions_for_user(user_id)
    await show_subscriptions_list(subs, user_id, ms.YOUR_SUBSCRIPTIONS, ms.NO_SUBSCRIPTIONS, True, changeable_message_id)

async def show_not_my_subscriptions(user_id, changeable_message_id=None):
    subs = get_not_subscriptions_for_user(user_id)
    await show_subscriptions_list(subs, user_id, ms.SUBSCRIPTIONS_YOU_NOT_SUBSCRIBED, ms.YOU_SUBSCRIBED_EVERYTHING, False, changeable_message_id)

async def show_subscription_card(user_id, sub_id, changeable_message_id, callback_my_subs):
    sub_info = get_subscription_by_id(sub_id)
    sub = get_one_users_subscription(user_id, sub_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    text = f"{sub_info.name}\n{sub_info.description}\n"
    if sub:
        if sub.remind:
            notif_button = types.InlineKeyboardButton(ms.TURN_OFF_NOTIF, callback_data=f"{ms.CALLBACK_CHANGE_NOTIF};off;{sub_id};{callback_my_subs}")
            notif_mark = ms.REMIND_ON
        else:
            notif_button = types.InlineKeyboardButton(ms.TURN_ON_NOTIF, callback_data=f"{ms.CALLBACK_CHANGE_NOTIF};on;{sub_id};{callback_my_subs}")
            notif_mark = ms.REMIND_OFF
        sub_button = types.InlineKeyboardButton(ms.UNSUBSCRIBE, callback_data=f"{ms.CALLBACK_CHANGE_SUB};off;{sub_id};{callback_my_subs}")
        keyboard.add(sub_button, notif_button)

        text+=f"{ms.SUBSCRIPTION}:{ms.SUBSCRIBED}\n{ms.NOTIFICATION}:{notif_mark}"
    else:
        text+=f"{ms.SUBSCRIPTION}:{ms.UNSUBSCRIBED}"
        sub_button = types.InlineKeyboardButton(ms.SUBSCRIBE, callback_data=f"{ms.CALLBACK_CHANGE_SUB};on;{sub_id};{callback_my_subs}")
        keyboard.add(sub_button, row_width=2)

    back_button = types.InlineKeyboardButton(ms.GO_BACK, callback_data=f"{ms.CALLBACK_SHOW_SUB_LIST};{callback_my_subs}")
    keyboard.add(back_button)

    if changeable_message_id:
        await bot.edit_message_text(text, user_id, changeable_message_id, reply_markup=keyboard)
    else:
        await bot.send_message(user_id, text, reply_markup=keyboard)
