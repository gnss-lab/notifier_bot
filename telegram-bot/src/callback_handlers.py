from .settings import bot
from .functions import cancel_notification
from .command_handlers import show_subscription_card, show_subscription_list_for_user
from . import messages as ms

@bot.callback_query_handler(func=lambda call: call.data == "ok")
async def callback(call) -> None:

    if call.data == "ok":
        await cancel_notification(call.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_CHANGE_SUB))
async def sub_callback(call) -> None:
    user_id = call.from_user.id
    data = call.data.split(";")
    need_subscribe = data[1]=="on"
    sub_id = int(data[2])

    await bot.send_message(user_id, f"{need_subscribe=},{sub_id=}")

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_CHANGE_NOTIF))
async def notif_callback(call) -> None:
    user_id = call.from_user.id
    data = call.data.split(";")
    need_notif = data[1]=="on"
    sub_id = int(data[2])
    await bot.send_message(user_id, f"{need_notif=},{sub_id=}")

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_SHOW_SUB_CARD))
async def show_sub_card_callback(call) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    sub_id = int(call.data.split(";")[1])
    await show_subscription_card(user_id, sub_id, changeable_message_id=message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_SHOW_SUB_LIST))
async def show_sub_list_callback(call) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    await show_subscription_list_for_user(user_id, changeable_message_id=message_id)
