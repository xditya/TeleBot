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

from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from telebot import CMD_HELP, bot
from telebot.plugins.sql_helper.gban_sql import *

from . import TELE_NAME

client = bot


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, f"* Pass the user's username, id or reply!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, "Failed \n **Error**\n", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await eor(event, str(err))
        return None
    return user_obj


@telebot.on(ChatAction)
async def handler(tele):
    if tele.user_joined or tele.user_added:
        try:
            from telebot.plugins.sql_helper.gban_sql import is_gbanned

            guser = await tele.get_user()
            gbanned = is_gbanned(guser.id)
        except BaseException:
            return
        if gbanned:
            for i in gbanned:
                if i.sender == str(guser.id):
                    chat = await tele.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                            await client.edit_permissions(
                                tele.chat_id, guser.id, view_messages=False
                            )
                            await tele.reply(
                                f"** Gbanned User Joined!!** \n"
                                f"**Victim Id**: [{guser.id}](tg://user?id={guser.id})\n"
                                f"**Action **  : `Banned`"
                            )
                        except BaseException:
                            return


@telebot.on(admin_cmd(pattern="gban(?: |$)(.*)"))
async def gspider(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`processing...`")
    else:
        rkp = await lazy.edit("`processing...`")
    me = await rk.client.get_me()
    await rkp.edit(f"**Global Banning User!!**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await rkp.edit("**Error! Unknown user.**")
    if user:
        if user.id == 719195224:
            return await rkp.edit("**Error! cant gban this user.**")
        try:
            from telebot.plugins.sql_helper.gban_sql import gban
        except BaseException:
            pass
        try:
            await rk.client(BlockRequest(user))
        except BaseException:
            pass
        testrk = [
            d.entity.id
            for d in await rk.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        await rkp.edit(f"**Gbanning user!\nIn progress...**")
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, view_messages=False)
                a += 1
            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**Reply to a user !! **")
    try:
        if gban(user.id) is False:
            return await rkp.edit(f"**Error! User probably already gbanned.**")
    except BaseException:
        pass
    return await rkp.edit(
        f"**Gbanned** [{user.first_name}](tg://user?id={user.id}) **\nChats affected - {a}\nBlocked user and added to Gban watch **"
    )


@telebot.on(admin_cmd(pattern="ungban(?: |$)(.*)"))
async def gspider(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`Processing...`")
    else:
        rkp = await lazy.edit("`Processing...`")
    me = await rk.client.get_me()
    await rkp.edit(f"**Requesting  to ungban user!**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await rkp.edit(f"**Error! Unknown user.**")
    if user:
        if user.id == 719195224:
            return await rkp.edit(f"**Error! cant ungban this user.**")
        try:
            from telebot.plugins.sql_helper.gban_sql import ungban
        except BaseException:
            pass
        try:
            await rk.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [
            d.entity.id
            for d in await rk.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        await rkp.edit(f"**Requesting  to ungban user!\nUnban in progress...**")
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, send_messages=True)
                a += 1
            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**Reply to a user !! **")
    try:
        if ungban(user.id) is False:
            return await rkp.edit(f"**Error! User probably already ungbanned.**")
    except BaseException:
        pass
    return await rkp.edit(
        f"**UnGbanned** [{user.first_name}](tg://user?id={user.id}) **\nChats affected - {a}\nUnBlocked and removed user from Gban watch **"
    )


CMD_HELP.update(
    {
        "gban": ".gban <username> / <userid> / <reply to a user>\
\n**Usage**: Global ban the person in all groups, channels , block in pm , add gban watch (use with solution) \
\n\n.ungban <username> / <userid> / <reply to a user>\
\n**Usage**: unban user from all groups, channels , remove user from gban watch.\
"
    }
)


@telebot.on(admin_cmd(pattern="listgbanned"))
@telebot.on(sudo_cmd(pattern="listgbanned", allow_sudo=True))
async def list(event):
    try:
        from telebot.plugins.sql_helper.gban_sql import all_gbanned
    except BaseException:
        await event.edit("Error. SQL Not found!")
        return
    doing = await eor(event, "`Making a list of GBanned Users`")
    allgbanned = all_gbanned()
    userlist = f"List of GBanned users by {TELE_NAME}\n"
    if len(allgbanned) > 0:
        for i in allgbanned:
            userlist += f"✘ [{i.sender}](tg://user?id={i.sender})"
    else:
        userlist = f"`{TELE_NAME} has not GBanned anyone!`"
    if len(userlist) > 4095:
        with io.BytesIO(str.encode(userlist)) as gbanned_list:
            gbanned_list.name = "GBanned.text"
            await telebot.send_file(
                event.chat_id,
                gbanned_list,
                force_document=True,
                allow_cache=False,
                caption=f"List of GBanned Users by {TELE_NAME}",
                reply_to=event,
            )
            await event.delete()
    else:
        await doing.edit(userlist)


CMD_HELP.update(
    {
        "gban": ".gban <username/userid/reply to a user>\
        \nUse - Global ban the person in all groups, channels , block in pm , add gban watch (use with solution)\
        \n\n.ungban <username/userid/reply to a user>\
        \nUse - UnbGan user from all groups, channels , remove user from gban watch.\
        \n\n.listgbanned\nUse - List all gbanned users."
    }
)
