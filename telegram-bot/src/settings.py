from pydantic import BaseSettings
from typing import Optional
from telebot.async_telebot import AsyncTeleBot


class Settings(BaseSettings):
    tg_token: str

    admins: list
    subscribers: list

    bot: Optional[AsyncTeleBot]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = AsyncTeleBot(self.tg_token)
        print("Starting bot...")
        # print(self.bot.get_me())

    # for auto importing .env variables by BaseSettings module
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
bot = settings.bot
