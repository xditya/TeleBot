import asyncio

from telebot import CMD_HELP
from telebot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(outgoing=True, pattern=r"mute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"mute ?(\d+)?"))
async def startmute(event):
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
            event, "Please reply to a user or add their into the command to mute them."
        )
    chat_id = event.chat_id
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await eor(
                event,
                "You can't mute a person if you dont have delete messages permission",
            )
    elif "creator" in vars(chat):
        pass
    elif private:
        pass
    else:
        return await eor(event, "You can't mute a person without admin rights")
    if is_muted(userid, chat_id):
        return await eor(event, "This user is already muted in this chat")
    try:
        mute(userid, chat_id)
    except Exception as e:
        await eor(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Successfully muted that person")


@telebot.on(admin_cmd(outgoing=True, pattern=r"unmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"unmute ?(\d+)?"))
async def endmute(event):
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
            "Please reply to a user or add their into the command to unmute them.",
        )
    chat_id = event.chat_id
    if not is_muted(userid, chat_id):
        return await eor(event, "This user is not muted in this chat")
    try:
        unmute(userid, chat_id)
    except Exception as e:
        await eor(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Successfully unmuted that person")


@telebot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()


CMD_HELP.update(
    {
        "mute": ".mute <reply to user>\nUse - Mute the user.\
        \n\n.unmute <reply to user>\nUse - UnMute the user."
    }
)
