# Lots of lub to @r4v4n4 for gibing the base <3
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="scan ?(.*)"))
@telebot.on(sudo_cmd(pattern="scan ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        xx = await event.eor(xx, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        xx = await event.eor(xx, "```reply to a media message```")
        return
    chat = "@DrWebBot"
    reply_message.sender
    if reply_message.sender.bot:
        xx = await event.eor(xx, "```Reply to actual users message.```")
        return
    xx = await event.eor(xx, " `Sliding my tip, of fingers over it`")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=161163358)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
        if response.text.startswith("Forward"):
            xx = await event.eor(
                xx,
                "```can you kindly disable your forward privacy settings for good?```",
            )
        else:
            if response.text.startswith("Select"):
                xx = await event.eor(
                    xx, "`Please go to` @DrWebBot `and select your language.`"
                )
            else:
                xx = await event.eor(
                    xx,
                    f"**Antivirus scan was completed. I got dem final results.**\n {response.message.message}",
                )
