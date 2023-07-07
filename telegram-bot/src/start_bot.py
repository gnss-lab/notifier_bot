import asyncio
from .settings import bot, scheduler
from .command_handlers import *
from .callback_handlers import *
from .db_functions import *
#todo fix bad imports

async def gather():
    scheduler.start()
    await asyncio.gather(check_db(), bot.polling(non_stop=True))

def start_bot():
    # non_stop - Do not stop polling when an ApiException occurs
    # task = asyncio.create_task()
    asyncio.run(gather())
