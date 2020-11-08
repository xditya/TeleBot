import asyncio

from telebot import CMD_HELP
from telebot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(outgoing=True, pattern=r"gmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"gmute ?(\d+)?"))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eor(
            event, "Please reply to a user or add their into the command to gmute them."
        )
    event.chat_id
    await event.get_chat()
    if is_muted(userid, "gmute"):
        return await eor(event, "This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await eor(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Silence now. **Successfully gmuted that person**")


@telebot.on(admin_cmd(outgoing=True, pattern=r"ungmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eor(
            event,
            "Please reply to a user or add their into the command to ungmute them.",
        )
    event.chat_id
    if not is_muted(userid, "gmute"):
        return await eor(event, "This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await eor(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Successfully ungmuted that person")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


CMD_HELP.update(
    {
        "gmute": ".gmute <reply to user>\nUse - Globally mute the person (across all chats).\
        \n\n.ungmute <reply to user>\nUse - Globally UnMute the person."
    }
)
