"""QuotLy: Avaible commands: .qbot
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from uniborg.util import admin_cmd

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="qbot ?(.*)"))
@telebot.on(sudo_cmd(pattern="qbot ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await eor(event, "```Reply to text message```")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await eor(event, "```Making a Quote```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
            return
        if response.text.startswith("Hi!"):
            await eor(
                event,
                "```Can you kindly disable your forward privacy settings for good?```",
            )
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update({"quotly": ".qbot <reply to message>\nUse - To make a quote."})
