# Copyright TeleBot
# For @TeleBitHelp coded by @xditya
# Kangers keep credits else I'll take down 🧐

import asyncio
import random
import re
import time

from collections import deque
from userbot import ALIVE_NAME
import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from cowpy import cow

from userbot import CMD_HELP,YOUTUBE_API_KEY
from userbot.utils import register

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "No name set yet, check pinned in @TeleBotHelp"

ONLINESTR = [
    "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ \n █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░ \n █░░║║║╠─║─║─║║║║║╠─░░ \n █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░ \n █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
    "\n\n```TeleBot is online.\nAll systems functioning normally ! ```\n"
    "Bot by [Aditya 🇮🇳](tg://user?id=719195224) \n"
    "More help - @TeleBotHelpChat \n\n"
    "           [🚧 GitHub Repository 🚧](https://github.com/xditya/TeleBot) " ,
    
    ]

@register(outgoing=True, pattern="^.online$")
async def telebot (onl):
    """ Check if TeleBot is online"""
    if not onl.text[0].isalpha() and onl.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(ONLINESTR) - 1)
        reply_text = ONLINESTR[index]
        await onl.edit(reply_text)
                     