# By @HeisenbergTheDanger for TeleBot
# @its_xditya
# Kangers keep credits

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="pmto ?(.*)"))
async def pmto(event):
    a = event.pattern_match.group(1)
    b = a.split(" ")
    chat_id = b[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    msg = ""
    for i in b[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await borg.send_message(chat_id, msg)
        await event.edit("Message sent!")
    except BaseException:
        await event.edit("Something went wrong.")


CMD_HELP.update({"pmto": ".pmto <username> <message>"})
