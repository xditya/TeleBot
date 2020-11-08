#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @INF1N17Y

from uniborg.util import admin_cmd

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern=r"mention (.*)"))
@telebot.on(sudo_cmd(pattern=r"mention (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = previous_message.forward.from_id
        else:
            replied_user = previous_message.from_id
    else:
        await eor(event, "reply To Message")
    user_id = replied_user
    caption = """<a href='tg://user?id={}'>{}</a>""".format(user_id, input_str)
    await eor(event, caption, parse_mode="HTML")


CMD_HELP.update(
    {
        "mention": ".mention <word> (reply to user)\nUse - Mention that user by that word."
    }
)
