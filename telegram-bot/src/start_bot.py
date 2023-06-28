import asyncio
from .settings import bot
from .command_handlers import *

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# from src.admin_panel.admin_command_handler import *
# from src.text_handlers import *
# from src.callback_handlers import *
# from src.admin_panel.admin_callback_handlers import *


def start_bot():
    # non_stop - Do not stop polling when an ApiException occurs
    # task = asyncio.create_task()
    asyncio.run(bot.polling(non_stop=True))