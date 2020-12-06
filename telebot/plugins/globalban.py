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

from datetime import datetime

from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from telebot import CMD_HELP
from telebot.plugins.sql_helper.gban_sql import *

from . import OWNER_ID, TELE_NAME, tele_grps


@telebot.on(admin_cmd(pattern="gban(?: |$)(.*)"))
async def banhammer(event):
    tele = await eor(event, "`Processing...`")
    sender = await event.get_sender()
    start = datetime.now
    xdi, grps = await tele_grps(event)
    await tele.edit(
        "`Initiating a Global Ban of` [User](tg://user?id={}) `in` **{}** `chats!!`".format(
            sender.id, xdi
        )
    )
    await event.get_chat()
    a = b = 0
    if event.is_private:
        user = event.pattern_match.group(1)
        if not user:
            await tele.edit("`No user was designated. Aborting...`")
            return
    else:
        event.chat.title
    try:
        user, reason = await get_user_from_event(event)
    except BaseException:
        pass
    if user:
        if user.id == 719195224:
            return await tele.edit("`You can't GBan my Dev!`")
        if user.id == OWNER_ID:
            await tele.edit(
                "`Yeah, now start gbanning yourself.`\n`Aborting... You can't gban yourself`"
            )
        return
        try:
            await event.client(BlockRequest(user))
        except BaseException:
            pass
        await tele.edit(
            f"**Global Banning user!**\nUser - {user.id}\n**Chats Affecting** - `{xdi}`\n**Satus** - `In progress...`"
        )
        for i in xdi:
            try:
                await telebot.edit_permissions(i, user, view_messages=False)
                a += 1
            except BaseException:
                b += 1
    else:
        await tele.edit(f"`Reply to a user!!`")
    try:
        if gban(user.id) is False:
            return await tele.edit(f"**Error! User probably already gbanned.**")
    except BaseException:
        pass
    end = datetime.now
    timetaken = (end - start).seconds
    await tele.edit(
        f"**GBan**\n**User** - [{user.first_name}](tg://user?id={user.id})\n**Chats affected** - {a}\n**Blocked user** - `True`\n**Time taken** - `{timetaken} seconds`"
    )
    await telebot.send_message(
        Var.PRIVATE_GROUP_ID,
        "#GBan\nUser - {}\nTotal chats - {}\nDone in `{}` chats, failed in `{}` chats coz you are not an admin!".format(
            user.id, xdi, a, b
        ),
    )
    return


@telebot.on(admin_cmd(pattern="ungban(?: |$)(.*)"))
async def unban(event):
    tele = await eor(event, "`Processing...`")
    sender = await event.get_sender()
    start = datetime.now
    xdi, grps = await tele_grps(event)
    await tele.edit(
        "`Regression of Global Ban on` [User](tg://user?id={}) `in` **{}** `chats!!`".format(
            sender.id, xdi
        )
    )
    await event.get_chat()
    a = b = 0
    if event.is_private:
        user = event.pattern_match.group(1)
        if not user:
            await tele.edit("`No user was designated... Aborting...`")
            return
    else:
        event.chat.title
    try:
        user = await get_user_from_event(event)
    except BaseException:
        pass
    if user:
        if user.id == 719195224:
            return await tele.edit("`You can't GBan/UnGban my Dev!`")
        if user.id == OWNER_ID:
            await tele.edit(
                "`Yeah, now start (un)gbanning yourself.`\n`Aborting... You can't (un)gban yourself`"
            )
        return
        try:
            await event.client(UnblockRequest(user))
        except BaseException:
            pass
        await tele.edit(
            f"**Global UnBanning user!**\nUser - {user.id}\n**Chats Affecting** - `{xdi}`\n**Satus** - `In progress...`"
        )
        for i in xdi:
            try:
                await event.client.edit_permissions(i, user, send_messages=True)
                a += 1
            except BaseException:
                b += 1
    else:
        await tele.edit(f"`**`Reply to a user !!`")
    try:
        if ungban(user.id) is False:
            return await tele.edit(
                f"`This user wasn't gbanned or is already ungbanned!!`"
            )
    except BaseException:
        pass
    end = datetime.now
    timetaken = (end - start).seconds
    await tele.edit(
        f"**UnGBan**\n**User** - [{user.first_name}](tg://user?id={user.id})\n**Chats affected** - {a}\n**UnBlocked user** - `True`\n**Time taken** - `{timetaken} seconds`"
    )
    await telebot.send_message(
        Var.PRIVATE_GROUP_ID,
        "#UnGBan\nUser - {}\nTotal chats - {}\nDone in `{}` chats, failed in `{}` chats coz you are not an admin!".format(
            user.id, xdi, a, b
        ),
    )
    return


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


async def get_user_from_event(event):  
    args = event.pattern_match.group(1).split(':', 1)
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
            await event.edit(f"* Pass the user's username, id or reply!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Failed \n **Error**\n", str(err))           
    return user_obj, extra



# supposed to be a gban watch


@telebot.on(ChatAction)
async def handler(tele):
    if tele.user_joined or tele.user_added:
        try:
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
                            await telebot.send_message(
                                "#GBan_Action\n**Chat** - {}\n**User** - [{}](tg://user?id={})\n**Action** - `Banned`".format(
                                    tele.chat_id, guser.id
                                )
                            )
                        except BaseException:
                            return


CMD_HELP.update(
    {
        "gban": ".gban <username/userid/reply to a user>\
        \nUse - Global ban the person in all groups, channels , block in pm , add gban watch (use with solution)\
        \n\n.ungban <username/userid/reply to a user>\
        \nUse - UnbGan user from all groups, channels , remove user from gban watch.\
        \n\n.listgbanned\nUse - List all gbanned users."
    }
)
