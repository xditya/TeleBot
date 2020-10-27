# (c)2020 TeleBot
# You may not use this file without proper authorship and consent from @TeleBotSupport
#
"""
Available command(s)
.sticklol
Generates a. random laughing sticker.
"""
import random

from telethon import functions, types, utils

from telebot.utils import admin_cmd


def choser(cmd, pack, blacklist=None):
    if blacklist is None:
        blacklist = {}
    docs = None

    @telebot.on(admin_cmd(pattern=rf"{cmd}", outgoing=True))
    async def handler(event):
        await event.delete()

        nonlocal docs
        if docs is None:
            docs = [
                utils.get_input_document(x)
                for x in (
                    await borg(
                        functions.messages.GetStickerSetRequest(
                            types.InputStickerSetShortName(pack)
                        )
                    )
                ).documents
                if x.id not in blacklist
            ]

        await event.respond(file=random.choice(docs))


choser(
    "sticklol",
    "TeleBot_LOLPack",
    {
        3088919966519394666,
        3088919966519394334,
        3088919966519394334,
        3088919966519394334,
    },
)
