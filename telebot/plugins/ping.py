# special thanks to Sur_vivor
# Re-written for TeleBot by @its_xditya

import time
from datetime import datetime

from telebot import CMD_HELP
from telebot.__init__ import StartTime
from telebot.plugins import OWNER_ID, TELE_NAME


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


# @command(pattern="^.ping$")


@telebot.on(admin_cmd(pattern="ping$"))
@telebot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    x = await eor(event, "⛝ Pong! ⛝")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    await x.edit(
        f"⪼ **Ping speed** : `{ms}`\n⪼ **Uptime** : `{uptime}`\n⪼ **Owner** : [{TELE_NAME}](tg://user?id={OWNER_ID})"
    )


CMD_HELP.update({"ping": ".ping\nUse - See the ping stats and uptime of userbot."})
