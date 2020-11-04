# Re-written for TeleBot by @its_xditya
# Kangers, repo will be taken down if these lines are removed

"""
Available Commands:
.unbanall
.skick option
Available Options:
nostat - userstatusempty
onemonth - userstatuslastmonth
oneweek - userstatuslastweek
offline - userstatusoffline
online - userstatusonline
recent - userstatusrecently
bots - bot
delacc - deleted account"""

import asyncio
from time import sleep

from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from uniborg.util import admin_cmd

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="unbanall ?(.*)"))
@telebot.on(sudo_cmd(pattern="unbanall ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        await eor(event, "Searching Participant Lists.")
        p = 0
        async for i in borg.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await borg(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await eor(event, str(ex))
            else:
                p += 1
        await eor(event, "{}: {} unbanned".format(event.chat_id, p))


@telebot.on(admin_cmd(pattern="skick ?(.*)"))
@telebot.on(sudo_cmd(pattern="skick ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await eor(event, "`You aren't an admin here!`")
            return False
    p = 0
    bots = 0
    c = 0
    delacc = 0
    e = []
    onemonth = 0
    n = 0
    nostat = 0
    oneweek = 0
    offline = 0
    online = 0
    recent = 0
    await eor(event, "Searching Participant Lists.")
    async for i in borg.iter_participants(event.chat_id):
        p = p + 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            nostat = nostat + 1
            if "nostat" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            onemonth = onemonth + 1
            if "onemonth" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            oneweek = oneweek + 1
            if "oneweek" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            offline = offline + 1
            if "offline" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            online = online + 1
            if "online" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            recent = recent + 1
            if "recent" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            bots = bots + 1
            if "bots" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            delacc = delacc + 1
            if "delacc" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eor(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                else:
                    c = c + 1
        elif i.status is None:
            n = n + 1
    if input_str:
        required_string = """TeleBot has Kicked {} / {} users, out of which -
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await eor(
            event,
            required_string.format(
                c,
                p,
                delacc,
                nostat,
                onemonth,
                oneweek,
                offline,
                online,
                recent,
                bots,
                n,
            ),
        )
        await asyncio.sleep(5)
    await eor(
        event,
        """Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        ),
    )


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


CMD_HELP.update(
    {
        "management": ".unbanall\
     \n.skick option\
     \nAvailable Options: \
     \nnostat - userstatusempty\
     \nonemonth - userstatuslastmonth\
     \noneweek - userstatuslastweek\
     \noffline - userstatusoffline\
     \nonline - userstatusonline\
     \nrecent - userstatusrecently\
     \nbots - bot\
     \ndelacc - deleted account"
    }
)
