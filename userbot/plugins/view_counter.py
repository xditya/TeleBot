"""Enable Seen Counter in any message to know how many users have seen your message
Syntax: .fwd as reply to any message"""

from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="frwd"))
@telebot.on(sudo_cmd(pattern="frwd", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if Config.CHANNEL_ID is None:
        await eor(
            event,
            "Please set the required environment variable `CHANNEL_ID` for this plugin to work",
        )
        return
    try:
        e = await borg.get_entity(Config.CHANNEL_ID)
    except Exception as e:
        await eor(event, str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await borg.forward_messages(e, re_message, silent=True)
        await borg.forward_messages(event.chat_id, fwd_message)
        await fwd_message.delete()
        await event.delete()
