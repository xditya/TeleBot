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

import asyncio

from telebot.plugins import OWNER_ID, TELE_NAME
from telebot.plugins.sql_helper.mute_sql import all_muted, is_muted, mute, unmute
from telebot.telebotConfig import Var


@telebot.on(admin_cmd(pattern=r"gmute ?(\d+)?"))
async def gmoot(event):
    tele = await eor(event, "`GMuting user...`")
    private = False
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    userid = reply.sender_id
    if userid == OWNER_ID:
        await tele.edit(r"Are you dumb nigga? Why would you mute yourself!!")
        return
    elif event.is_private:
        await tele.edit("Globally muted [user](tg://user?id={})".format(userid))
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await tele.edit("`Reply to a person or give me his id to GMute!!`")
    event.chat_id
    await event.get_chat()
    if is_muted(userid, "gmute"):
        return await tele.edit(
            "This [user](tg://user?id={}) is already GMuted!!".format(userid)
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await tele.edit("**Error**\n" + str(e))
    else:
        await tele.edit(
            "**GMuted!**\nUserID - {}\nLink - [here](tg://user?id={})".format(
                userid, userid
            )
        )
    try:
        await telebot.send_message(
            Var.PRIVATE_GROUP_ID,
            "#GMute\nUserID - {}\nLink - [here](tg://user?id={})".format(
                userid, userid
            ),
        )
    except BaseException:
        pass


@telebot.on(admin_cmd(pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    tele = await eor(event, "`UnGMuting user...`")
    if event.fwd_from:
        return
    elif event.is_private:
        await tele.edit("UnGMuted user")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await tele.edit("`Reply to a person or give me his id to UnGMute!!`")
    event.chat_id
    if not is_muted(userid, "gmute"):
        return await tele.edit("Hmm.. This person is not GMuted, yet!")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await tele.edit("**Error**\n" + str(e))
    else:
        await tele.edit(
            "**UnGMuted!**\nUserID - {}\nLink - [here](tg://user?id={})".format(
                userid, userid
            )
        )
    try:
        await telebot.send_message(
            Var.PRIVATE_GROUP_ID,
            "#UnGMute\nUserID - {}\nLink - [here](tg://user?id={})".format(
                userid, userid
            ),
        )
    except BaseException:
        pass


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@telebot.on(admin_cmd(pattern="listgmuted"))
@telebot.on(sudo_cmd(pattern="listgmuted", allow_sudo=True))
async def list(event):
    doing = await eor(event, "`Making a list of GMuted Users`")
    allmuted = all_muted()
    userlist = f"List of GMuted users by {TELE_NAME}\n"
    if len(allmuted) > 0:
        for i in allmuted:
            userlist += f"✘ [{i.sender}](tg://user?id={i.sender})"
    else:
        userlist = f"{TELE_NAME} has not GMuted anyone!"
    if len(userlist) > 4095:
        with io.BytesIO(str.encode(userlist)) as gmuted_list:
            gmuted_list.name = "GMuted.text"
            await telebot.send_file(
                event.chat_id,
                gmuted_list,
                force_document=True,
                allow_cache=False,
                caption=f"List of GMuted Users by {TELE_NAME}",
                reply_to=event,
            )
            await event.delete()
    else:
        await doing.edit(userlist)
