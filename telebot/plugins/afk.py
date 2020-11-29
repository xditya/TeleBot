#    TeleBot - UserBot
#    Copyright (C) 2020 TeleBot

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Based of AFK by @SpEcHIDe
# Media Afk, Time, by @xditya
"""
AFK Plugin for TeleBot
Syntax: .afk REASON
"""
import asyncio
import os
from datetime import datetime

from telegraph import Telegraph, upload_file
from telethon import Button, events
from telethon.tl import functions, types

from telebot import CMD_HELP
from telebot.telebotConfig import Config, Var

# --=============================================--#
global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global last_afk_message  # pylint:disable=E0602
global afk_start  # pylint:disable=E0602
global afk_end  # pylint:disable=E0602
# --=============================================--#
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}
BOTLOG = True
CUSTOM_AFK = Var.CUSTOM_AFK if Var.CUSTOM_AFK else "I am currently unavailable!"
botname = Var.TG_BOT_USER_NAME_BF_HER
if botname.startswith("@"):
    MYBOT = botname
else:
    MYBOT = f"@{botname}"
path = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(path):
    os.makedirs(path)
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]
# --=============================================--#


@telebot.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = afk_end - afk_start
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot:
        msg = None
        if reason is not None and tele == "True":
            message_to_reply = "**AFK**\n{}\n\n**Last active** `{}` **ago.**\n\n**Reason** : {}".format(
                CUSTOM_AFK, endtime, reason
            )
        elif tele == "False":
            message_to_reply = "**AFK**\n{}\n\n**Last active** `{}` **ago.**\n\n**Reason** - {}".format(
                CUSTOM_AFK, endtime, reason
            )
        else:
            message_to_reply = "**AFK**\n{}\n\n**Last active** {} **ago.**".format(
                CUSTOM_AFK, endtime
            )
        if event.chat_id not in Config.UB_BLACK_LIST_CHAT:
            msg = await event.reply(message_to_reply)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg
        chat = await event.get_chat()
        if Var.PRIVATE_GROUP_ID:
            await asyncio.sleep(5)
            if not event.is_private:
                mssgtosend = f"#AFK \nYou were tagged in `{chat.title}`"
                try:
                    await tgbot.send_message(
                        Var.PRIVATE_GROUP_ID,
                        mssgtosend,
                        buttons=[
                            Button.url(
                                "Go to Message",
                                url=f"https://t.me/c/{chat.id}/{event.message.id}",
                            )
                        ],
                    )
                except BaseException:
                    await telebot.send_message(
                        Var.PRIVATE_GROUP_ID,
                        f"Please add {MYBOT} here for afk tags to work.",
                    )


@telebot.on(admin_cmd(pattern=r"afk ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    global tele
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    tele = "False"
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if not USER_AFK:
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            media = await telebot.download_media(reply_message, "AFK_media")
            try:
                url = upload_file(media)
                os.remove(media)
            except BaseException:
                pass
            input_str = event.pattern_match.group(1)
            if url:
                if input_str is not None:
                    tele = "True"
                    reason = f"`{input_str}`[‎‏‏‎ ‎](https://telegra.ph/{url[0]})"
                else:
                    tele = "False"
                    reason = f"[‎‏‏‎ ‎](https://telegra.ph/{url[0]})"
            else:
                if input_str is not None:
                    reason = f"`{input_str}`"
        else:
            input_str = event.pattern_match.group(1)
            reason = f"`{input_str}`"
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USER_AFK = f"on: {reason}"
        if reason:
            await event.edit(
                f"`Your status has been set to AFK.`\n**Reason** - {reason}"
            )
            await asyncio.sleep(5)
            await event.delete()
        else:
            await event.edit("`Your status has been set to AFK.`")
            await asyncio.sleep(5)
            await event.delete()
        if BOTLOG:
            if reason:
                await event.client.send_message(
                    Var.PRIVATE_GROUP_ID,
                    f"#AFK \nAFK - Active\nReason - {reason}",
                )
            else:
                await event.client.send_message(
                    Var.PRIVATE_GROUP_ID,
                    f"#AFK \nAFK - Active\nReason - None Specified.",
                )


@telebot.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = afk_end - afk_start
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message = event.message.message
    if "afk" not in current_message and "on" in USER_AFK:
        shite = await event.client.send_message(
            event.chat_id,
            f"`I'm back!\nWas afk for {endtime}`",
        )
        USER_AFK = {}
        afk_time = None
        await asyncio.sleep(5)
        await shite.delete()
        if BOTLOG:
            await event.client.send_message(
                Var.PRIVATE_GROUP_ID, f"#AFK \n`AFK - Disabled\nAFK for {endtime}`"
            )


CMD_HELP.update(
    {
        "afk": "➟ `.afk` <optional reason>\nUse - Sets your status to AwayFromKeyboard. The bot will reply when you are tagged in groups. Will be auto turned off when you message again!"
    }
)
