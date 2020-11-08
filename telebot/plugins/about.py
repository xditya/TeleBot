# Ported from other Telegram UserBots for TeleBot//Made for TeleBot
# Kangers, don't remove this line
# @its_xditya

"""Available Commands:
.info
"""

import asyncio

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="info"))
@telebot.on(sudo_cmd(pattern="info", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 36)
    # input_str = event.pattern_match.group(1)
    # if input_str == "Visit this page to know more about TeleBot.":
    await eor(event, "Thanks")
    animation_chars = ["**TeleBot**", "[More Info](https://telegra.ph/TeleBot-07-08)"]

    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await eor(event, animation_chars[i % 18])


CMD_HELP.update({"about": "➟ .info\nUse - Get to know about your bot."})
