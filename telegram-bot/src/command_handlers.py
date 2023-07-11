from .settings import bot
from . import messages as ms
from telebot.types import Message
from .db_functions import test_notification, get_users_subscriptions_for_user, get_subscription_by_id
import requests
from telebot import types

@bot.message_handler(commands=["start"])
async def handle_start_command(message: Message) -> None:
    await bot.send_message(message.chat.id, ms.WELCOME_MESSAGE)

@bot.message_handler(commands=["subscribe"])
async def subscribe_command(message: Message) -> None:
    pass

@bot.message_handler(commands=["test_notification"])
async def test_notification_command(message: Message) -> None:
    test_notification()

@bot.message_handler(commands=["joke"])
async def joke_command(message: Message) -> None:
    joke_text = requests.get('https://geek-jokes.sameerkumar.website/api?format=json').json()["joke"]
    await bot.send_message(message.chat.id, joke_text)

@bot.message_handler(commands=["my_subscriptions"])
async def my_subscriptions_command(message: Message) -> None:
    await show_subscription_list_for_user(message.chat.id)


async def show_subscription_list_for_user(user_id, changeable_message_id=None):
    subs = get_users_subscriptions_for_user(user_id)
    if subs:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for sub in subs:
            sub_info = get_subscription_by_id(sub.sub_id)
            button = types.InlineKeyboardButton(sub_info.name, callback_data=f"{ms.CALLBACK_SHOW_SUB_CARD};{sub.sub_id}")
            keyboard.add(button)
            # result += f"{sub_info.name} {ms.REMIND_ON if sub.remind else ms.REMIND_OFF}\n{sub_info.description}\n\n"
        if changeable_message_id:
            await bot.edit_message_text(ms.YOUR_SUBSCRIPTIONS, user_id, changeable_message_id, reply_markup=keyboard)
        else:
            await bot.send_message(user_id, ms.YOUR_SUBSCRIPTIONS, reply_markup=keyboard)

    else:
        await bot.send_message(user_id, ms.NO_SUBSCRIPTIONS)

async def show_subscription_card(user_id, sub_id, changeable_message_id=None):
    sub_info = get_subscription_by_id(sub_id)
    sub = next((x for x in get_users_subscriptions_for_user(user_id) if x.sub_id==sub_id),None)
    sub_mark = ms.SUBSCRIBED if sub else ms.UNSUBSCRIBED
    notif_mark = ms.REMIND_ON if sub.remind else ms.REMIND_OFF
    text = f"{sub_info.name}\n{sub_info.description}\n{ms.SUBSCRIPTION}:{sub_mark}\n{ms.NOTIFICATION}:{notif_mark}"
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    sub_button = types.InlineKeyboardButton(ms.UNSUBSCRIBE if sub else ms.SUBSCRIBE, callback_data=f"{ms.CALLBACK_CHANGE_SUB};{'off' if sub else 'on'};{sub.sub_id}")
    notif_button = types.InlineKeyboardButton(ms.TURN_OFF_NOTIF if sub.remind else ms.TURN_ON_NOTIF, callback_data=f"{ms.CALLBACK_CHANGE_NOTIF};{'off' if sub.remind else 'on'};{sub.sub_id}")
    back_button = types.InlineKeyboardButton(ms.GO_BACK, callback_data=ms.CALLBACK_SHOW_SUB_LIST)
    keyboard.add(sub_button, notif_button, back_button)
    if changeable_message_id:
        await bot.edit_message_text(text, user_id, changeable_message_id, reply_markup=keyboard)
    else:
        await bot.send_message(user_id, text, reply_markup=keyboard)
