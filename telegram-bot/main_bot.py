import requests
import telebot
from telebot import types
import secrets
import asyncio
from telebot.async_telebot import AsyncTeleBot


subscribers = [5718232858]

bot = AsyncTeleBot(secrets.API_TOKEN)

# bot = telebot.TeleBot(secrets.API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
	await bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@bot.message_handler(commands=['id'])
async def command_id(message):
	# print(message)
	await bot.send_message(message.chat.id, "Ваш id:\n"+str(message.chat.id))


@bot.message_handler(commands=['notify_all'])
async def command_notify_all(message):
	text = message.text[len("/notify_all"):]
	if text:
		await notify_all(text)
		await bot.send_message(message.chat.id, f"Сообщение отправлено {len(subscribers)} пользователям")
	else:
		await bot.send_message(message.chat.id, "Вы не ввели сообщение для отправки")



@bot.message_handler(commands=['joke'])
async def send_joke(message):
	joke_text = requests.get('https://geek-jokes.sameerkumar.website/api?format=json').json()["joke"]
	await bot.send_message(message.chat.id, joke_text)


async def notify_all(text):
	tasks = []
	for uid in subscribers:
		tasks.append(notify(uid, text))
	await asyncio.gather(*tasks)


async def notify(user_id, text):
    keyboard = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton("Сайт", url='https://simurg.iszf.irk.ru/')
    ok_button = types.InlineKeyboardButton("Ок", callback_data='ok')
    keyboard.add(link_button, ok_button)
    
    await bot.send_message(user_id, text, reply_markup=keyboard)


# func - filter function. Call Obfect fields https://pytba.readthedocs.io/en/latest/types.html#telebot.types.CallbackQuery
@bot.callback_query_handler(func=lambda call: True)
async def handle_button_click(call):
    msg = "Что-то пошло не так"
    # if call.data == 'repeat':
        # Отправляем сообщение повторно
        # bot.send_message(call.message.chat.id, "Привет!", reply_markup=call.message.reply_markup)
        # test(call.message)
    if call.data == 'ok':
    	msg = "Напоминание выключено"
    
    await bot.send_message(call.message.chat.id, msg)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
	await bot.reply_to(message, f'You said: "{message.text}"!')




async def start_loop():
	print("Bot is running...")
	# notify_all("Какой-то сервис не работает")
	await bot.polling()

def start_bot():
	asyncio.run(start_loop())
if __name__ == "__main__":
    asyncio.run(start_bot())