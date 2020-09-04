# For TeleBot, by @its_xditya, @MrConfused and @Jisan7509. 
# Kangers keep credits.

from userbot.utils import command, remove_plugin, load_module
from pathlib import Path
import asyncio
import os
import userbot.utils
from datetime import datetime
from .. import ALIVE_NAME 
from userbot.utils import admin_cmd
DELETE_TIMEOUT = 5
thumb_image_path = "./TeleBot.png"

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot User"

@telebot.on(admin_cmd(pattern="send (?P<shortname>\w+)", outgoing=True))
async def send(event):
    if event.fwd_from:
        return
    hmm = bot.uid
    message_id = event.message.id
    thumb = thumb_image_path
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./userbot/plugins/{}.py".format(input_str)
    start = datetime.now()
    pro = await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        thumb=thumb,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await pro.edit(f"__**Plugin Name:- {input_str} .**__\n__**Uploaded in {time_taken_in_ms} seconds.**__\n__**Uploaded by :-**__ [{DEFAULTUSER}](tg://user?id={hmm})\n© @TeleBotSupport")
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
