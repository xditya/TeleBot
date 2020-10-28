""".admin Plugin for @UniBorg"""
from telethon.tl.types import ChannelParticipantsAdmins

from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="warn1"))
@telebot.on(sudo_cmd(pattern="warn1", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = (
        "`You Have  1/3  warnings...\nWatch out!....\nReason for warn: Porn Demand`"
    )
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


""".admin Plugin for @UniBorg"""


@telebot.on(admin_cmd(pattern="warn2"))
@telebot.on(sudo_cmd(pattern="warn2", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "`You Have  2/3  warnings...\nWatch out!....\nReason for last warn: Porn Demand`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


""".admin Plugin for @UniBorg"""


@telebot.on(admin_cmd(pattern="warn3"))
@telebot.on(admin_cmd(pattern="warn3", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = (
        "`You Have  3/3  warnings...\nBanned!!!....\nReason for ban: Porn Demand`"
    )
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


""".admin Plugin for @UniBorg"""


@telebot.on(admin_cmd(pattern="warn0"))
@telebot.on(admin_cmd(pattern="warn0", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "`Warning Resetted By Admin...\nYou Have  0/3  warnings`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


@telebot.on(admin_cmd(pattern="ocb"))
@telebot.on(sudo_cmd(pattern="ocb", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Warning..\n\nBattery Below 10%, Please Charge Your Phone**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


@telebot.on(admin_cmd(pattern="fw"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "`U Got A FloodWait:\nReason:telethon.errors.rpcerrorlist.FloodWaitError: A wait of 546578265716823 seconds is required (caused by EditMessageRequest)`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
