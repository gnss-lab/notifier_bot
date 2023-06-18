import secrets
from telebot.async_telebot import AsyncTeleBot
import asyncio
import time

bot = AsyncTeleBot(secrets.API_TOKEN)

count = 0


async def check_db():
    while True:
        global count
        count += 1
        print(count)
        # await asyncio.sleep(1)
        time.sleep(1)


@bot.message_handler(commands=['count'])
async def send_welcome(message):
    await bot.reply_to(message, f"Counter = {count}")


async def run():
    await asyncio.gather(check_db(), bot._process_polling())


if __name__ == "__main__":
    asyncio.run(run())

# запустить в 4 потока