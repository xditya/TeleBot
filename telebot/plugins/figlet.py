import pyfiglet

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="figlet ?(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="figlet ?(.*)", allow_sudo=True))
async def figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        text, cmd = input_str.split("|", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await eor(event, "Please add some text to figlet")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await eor(event, "Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await event.respond("‌‌‎`{}`".format(result))
    await event.delete()


CMD_HELP.update({"figlet": ".figlet <text>\nUse - Try it yourself."})
