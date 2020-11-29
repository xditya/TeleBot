"""
Userbot module to help you manage a group
"""

from asyncio import sleep
from datetime import datetime
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from telebot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from telebot.telebotConfig import Var
from telebot.utils import admin_cmd, errors_handler, sudo_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin here!`"
NO_PERM = "`No sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

BOTLOG_CHATID = Var.PRIVATE_GROUP_ID


@telebot.on(admin_cmd(outgoing=True, pattern="setgpic"))
@telebot.on(sudo_cmd(outgoing=True, pattern="setgpic", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.eor(event, "`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        x = await gpic.eor(x, NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            x = await gpic.eor(x, INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            x = await gpic.eor(x, CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            x = await gpic.eor(x, PP_TOO_SMOL)
        except ImageProcessFailedError:
            x = await gpic.eor(x, PP_ERROR)


@telebot.on(admin_cmd("promote(?: |$)(.*)"))
@telebot.on(sudo_cmd(pattern="promote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def promote(promt):
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    x = await edit_or_reply(promt, "`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "pro-admin"  # just in case
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await x.edit("`Promoted Successfully! Enjoy!!`")
    except BadRequestError:
        await x.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


@telebot.on(admin_cmd(outgoing=True, pattern="demote(?: |$)(.*)"))
@telebot.on(sudo_cmd(pattern="demote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")
    rank = "Admeen"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await eor(dmod, NO_PERM)
        return
    await eor(dmod, "`Demoted this retard!!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@telebot.on(admin_cmd(pattern="(ban|unban) ?(.*)"))
@telebot.on(sudo_cmd(pattern="(ban|unban) ?(.*)", allow_sudo=True))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = BANNED_RIGHTS
    elif input_cmd == "unban":
        rights = UNBAN_RIGHTS
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.sender_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await eor(event, str(exc))
    else:
        await eor(event, f"{input_cmd}ned Successfully!")


@telebot.on(admin_cmd(pattern="pgs ?(.*)"))
@telebot.on(sudo_cmd(pattern="pgs ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await borg.get_entity(input_str)
            logger.info(from_user)
        async for message in borg.iter_messages(
            event.chat_id, min_id=event.reply_to_msg_id, from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await borg.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await eor(event, "**PURGE** Failed!")


@telebot.on(admin_cmd(pattern="(ban|unban) ?(.*)"))
@telebot.on(sudo_cmd(pattern="(ban|unban) ?(.*)", allow_sudo=True))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = BANNED_RIGHTS
    elif input_cmd == "unban":
        rights = UNBAN_RIGHTS
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.sender_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await eor(event, str(exc))
    else:
        await eor(event, f"{input_cmd}ned Successfully!")


@telebot.on(admin_cmd(outgoing=True, pattern="admins$"))
@errors_handler
async def get_admin(show):
    """ For .admins command, list all of the admins of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"<b>Admins in {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@telebot.on(admin_cmd(outgoing=True, pattern="pin(?: |$)(.*)"))
@telebot.on(sudo_cmd(outgoing=True, pattern="pin(?: |$)(.*)"))
@errors_handler
async def pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await eor(msg, NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await eor(msg, "`Reply to a message to pin it.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await eor(msg, NO_PERM)
        return

    await eor(msg, "`Pinned Successfully!`")

    user = await get_user_from_id(msg.sender_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )


@telebot.on(admin_cmd(outgoing=True, pattern="kick(?: |$)(.*)"))
@telebot.on(sudo_cmd(outgoing=True, pattern="kick(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await eor(usr, NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await eor(usr, "`Couldn't fetch user.`")
        return

    await eor(usr, "`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await eor(usr, NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await eor(
            usr,
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}",
        )
    else:
        await eor(usr, f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@telebot.on(admin_cmd(outgoing=True, pattern="users ?(.*)"))
@errors_handler
async def get_users(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await eor(show, mentions)
    except MessageTooLongError:
        await eor(show, "Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="Users in {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await eor(event, "`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await eor(event, str(err))
            return None

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


CMD_HELP.update(
    {
        "admin": ".promote <username/reply> <custom rank (optional)>\
\nUse - : Provides admin rights to the person in the chat.\
\n\n.demote <username/reply>\
\nUse - : Revokes the person's admin permissions in the chat.\
\n\n.ban <username/reply> <reason (optional)>\
\nUse - : Bans the person off your chat.\
\n\n.unban <username/reply>\
\nUse - : Removes the ban from the person in the chat.\
\n\n.mute <username/reply> <reason (optional)>\
\nUse - : Mutes the person in the chat, works on admins too.\
\n\n.unmute <username/reply>\
\nUse - : Removes the person from the muted list.\
\n\n.admins\
\nUse - : Retrieves a list of admins in the chat.\
\n\n.users or .users <name of member>\
\nUse - : Retrieves all (or queried) users in the chat.\
\n\n.setgppic <reply to image>\
\nUse - : Changes the group's display picture."
    }
)
