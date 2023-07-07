from .settings import bot
from . import messages as ms
from telebot.types import Message
from .db_functions import test_subscription
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
