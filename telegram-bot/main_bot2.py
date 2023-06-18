import requests
import telebot
from telebot import types
import secrets
import asyncio

subscribers = [5718232858]

bot = AsyncTeleBot(secrets.API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
	bot.reply_to(message, f'You said: "{message.text}"!')


def start_bot():
	print("Bot is running...")
	# notify_all("Какой-то сервис не работает")
	bot.polling()

if __name__ == "__main__":
    asyncio.run(start_bot())