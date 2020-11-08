from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(outgoing=True, pattern="group"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern="group"))
async def join(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await eor(
            e,
            "This is my community.\n\n[Channel](http://t.me/giveaways_24hrs)\n\n[Chat Group](https://t.me/giveaways24hrsdiscuss)\n\n[UserBot Tutorial - TeleBot](https://t.me/TeleBotHelp)\n\n[TeleBot Chat](https://t.me/TeleBotHelpChat)\n\n[Github](https://github.com/xditya)\n\n[YouTube](https://bit.ly/adityas7)",
        )


CMD_HELP.update({"group": ".group\nUse - None."})
