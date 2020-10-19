# special thanks to Sur_vivor
# Re-written for TeleBot by @its_xditya

import time
from datetime import datetime

from userbot.__init__ import StartTime
from userbot.utils import admin_cmd, sudo_cmd


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
@telebot.on(sudo_cmd(pattern="ping$"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("🏓 Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    await event.edit(f"🏓Ping speed: {ms}\n🤖TeleBot Uptime: {uptime}")
