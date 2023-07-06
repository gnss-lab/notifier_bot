from .settings import bot
from .functions import cancel_notification

@bot.callback_query_handler(func=lambda call: True)
def callback(call) -> None:

    if call.data == "ok":
        cancel_notification(call.from_user)
