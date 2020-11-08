# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import wait

from telebot import CMD_HELP
from telebot.telebotConfig import Var
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern=r"spam", outgoing=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])

        await wait([e.respond(spam_message) for i in range(counter)])

        await e.delete()
        if Var.PRIVATE_GROUP_ID:
            await e.client.send_message(
                Var.PRIVATE_GROUP_ID, "#SPAM \n\n" "Spam was executed successfully"
            )


CMD_HELP.update({"spam": ".spam <n> <text>\nUse -Spam the word/sentence 'n' times."})
