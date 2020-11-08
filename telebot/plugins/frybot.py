# credits: @r4v4n4
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="frybot ?(.*)"))
@telebot.on(sudo_cmd(pattern="frybot ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eor(event, "```reply to text message```")
        return
    chat = "@image_deepfrybot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await eor(event, "```Processing```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=432858024)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
        if response.text.startswith("Forward"):
            await eor(
                event,
                "```can you kindly disable your forward privacy settings for good?```",
            )
        else:
            await borg.send_file(event.chat_id, response.message.media)


CMD_HELP.update({"frybot": ".frybot <reply to pic>\nUse - Fry the pic xD"})
