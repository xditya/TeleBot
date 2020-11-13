# Incoming message checker.
from telebot.plugins.mybot.sql.users_sql import add_user_to_db
from chatrobot.plugins.sql.blacklist_sql import check_is_black_list
from telethon import events
from telethon.tl.types import (Channel, Chat, User)
from telebot.plugins import OWNER_ID

# if incoming
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def one_new_mssg(event):
    incoming = event.raw_text
    who = event.sender_id
    if check_is_black_list(who):
        return
    if incoming.startswith("/"):
        pass
    elif who == OWNER_ID:
        return
    else:
        sender = await event.get_sender()
        chat_id = event.chat_id
        to = await event.forward_to(OWNER_ID)
        add_user_to_db(to.id, who, event.id)
  