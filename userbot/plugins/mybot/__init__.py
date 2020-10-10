#    TeleBot - UserBot
#    Copyright (C) 2020 TeleBot

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html, time
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import ALIVE_NAME
from userbot.__init__ import StartTime
from datetime import datetime

# /start
started = f"**Welcome To TeleBot**\nHi, this is the assistant bot of {ALIVE_NAME}.\nSend `/help` to see what you can do here!\n\n(c) @TeleBotSupport"

# /help
helpmefast = "Here are the things that you can do with this bot!\n\n`/info @username` - get information about the user.\n`/ping` - Ping stats\n`/tr <lang_code>` - Use as reply to the text to translate, language codes can be foung [here](https://t.me/TeleBotHelpChat/22678)!.\n`/help` - This menu.\n\n__Set-up your own TeleBot via @TeleBotSupport to get such amazing features and more!__"

# /ping
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

start = datetime.now()
end = datetime.now()
ms = (end - start).microseconds / 1000
forping = f"🏓Ping speed: {ms}"
