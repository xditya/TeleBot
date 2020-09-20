#  (c)2020 TeleBot
#
# You may not use this plugin without proper authorship and consent from @TeleBotSupport
#
from userbot.utils import admin_cmd
import os
from telethon.tl import functions
from telethon.tl.functions.account import (UpdateProfileRequest)
from userbot import ALIVE_NAME

TELENAME = ALIVE_NAME if ALIVE_NAME else "TeleBot"

# set your mood
@telebot.on(admin_cmd(pattern="mood ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = f"「{names}」"
    last_name = f"{ALIVE_NAME}"
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            first_name=first_name,
            last_name=last_name
        ))
        await event.edit("Mood set xD")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))

# reset back        
@telebot.on(admin_cmd(pattern="resetmood"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    first_name = f"{ALIVE_NAME}"
    last_name = ""
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            first_name=first_name,
            last_name=last_name
        ))
        await event.edit("Mood reset xD")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
        
"""
Usage - .mood Offline - Sets name to Offline ALIVE_NAME
        .resetmood - revert changes
"""
