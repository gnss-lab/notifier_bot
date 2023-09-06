from telegram_bot.src.start_bot import start_bot
from telegram_bot.src.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    start_bot()