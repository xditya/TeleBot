import asyncio

from telebot import CMD_HELP
from telebot.plugins.sql_helper.mute_sql import all_muted, is_muted, mute, unmute

from . import OWNER_ID, TELE_NAME


@telebot.on(admin_cmd(outgoing=True, pattern=r"mute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"mute ?(\d+)?"))
async def startmute(event):
    private = False
    ok = await eor(event, "Muting User...")
    if event.fwd_from:
        return
    elif event.is_private:
        await ok.edit("Muted! Quiet now!")
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
        return await ok.edit("Please reply to a user or send thier id to mute them.")
    if userid == OWNER_ID:
        await ok.edit("`Are you dumb?? Why are you trying to mute yourself??`")
        return
    chat_id = event.chat_id
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await ok.edit(
                "You can't mute a person if you dont have delete messages permission"
            )
    elif "creator" in vars(chat):
        pass
    elif private:
        pass
    else:
        return await ok.edit("You can't mute a person without admin rights")
    if is_muted(userid, chat_id):
        return await ok.edit("This user is already muted in this chat")
    try:
        mute(userid, chat_id)
    except Exception as e:
        await ok.edit("Error occured!\nError is " + str(e))
    else:
        await ok.edit(
            "Successfully muted [that person](tg://user?id={})".format(userid)
        )


@telebot.on(admin_cmd(outgoing=True, pattern=r"unmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"unmute ?(\d+)?"))
async def endmute(event):
    private = False
    ok = await eor(event, "UnMuting...")
    if event.fwd_from:
        return
    elif event.is_private:
        await ok.edit("UnMuted!")
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
        return await ok.edit("Please reply to a user or send thier id to mute them.")
    chat_id = event.chat_id
    if not is_muted(userid, chat_id):
        return await ok.edit("This user is not muted in this chat")
    try:
        unmute(userid, chat_id)
    except Exception as e:
        await ok.edit("Error occured!\nError is " + str(e))
    else:
        await ok.edit(
            "Successfully unmuted [that person](tg://user?id={})".format(userid)
        )


@telebot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()


@telebot.on(admin_cmd(pattern="listmuted"))
@telebot.on(sudo_cmd(pattern="listmuted", allow_sudo=True))
async def list(event):
    doing = await eor(event, "`Making a list of Muted Users`")
    allmuted = all_muted()
    userlist = f"List of Muted users by {TELE_NAME}\n"
    if len(allmuted) > 0:
        for i in allmuted:
            userlist += f"✘ [{i.sender}](tg://user?id={i.sender})"
    else:
        userlist = f"{TELE_NAME} has not Muted anyone!"
    if len(userlist) > 4095:
        with io.BytesIO(str.encode(userlist)) as muted_list:
            muted_list.name = "Muted.text"
            await telebot.send_file(
                event.chat_id,
                muted_list,
                force_document=True,
                allow_cache=False,
                caption=f"List of Muted Users by {TELE_NAME}",
                reply_to=event,
            )
            await event.delete()
    else:
        await doing.edit(userlist)


CMD_HELP.update(
    {
        "mute": ".mute <reply to user>\nUse - Mute the user.\
        \n\n.unmute <reply to user>\nUse - UnMute the user.\
        \n\n.listmuted\nUse - List all muted users."
    }
)
