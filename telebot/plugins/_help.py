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

import os

from telebot import ALIVE_NAME, CMD_HELP, CMD_HNDLR, CMD_LIST
from telebot.telebotConfig import Config

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot User"
CMD_HNDLR = Config.CMD_HNDLR
CUSTOM_HELP_EMOJI = os.environ.get("CUSTOM_HELP_EMOJI", "⚡")

if CMD_HNDLR is None:
    CMD_HNDLR = "."


@telebot.on(admin_cmd(pattern="help ?(.*)"))
async def cmd_list(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        input_str = event.pattern_match.group(1)
        if tgbotusername is None or input_str == "text":
            string = ""
            for i in CMD_HELP:
                string += CUSTOM_HELP_EMOJI + " " + i + " " + CUSTOM_HELP_EMOJI + "\n"
                for iter_list in CMD_HELP[i]:
                    string += "    `" + str(iter_list) + "`"
                    string += "\n"
                string += "\n"
            if len(string) > 4095:
                with io.BytesIO(str.encode(string)) as out_file:
                    out_file.name = "cmd.txt"
                    await tgbot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="**COMMANDS**",
                        reply_to=reply_to_id,
                    )
                    await event.delete()
            else:
                await event.edit(string)
        elif input_str:
            if input_str in CMD_LIST:
                string = "**Commands available in {}** \n\n".format(input_str)
                if input_str in CMD_HELP:
                    for i in CMD_HELP[input_str]:
                        string += i
                    string += "\n\n**© @TeleBotSupport**"
                    await event.edit(string)
                else:
                    for i in CMD_LIST[input_str]:
                        string += "    " + i
                        string += "\n"
                    string += "\n**© @TeleBotSupport**"
                    await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            help_string = f"""`Userbot Helper for {DEFAULTUSER} to reveal all the commands of `**[TeleBot](https://xditya.gitbook.io/telebot/)**\n\n"""
            try:
                results = await bot.inline_query(  # pylint:disable=E0602
                    tgbotusername, help_string
                )
                await results[0].click(
                    event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
                )
                await event.delete()
            except BaseException:
                await event.edit(
                    f"This bot has inline disabled. Please enable it to use `{CMD_HNDLR}help`.\nGet help from [here](t.me/TeleBotHelpChat)"
                )
