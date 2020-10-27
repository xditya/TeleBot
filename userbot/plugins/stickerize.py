from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot.utils import admin_cmd, sudo_cmd

# (c)2020 TeleBot


@telebot.on(admin_cmd(pattern="stickerize(?: |)(.*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern="stickerize(?: |$)(.*)"))
async def _(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        teletemp = await event.reply("`Processing...`")
    else:
        teletemp = await eor(event, "`Processing...`")
    try:
        reply_message = await event.get_reply_message()
        if reply_message:
            if not reply_message.media:
                return await teletemp.edit(
                    "`Reply to a photo to convert it to a stiker.`"
                )
        if not reply_message:
            return await teletemp.edit("**Syntax:**`.stickerize` reply to a  photo")
        chat = "@stickerator_bot"
        async with event.client.conversation(chat, timeout=7) as conv:
            try:
                test = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=384614990)
                )
                await event.client.forward_messages(chat, reply_message)
                response = await test
            except YouBlockedUserError:
                return await teletemp.edit(
                    "`Please unblock @stickerator_bot and try again`"
                )
            if response.text.startswith("274"):
                return await teletemp.edit("`Failed to convert`")
            await teletemp.delete()
            return await event.client.send_file(
                event.chat_id,
                response.message.media,
                reply_to=event.message.reply_to_msg_id,
            )
    except Exception as e:
        error = str(e)
        if not error:
            error = f"No response from {chat}"
        return await teletemp.edit(f"**Error**\n\n{error}")
