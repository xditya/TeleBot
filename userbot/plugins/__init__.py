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
from userbot.utils import admin_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from userbot import telever, ALIVE_NAME
from heroku_config import Var

# stats
if Config.PRIVATE_GROUP_BOT_API_ID:
 log = "Enabled"
else:
 log = "Disabled"

if Config.TG_BOT_USER_NAME_BF_HER:
 bots = "Enabled"
else:
 bots = "Disabled"
 
if Var.LYDIA_API_KEY:
 lyd = "Enabled"
else:
 lyd = "Disabled"
 
if Config.SUDO_USERS:
 sudo = "Disabled"
else:
 sudo = "Enabled"
 
if Var.PMSECURITY.lower() == "off":
 pm = "Disabled" 
else:
 pm = "Enabled"
 
TELEUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"

tele =f"TeleBot Version: {telever}\n"
tele +=f"Log Group: {log}\n"
tele +=f"Assistant Bot: {bots}\n"
tele +=f"Lydia: {lyd}\n"
tele +=f"Sudo: {sudo}\n"
tele +=f"PMSecurity: {pm}\n"
tele +=f"\nVisit @TeleBotSupport for assistance.\n"
telestats = (f"{tele}")

# /start
started = f"**Welcome To TeleBot**\nHi, this is the assistant bot of {ALIVE_NAME}.\nSend `/help` to see what you can do here!\n\n(c) @TeleBotSupport"

# /help
helpmefast = "Here are the things that you can do with this bot!\n\n`/info @username` - get information about the user.\n`/ping` - Ping stats\n`/help` - This menu.\n\n__Set-up your own TeleBot via @TeleBotSupport to get such amazing features and more!__"

# /info
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    replied_user_profile_photos = await borg(GetUserPhotosRequest(
        user_id=replied_user.user.id,
        offset=42,
        max_id=0,
        limit=80
    ))
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError as e:
        pass
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Need a Profile Picture to check **this**"
        location = str(e)
    caption = """Extracted Userdata From TeleBot's DATABASE
ID: <code>{}</code>
Target's Name: <a href='tg://user?id={}'>{}</a>
Bio: {}
DC ID: {}
Number of PPs: {}
Restricted? : {}
Verified : {}
Bot : {}
No. of Common Groups : {}
""".format(
        user_id,
        user_id,
        first_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
        
async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
forinfo = caption

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
uptime = get_readable_time((time.time() - StartTime))
end = datetime.now()
ms = (end - start).microseconds / 1000

forping = f"🏓Ping speed: {ms}\n🤖TeleBot Uptime: {uptime}"

