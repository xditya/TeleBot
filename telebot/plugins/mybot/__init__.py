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

from telebot.plugins import OWNER_ID, TELE_NAME
import time
from datetime import datetime
from telebot.telebotConfig import Var

# start-other disabled
startotherdis = """
Hi there. I am {}'s bot. Nice to see you here.
""".format(TELE_NAME)

# start-other enabled
if Var.PMBOT_START_MSSG is None:
    MSSG = """
Hi there, I am {}'s personal bot.
You can contact him through me 😌.

Have a nice time!
""".format(TELE_NAME)
else:
    MSSG = Var.PMBOT_START_MSSG
startotherena = MSSG

# start-owner
startowner = """
Welcome back {}. Choose the options available from below:
""".format(TELE_NAME)

# for ping


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


xstart = datetime.now()
xend = datetime.now()
ms = (xend - xstart).microseconds / 1000
ping = f"🏓Pong\nPing speed: {ms}"
