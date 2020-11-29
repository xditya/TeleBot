import asyncio

from telebot import CMD_HELP
from telebot.plugins import TELE_NAME
from telebot.plugins.sql_helper.gmute_sql import all_gmuted, gmute, is_gmuted, ungmute


@telebot.on(admin_cmd(outgoing=True, pattern=r"gmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"gmute ?(\d+)?"))
async def startgmute(event):
    doing = await eor(event, "`Gmuting...`")
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await doing.edit("`Unexpected issues or ugly errors may occur!`")
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
        return await doing.edit("`Please` **reply to a user** `to GMute him!`")
    event.chat_id
    await event.get_chat()
    if is_gmuted(userid):
        return await doing.edit("`This user is already gmuted`")
    try:
        gmute(userid)
    except Exception as e:
        await doing.edit("Error occured!\nError is " + str(e))
    else:
        await doing.edit("`Silence now.`\n**Successfully gmuted that person**")


@telebot.on(admin_cmd(outgoing=True, pattern=r"ungmute ?(\d+)?"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    doing = await eor(event, "`UnGmuting...`")
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await doint.edit("`Unexpected issues or ugly errors may occur!`")
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
        return await doing.edit("`Please` **reply to a user** `to GMute him!`")
    event.chat_id
    if not is_gmuted(userid):
        return await doing.edit("`This user ain't GMuted`")
    try:
        ungmute(userid)
    except Exception as e:
        await doing.edit("`Error occured!`\n" + str(e))
    else:
        await doing.edit("`Successfully ungmuted that person!`")


# By @its_xditya


@telebot.on(admin_cmd(pattern="listgmuted"))
@telebot.on(sudo_cmd(pattern="listgmuted", allow_sudo=True))
async def list(event):
    doing = await eor(event, "`Making a list of GMuted Users`")
    allgmuted = all_gmuted()
    userlist = f"List of GMuted users by {TELE_NAME}\n"
    if len(allgmuted) > 0:
        for i in allgmuted:
            userlist += f"✘ [{i.sender}](tg://user?id={i.sender})"
    else:
        userlist = f"{TELE_NAME} has not GMuted anyone!"
    if len(userlist) > 4095:
        with io.BytesIO(str.encode(userlist)) as gmuted_list:
            gmuted_list.name = "GMuted.text"
            await telebot.send_file(
                event.chat_id,
                gmuted_list,
                force_document=True,
                allow_cache=False,
                caption=f"List of GMuted Users by {TELE_NAME}",
                reply_to=event,
            )
            await event.delete()
    else:
        await doing.edit(userlist)


@command(incoming=True)
async def watcher(event):
    if is_gmuted(event.sender_id):
        await event.delete()


CMD_HELP.update(
    {
        "gmute": ".gmute <reply to user>\nUse - Globally mute the person (across all chats).\
        \n\n.ungmute <reply to user>\nUse - Globally UnMute the person.\
        \n\n.listgmuted\nUse - Get the list of users GMuted by you."
    }
)
