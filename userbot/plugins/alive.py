# For @TeleBotHelp
"""Check if your userbot is working."""
import requests
import time
from PIL import Image
from io import BytesIO
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd
from userbot.__init__ import StartTime
from datetime import datetime

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

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "No name set yet, check pinned in @TeleBotHelp"

@command(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    start = datetime.now()
    req = requests.get("https://telegra.ph/file/0670190de8e3bddea6d95.png")
    req.raise_for_status()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    file = BytesIO(req.content)
    file.seek(0)
    img = Image.open(file)
    with BytesIO() as sticker:
        img.save(sticker, "webp")
        sticker.name = "sticker.webp"
        sticker.seek(0)
        await borg.send_message(alive.chat_id, f"**Welcome To TeleBot **\n\n"
            "**`Hey! I'm alive. All systems online and functioning normally!`**\n\n"
            "` 🔸 Telethon version:` **1.15.0**\n` 🔹 Python:` **3.8.3**\n"
            "` 🔸 More info:` [TeleBot](https://telegra.ph/TeleBot-07-08)\n"
            "` 🔹 Bot created by:` [Aditya](https://t.me/xditya)\n"
            f"` 🔸 TeleBot Uptime:` {uptime}\n"
            "` 🔸 Database Status:` **All OK 👌!**\n"
            f"` 🔹 My pro owner`: {DEFAULTUSER}\n\n"
            "    [✨ GitHub Repository ✨](https://github.com/xditya/TeleBot)", link_preview = False)
        await borg.send_file(alive.chat_id, file=sticker) 
        await alive.delete()
