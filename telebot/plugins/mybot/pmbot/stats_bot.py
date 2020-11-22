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

from telebot.plugins.mybot.sql.blacklist_sql import all_bl_users
from telebot.plugins.mybot.sql.userbase_sql import full_userbase
from telethon import events
from telebot.plugins import OWNER_ID


@tgbot.on(events.NewMessage(pattern="^/stats", from_users=OWNER_ID))
async def tele(event):
    allu = len(full_userbase())
    blu = len(all_bl_users())
    await tgbot.send_message(event.chat_id,
                             "Here is the stats for your bot:\nTotal Users = {}\nBlacklisted Users = {}".format(allu, blu)
                             )
