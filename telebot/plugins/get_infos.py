"""Get Administrators of any Chat*
Syntax: .get_admin, .get_bot, .get_id"""

from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
)
from telethon.utils import pack_bot_file_id

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="get_ad?(m)in ?(.*)"))
@telebot.on(sudo_cmd(pattern="get_ad?(m)in ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "m" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(2)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions_heading = "Admins in {} channel: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await borg.get_entity(input_str)
        except Exception as e:
            await eor(event, str(e))
            return None
    try:
        async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantCreator):
                    mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
        mentions += "\n"
        async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
            else:
                mentions += "\n `{}`".format(x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await eor(event, mentions)


@telebot.on(admin_cmd(pattern="get_id"))
@telebot.on(sudo_cmd(pattern="get_id", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await eor(
                event,
                "Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(
                    str(event.chat_id), str(r_msg.from_id), bot_api_file_id
                ),
            )
        else:
            await eor(
                event,
                "Current Chat ID: `{}`\nFrom User ID: `{}`".format(
                    str(event.chat_id), str(r_msg.from_id)
                ),
            )
    else:
        await eor(event, "Current Chat ID: `{}`".format(str(event.chat_id)))


@telebot.on(admin_cmd(pattern="get_bot ?(.*)"))
@telebot.on(sudo_cmd(pattern="get_bot ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Bots in this Channel**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Bots in {} channel: \n".format(input_str)
        try:
            chat = await borg.get_entity(input_str)
        except Exception as e:
            await eor(event, str(e))
            return None
    try:
        async for x in borg.iter_participants(chat, filter=ChannelParticipantsBots):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await eor(event, mentions)


CMD_HELP.update(
    {
        "get_infos": ".get_admin\nUse - To get admins in a chat.\
        \n\n.get_id\nUse - Get chat id.\
        \n\n.get_bot\nUse - Get all bots in a chat."
    }
)
