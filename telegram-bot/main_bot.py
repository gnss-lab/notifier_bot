import requests
import telebot
from telebot import types
import secrets

subscribers = [5718232858]

# from telebot.async_telebot import AsyncTeleBot

# bot = AsyncTeleBot(API_TOKEN)


bot = telebot.TeleBot(secrets.API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@bot.message_handler(commands=['id'])
def command_id(message):
	# print(message)
	bot.send_message(message.chat.id, "Ваш id:\n"+str(message.chat.id))


@bot.message_handler(commands=['notify_all'])
def command_notify_all(message):
	text = message.text[len("/notify_all"):]
	if text:
		notify_all(text)
		bot.send_message(message.chat.id, f"Сообщение отправлено {len(subscribers)} пользователям")
	else:
		bot.send_message(message.chat.id, "Вы не ввели сообщение для отправки")



@bot.message_handler(commands=['joke'])
def send_joke(message):
	joke_text = requests.get('https://geek-jokes.sameerkumar.website/api?format=json').json()["joke"]
	bot.send_message(message.chat.id, joke_text)


def notify_all(text):
	for uid in subscribers:
		notify(uid, text)


def notify(user_id, text):
    keyboard = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton("Сайт", url='https://simurg.iszf.irk.ru/')
    ok_button = types.InlineKeyboardButton("Ок", callback_data='ok')
    keyboard.add(link_button, ok_button)
    
    bot.send_message(user_id, text, reply_markup=keyboard)


# func - filter function. Call Obfect fields https://pytba.readthedocs.io/en/latest/types.html#telebot.types.CallbackQuery
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    # if call.data == 'repeat':
        # Отправляем сообщение повторно
        # bot.send_message(call.message.chat.id, "Привет!", reply_markup=call.message.reply_markup)
        # test(call.message)
    if call.data == 'ok':
        # Отправляем сообщение "Всё ок!"
        bot.send_message(call.message.chat.id, "Напоминание выключено")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
	bot.reply_to(message, f'You said: "{message.text}"!')




print("Bot is running...")
notify_all("Какой-то сервис не работает")
bot.infinity_polling()
