import secrets
from telebot.async_telebot import AsyncTeleBot
import asyncio
import time
import threading
from database import *


bot = AsyncTeleBot(secrets.API_TOKEN)

count = 0


async def check_db():
    while True:
        global count
        count += 1
        print(count)
        print(get_unread_messages())
        for row in get_unread_messages():
            mid, msg = row
            await bot.send_message(5718232858,msg)
            mark_message_as_read(mid)

        await asyncio.sleep(1)
        # time.sleep(1)


@bot.message_handler(commands=['count'])
async def send_welcome(message):
    await bot.reply_to(message, f"Counter = {count}")


async def run():
    await asyncio.gather(check_db(), bot.polling())


def start():
    asyncio.run(run())

if __name__ == "__main__":
    start()
    
    threads = []
    # запустить в 4 потока
    # for i in range(4):
    #     t = threading.Thread(target=start)
    #     threads.append(t)
    #     t.start()

    # for t in threads:
    #     t.join()
