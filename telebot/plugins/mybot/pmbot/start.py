from telebot.plugins.mybot import *
from telethon import events, Button

# start-other-enabled


@tgbot.on(events.NewMessage(pattern="^/start"))
async def start_all(event):
    if event.sender_id == OWNER_ID:
        return
    else:
        await tgbot.send_message(event.chat_id,
                                 startotherena,
                                 buttons=[
                                     (Button.url(
                                         "TeleBot",
                                         url="https://github.com/xditya/TeleBot"))]
                                 )
