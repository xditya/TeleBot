from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP
from userbot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="ascii ?(.*)"))
@telebot.on(sudo_cmd(pattern="ascii ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        xx = await event.eor(xx, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        xx = await event.eor(xx, "```reply to media message```")
        return
    chat = "@asciiart_bot"
    reply_message.sender
    if reply_message.sender.bot:
        xx = await event.eor(xx, "```Reply to actual users message.```")
        return
    xx = await event.eor(xx, "```Wait making ASCII...```")
    # For TeleBot
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164766745)
            )
            await borg.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @asciiart_bot and try again```")
            return
        if response.text.startswith("Forward"):
            xx = await event.eor(
                xx,
                "```can you kindly disable your forward privacy settings for good?```",
            )
        else:
            await borg.send_file(event.chat_id, response.message.media)


# For TeleBot
CMD_HELP.update(
    {
        "ascii": "`.ascii` reply to any image file:\
      \nUSAGE:makes an image ascii style, try out your own.\
      "
    }
)
