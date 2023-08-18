import asyncio
from .settings import bot, scheduler
from .command_handlers import *
from .callback_handlers import *
from .db_functions import *
from loguru import logger
#todo fix bad imports

async def gather():
    scheduler.start()
    await asyncio.gather(check_db(), bot.polling(non_stop=True))
def start_bot():
    logger.trace("asyncio.run")
    try:
        asyncio.run(gather())
    except Exception as e:
        logger.critical(f"bot evaluation stopped with an exception: {e.args}")
