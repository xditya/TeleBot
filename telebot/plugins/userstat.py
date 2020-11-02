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
#   thanks to @rekcah-pavi for the base

import html
import os

import spamwatch
from telethon.tl.functions.users import GetFullUserRequest

swapi = os.environ.get("SPAMWATCH_API_KEY", None)


@telebot.on(admin_cmd(pattern=f"ustat(?: |$)(.*)"))
@telebot.on(sudo_cmd(pattern=f"ustat(?: |$)(.*)", allow_sudo=True))
async def _(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        tele = await event.reply("`Processing...`")
    else:
        tele = await event.edit("`Processing...`")
    if event.fwd_from:
        return
    tuser, rdhs = await get_full_user(event)
    if tuser is None:
        await tele.edit("Error! Please mention user to check his stats!!")
        return False
    user_id = tuser.user.id
    first_name = html.escape(tuser.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    user_bio = tuser.about
    if user_bio is not None:
        user_bio = html.escape(tuser.about)
    spamw = "SpamWatch API not added.\nGet it from @SpamWatchBot and add it to `SPAMWATCH_API_KEY` for this plugin to work."
    sreason = {}
    try:
        cas_url = f"https://api.cas.chat/check?user_id={user_id}"
        r = get(cas_url, timeout=3)
        data = r.json()
    except BaseException:
        pass
    spambot = data = None
    if data:
        if data and data["ok"]:
            reason = f"[Banned by Combot Anti Spam](https://combot.org/cas/query?u={check_user.id})"
            spambot = True
    if spambot:
        sbot = "Yes"
        sn = reason
    else:
        sbot = "No"
        sn = {}
    if swapi:
        sw = spamwatch.Client(swapi)
        sswatch = sw.get_ban(user_id)
        if sswatch:
            spamw = "`Yes`"
            sreason = sswatch.reason
        else:
            spamw = "`No`"
            sreason = {}

    caption = f"**About** [{first_name}](tg://user?id={user_id})\n\n"
    caption += f"**User ID:** `{user_id}`\n"
    caption += f"**UserName:** `@{tuser.user.username}`\n"
    caption += f"**Scam:** `{tuser.user.scam}`\n"
    caption += f"**Restricted:** `{tuser.user.restricted}`\n"
    temp = tuser.user.restriction_reason
    if temp:
        caption += f"**Reason:** `{temp}`\n\n"
    caption += f"**Banned in SpamWatch:** {spamw}\n"
    if sreason:
        caption += f"**Reason:** `{sreason}`\n\n"
    caption += f"**Banned in CAS:** {sbot} [?](http://cas.chat)\n"
    if sn:
        caption += f"**Reason:** `{sn}`\n\n"
    await tele.edit(caption)


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            ruser = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return ruser, None
        else:
            ruser = await event.client(GetFullUserRequest(previous_message.from_id))
            return ruser, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                ruser = await event.client(GetFullUserRequest(user_id))
                return ruser, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    ruser = await event.client(GetFullUserRequest(user_id))
                    return ruser, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                ruser = await event.client(GetFullUserRequest(user_id))
                return ruser, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                ruser = await event.client(GetFullUserRequest(user_id))
                return ruser, None
            except Exception as e:
                return None, e
