from .settings import bot
from .functions import cancel_notification
from .command_handlers import show_subscription_card, show_my_subscriptions, show_not_my_subscriptions
from .db_functions import set_notification, get_one_users_subscription, subscribe, unsubscribe
from . import messages as ms
from telebot.types import CallbackQuery

@bot.callback_query_handler(func=lambda call: call.data == "ok")
async def callback(call: CallbackQuery) -> None:
    if call.data == "ok":
        await cancel_notification(call.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_CHANGE_SUB))
async def sub_callback(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    data = call.data.split(";")
    need_subscribe = data[1]=="on"
    sub_id = int(data[2])
    show_my_subs = data[3] == 'True'
    message_id = call.message.message_id
    sub = get_one_users_subscription(user_id, sub_id)
    if need_subscribe:
        if not sub:
            subscribe(sub_id, user_id)
    elif sub:
        unsubscribe(sub_id, user_id)
    await show_subscription_card(user_id, sub_id, message_id, show_my_subs)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_CHANGE_NOTIF))
async def notif_callback(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    data = call.data.split(";")
    remind = data[1]=="on"
    sub_id = int(data[2])
    show_my_subs = data[3] == 'True'
    message_id = call.message.message_id
    set_notification(remind,sub_id, user_id)
    await show_subscription_card(user_id, sub_id, message_id, show_my_subs)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_SHOW_SUB_CARD))
async def show_sub_card_callback(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data.split(";")
    sub_id = int(data[1])
    show_my_subs = data[2] == 'True'
    await show_subscription_card(user_id, sub_id, message_id, show_my_subs)

@bot.callback_query_handler(func=lambda call: call.data.startswith(ms.CALLBACK_SHOW_SUB_LIST))
async def show_sub_list_callback(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data.split(";")
    show_my_subs = data[1] == 'True'
    if show_my_subs:
        await show_my_subscriptions(user_id, message_id)
    else:
        await show_not_my_subscriptions(user_id, message_id)