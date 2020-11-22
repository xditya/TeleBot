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
#
import logging
import os
import sys
from asyncio import sleep

from telethon import events

from telebot import CMD_HELP
from telebot.telebotConfig import Var
from telebot.utils import admin_cmd

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)

NO_PM_LOG_USERS = []

BOTLOG = True
BOTLOG_CHATID = Var.PRIVATE_GROUP_ID


@telebot.on(admin_cmd(outgoing=True, pattern=r"save(?: |$)([\s\S]*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"save(?: |$)([\s\S]*)"))
async def log(log_text):
    """ For .log command, forwards a message or the command argument to the bot logs group """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to log?`")
            return
        await eor(log_text, "`Message saved 😁`")
        await sleep(5)
        await log_text.delete()
    else:
        await eor(log_text, "`This feature requires Logging to be enabled!`")
    await sleep(2)
    await log_text.delete()


@telebot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if Config.NC_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != borg.uid:
            try:
                if Config.PM_LOGGR_BOT_API_ID:
                    if event.message:
                        e = await borg.get_entity(int(Config.PM_LOGGR_BOT_API_ID))
                        fwd_message = await borg.forward_messages(
                            e, event.message, silent=True
                        )
                    else:
                        return
                else:
                    return
            except Exception as e:
                # logger.warn(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)


CMD_HELP.update(
    {
        "saver": ".save <reply to mssg>\
      \nUSAGE: saves taged message in private group .\ "
    }
)
