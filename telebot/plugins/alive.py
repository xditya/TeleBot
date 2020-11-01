# For @TeleBotHelp
"""Check if your userbot is working."""
import os
import time
from datetime import datetime
from io import BytesIO
from telebot import CMD_HELP
import requests
from PIL import Image

from telebot import telever
from telebot.__init__ import StartTime
from telebot.telebotConfig import Config
from telebot.utils import admin_cmd, sudo_cmd

temp = telebot.me
ALIVE_NAME = temp.first_name

ALV_PIC = os.environ.get("ALIVE_PIC", None)

if Config.SUDO_USERS:
    sudo = "Enabled"
else:
    sudo = "Disabled"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"


@telebot.on(admin_cmd(outgoing=True, pattern="alive"))
@telebot.on(sudo_cmd(outgoing=True, pattern="alive", allow_sudo=True))
async def amireallyalive(alive):
    start = datetime.now()
    myid = bot.uid
    """ For .alive command, check if the bot is running.  """
    end = datetime.now()
    (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    if ALV_PIC:
        tele = f"**Welcome To TeleBot **\n\n"
        tele += "`Hey! I'm alive. All systems online and functioning normally!`\n\n"
        tele += "` 🔸 Telethon version:` **1.17**\n` 🔹 Python:` **3.8.3**\n"
        tele += f"` 🔸 TeleBot Version:` **{telever}**\n"
        tele += "` 🔹 More Info:` **@TeleBotSupport**\n"
        tele += f"` 🔸 Sudo :` **{sudo}**\n"
        tele += f"` 🔹 TeleBot Uptime:` **{uptime}**\n"
        tele += "` 🔸 Database Status:` **All OK 👌!**\n"
        tele += f"` 🔹 My pro owner` : **[{DEFAULTUSER}](tg://user?id={myid})**\n\n"
        tele += "    [✨ GitHub Repository ✨](https://github.com/xditya/TeleBot)"

        await alive.get_chat()
        await alive.delete()
        """ For .alive command, check if the bot is running.  """
        await borg.send_file(alive.chat_id, ALV_PIC, caption=tele, link_preview=False)
        await alive.delete()
        return
    req = requests.get("https://telegra.ph/file/0670190de8e3bddea6d95.png")
    req.raise_for_status()
    file = BytesIO(req.content)
    file.seek(0)
    img = Image.open(file)
    with BytesIO() as sticker:
        img.save(sticker, "webp")
        sticker.name = "sticker.webp"
        sticker.seek(0)
        await borg.send_message(
            alive.chat_id,
            f"**Welcome To TeleBot **\n\n"
            "`Hey! I'm alive. All systems online and functioning normally!`\n\n"
            "` 🔸 Telethon version:` **1.17**\n` 🔹 Python:` **3.8.3**\n"
            f"` 🔸 TeleBot Version:` **{telever}**\n"
            "` 🔹 More Info:` **@TeleBotSupport**\n"
            f"` 🔸 Sudo :` **{sudo}**\n"
            f"` 🔹 TeleBot Uptime:` **{uptime}**\n"
            "` 🔸 Database Status:` **All OK 👌!**\n"
            f"` 🔹 My pro owner` : **[{DEFAULTUSER}](tg://user?id={myid})**\n\n"
            "    [✨ GitHub Repository ✨](https://github.com/xditya/TeleBot)",
            link_preview=False,
        )
        await borg.send_file(alive.chat_id, file=sticker)
        await alive.delete()

CMD_HELP.update(
    {
        "alive": ".alive\nUse - Check if your bot is working."
    }
)
