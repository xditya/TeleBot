from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="tspam"))
async def tmeme(e):
    tspam = str(e.text[7:])
    message = tspam.replace(" ", "")
    for letter in message:
        await e.respond(letter)
    await e.delete()


CMD_HELP.update({"spamV2": ".tspam\nUse - Text spam."})
