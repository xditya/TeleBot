# For TeleBot.
# Add G_BAN_LOGGER_GROUP as config var for it to work.

"""Globally Ban users from all the
Group Administrations bots where you are SUDO
Available Commands:
.gban REASON
.ungban"""

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="botgban ?(.*)"))
@telebot.on(sudo_cmd(pattern="botgban ?(.*)", allow_sudo=True))
async def _(event):
    if Config.G_BAN_LOGGER_GROUP is None:
        await eor(
            event,
            "Make a group, add all your sudo bots and paste it's id in ENV VAR (G_BAN_LOGGER_GROUP) for this module to work.",
        )
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if r.forward:
            r_from_id = r.forward.from_id or r.from_id
        else:
            r_from_id = r.from_id
        await borg.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "/gban [user](tg://user?id={}) {}".format(r_from_id, reason),
        )
    await event.delete()


@telebot.on(admin_cmd(pattern="botungban ?(.*)"))
@telebot.on(sudo_cmd(pattern="botungban ?(.*)", allow_sudo=True))
async def _(event):
    if Config.G_BAN_LOGGER_GROUP is None:
        await eor(
            event,
            "Make a group, add all your sudo bots and paste it's id in ENV VAR (G_BAN_LOGGER_GROUP) for this module to work.",
        )
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_from_id = r.from_id
        await borg.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "/ungban [user](tg://user?id={}) {}".format(r_from_id, reason),
        )
    await event.delete()


CMD_HELP.update(
    {
        "gban_bots": ".botgban <reply to user/userid/username> <reason>\nUse - Gban in all bots you are sudo.\
        \n\n.botungban <reply to user/userid/username>\nUse - Ungban from all bots."
    }
)
