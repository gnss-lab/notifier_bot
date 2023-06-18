import uvicorn
from fastapi import FastAPI

import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
import secrets
import asyncio
import threading


subscribers = [5718232858]

# Telegram bot
bot = AsyncTeleBot(secrets.API_TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hello!")

async def notify_all():
    for uid in subscribers:
        await bot.send_message(uid, "Hello!")



# FastAPI
app = FastAPI()

@app.get('/')
def root():
    await notify_all()
    return {'message': 'Hello, World!'}


def start_services():
    # code for starting the bot and API service
    pass


if __name__ == '__main__':
    start_services()
