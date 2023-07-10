from .settings import bot
from . import messages as ms
from telebot.types import Message
from .db_functions import test_subscription, get_subscriptions_for_user, get_subscription_by_id
import requests

@bot.message_handler(commands=["start"])
async def handle_start_command(message: Message) -> None:
    await bot.send_message(message.chat.id, ms.WELCOME_MESSAGE)

@bot.message_handler(commands=["subscribe"])
async def subscribe_command(message: Message) -> None:
    test_subscription()

@bot.message_handler(commands=["joke"])
async def joke_command(message: Message) -> None:
    joke_text = requests.get('https://geek-jokes.sameerkumar.website/api?format=json').json()["joke"]
    await bot.send_message(message.chat.id, joke_text)

@bot.message_handler(commands=["mysubscriptions"])
async def my_subscriptions_command(message: Message) -> None:
    uid = message.chat.id
    subs = get_subscriptions_for_user(uid)
    if subs:
        result = ms.YOUR_SUBSCRIPTIONS+f" {len(subs)}:\n"
        for sub in subs:
            sub_info = get_subscription_by_id(sub.sub_id)
            result+=f"{sub_info.name} {ms.REMIND_ON if sub.remind else ms.REMIND_OFF}\n{sub_info.description}\n\n"
        await bot.send_message(uid, result)
    else:
        await bot.send_message(uid, ms.NO_SUBSCRIPTIONS)
