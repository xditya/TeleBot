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

from telethon import events, Button
from userbot.plugins import started, helpmefast, forinfo, forping

@tgbot.on(events.NewMessage(pattern="^/start"))
async def thisfn(event):
    await tgbot.send_message(
           event.chat_id,
           message=started,
           buttons = [
           [Button.url("Repository", "https://github.com/xditya/TeleBot/")]
            ]
      )
     
@tgbot.on(events.NewMessage(pattern="^/help"))
async def thisfn(event):
    await tgbot.send_message(
           event.chat_id,
           message=helpmefast,
           buttons = [
           [Button.url("TeleBot", "https://t.me/TeleBotSupport")]
            ]
      )
      
@tgbot.on(events.NewMessage(pattern="^/info ?(.*)"))
async def thisfn(event):
    caption = forinfo
    await tgbot.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
        buttons = [
           [Button.url("TeleBot", "https://t.me/TeleBotSupport")]
            ]
    )

@tgbot.on(events.NewMessage(pattern="^/ping"))
async def thisfn(event):
    await tgbot.send_message(
           event.chat_id,
           message=forping,
           buttons = [
           [Button.url("Deploy", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot")]
            ]
      )
